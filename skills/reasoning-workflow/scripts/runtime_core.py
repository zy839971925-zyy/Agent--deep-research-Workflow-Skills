#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import hashlib, json

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

@dataclass
class Finding:
    severity: str
    code: str
    message: str
    refs: list[str]
    def as_dict(self): return asdict(self)

def finding(sev, code, msg, *refs): return Finding(sev, code, msg, [r for r in refs if r])
def load_json(path: Path): return json.loads(path.read_text(encoding='utf-8'))

def validate_schema(data, schema_path: Path):
    if jsonschema is None:
        return [finding('ERROR','SCHEMA_RUNTIME_MISSING','Python package jsonschema is required for Draft 2020-12 validation')]
    schema=load_json(schema_path); v=jsonschema.Draft202012Validator(schema); out=[]
    for e in sorted(v.iter_errors(data), key=lambda x:list(x.absolute_path)):
        loc='/'.join(str(x) for x in e.absolute_path) or '$'
        out.append(finding('ERROR','SCHEMA',f'{loc}: {e.message}'))
    return out

def _canon(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def _sha_bytes(b: bytes): return 'sha256:'+hashlib.sha256(b).hexdigest()
def node_contract_payload(node): return {k:v for k,v in node.items() if k not in {'node_contract_hash'}}
def compute_node_contract_hash(node): return _sha_bytes(_canon(node_contract_payload(node)).encode())

def _cycles(nodes,deps):
    white,gray,black=0,1,2; color={n:white for n in nodes}; stack=[]; out=[]
    def dfs(u):
        color[u]=gray; stack.append(u)
        for v in deps.get(u,[]):
            if color.get(v,white)==white: dfs(v)
            elif color.get(v)==gray:
                try: i=stack.index(v); out.append(stack[i:]+[v])
                except ValueError: pass
        stack.pop(); color[u]=black
    for n in nodes:
        if color[n]==white: dfs(n)
    return out

def _ancestors(nodes):
    deps={nid:set(n.get('depends_on',[])) for nid,n in nodes.items()}; memo={}
    def anc(nid,seen=None):
        if nid in memo: return memo[nid]
        seen=set() if seen is None else seen
        if nid in seen: return set()
        seen.add(nid); out=set(deps.get(nid,set()))
        for d in list(out): out |= anc(d,seen.copy())
        memo[nid]=out; return out
    return {nid:anc(nid) for nid in nodes}

def validate_plan(plan, root: Path):
    out=validate_schema(plan,root/'schemas'/'execution-plan.schema.json')
    if any(f.severity=='ERROR' for f in out): return out
    nodes={}
    for n in plan.get('nodes',[]):
        nid=n['node_id']
        if nid in nodes: out.append(finding('ERROR','PLAN_DUPLICATE_NODE',f'duplicate node {nid}',nid))
        nodes[nid]=n
        actual=compute_node_contract_hash(n)
        if n.get('node_contract_hash')!=actual:
            out.append(finding('ERROR','NODE_CONTRACT_HASH',f'{nid} node_contract_hash does not match semantic node contract',nid))
        required=set(n.get('required_capabilities',[]))
        for fb in (n.get('degradation_policy') or {}).get('fallbacks',[]):
            if fb.get('required_capability') not in required:
                out.append(finding('ERROR','FALLBACK_UNBOUND_REQUIREMENT',f'{nid} fallback maps unknown/non-required capability {fb.get("required_capability")}',nid,fb.get('required_capability')))
        if n.get('side_effect_class') in ('consequential','irreversible') and n.get('replay_safety','safe')=='safe':
            out.append(finding('WARNING','REPLAY_SAFETY_SUSPICIOUS',f'{nid} has {n.get("side_effect_class")} side effects but replay_safety=safe; confirm this is genuinely replay-safe',nid))
    deps=defaultdict(list)
    for nid,n in nodes.items():
        for d in n.get('depends_on',[]):
            if d not in nodes: out.append(finding('ERROR','PLAN_DEP_MISSING',f'{nid} depends on missing node {d}',nid,d))
            else: deps[nid].append(d)
    for cyc in _cycles(nodes,deps): out.append(finding('ERROR','PLAN_DEP_CYCLE',f'execution dependency cycle: {" -> ".join(cyc)}',*cyc))
    return out

def validate_schedule(plan, schedule, root: Path, node_ledger: dict|None=None):
    out=validate_schema(schedule,root/'schemas'/'execution-schedule.schema.json')
    if schedule.get('plan_id')!=plan.get('plan_id'): out.append(finding('ERROR','SCHEDULE_PLAN_ID','schedule plan_id does not match execution plan'))
    if schedule.get('based_on_plan_version')!=plan.get('plan_version'): out.append(finding('ERROR','SCHEDULE_PLAN_VERSION','schedule is based on a stale/different plan_version'))
    nodes={n['node_id']:n for n in plan.get('nodes',[])}; seen=set(); bygroup=defaultdict(list); assignments={}; order={}
    deferred={x.get('node_id'):x for x in schedule.get('deferred_nodes',[]) if isinstance(x,dict)}
    precompleted=set(schedule.get('completed_prerequisite_refs',[]) or [])
    ledger_status={}
    if node_ledger:
        ledger_status={n.get('node_id'):n.get('effective_status') for n in node_ledger.get('nodes',[]) if isinstance(n,dict)}
    for i,a in enumerate(schedule.get('assignments',[])):
        nid=a.get('node_id'); order[nid]=i; assignments[nid]=a
        if nid in seen: out.append(finding('ERROR','SCHEDULE_DUPLICATE_ASSIGNMENT',f'node {nid} assigned more than once',nid))
        seen.add(nid)
        if nid not in nodes: out.append(finding('ERROR','SCHEDULE_UNKNOWN_NODE',f'assignment references unknown node {nid}',nid)); continue
        if a.get('node_contract_hash')!=nodes[nid].get('node_contract_hash'): out.append(finding('ERROR','SCHEDULE_STALE_CONTRACT',f'{nid} assignment uses stale node contract hash',nid))
        if nodes[nid].get('parallel_policy')=='forbidden' and schedule.get('mode') in ('parallel','hybrid') and a.get('concurrency_group'):
            out.append(finding('ERROR','PARALLEL_FORBIDDEN',f'{nid} forbids parallel execution',nid))
        if a.get('concurrency_group'): bygroup[a['concurrency_group']].append(a)
    for nid in deferred:
        if nid not in nodes: out.append(finding('ERROR','SCHEDULE_UNKNOWN_DEFERRED_NODE',f'deferred_nodes references unknown node {nid}',nid))
        if nid in assignments: out.append(finding('ERROR','SCHEDULE_NODE_BOTH_ASSIGNED_DEFERRED',f'{nid} is both assigned and deferred',nid))
    for nid in precompleted:
        if nid not in nodes: out.append(finding('ERROR','SCHEDULE_UNKNOWN_PREREQUISITE',f'completed_prerequisite_refs contains unknown node {nid}',nid))
        elif node_ledger and ledger_status.get(nid)!='verified_complete': out.append(finding('ERROR','SCHEDULE_PREREQUISITE_NOT_VERIFIED',f'{nid} is declared as completed prerequisite but ledger status is {ledger_status.get(nid)!r}',nid))
    if schedule.get('scope')=='full_plan':
        covered=set(assignments)|set(deferred)
        missing=set(nodes)-covered
        if missing: out.append(finding('ERROR','SCHEDULE_INCOMPLETE_FULL_PLAN',f'full_plan schedule omits nodes without defer reason: {sorted(missing)}',*sorted(missing)))
    # starts_after must resolve and be consistent with assignment order or completed prerequisites.
    for nid,a in assignments.items():
        for dep in a.get('starts_after',[]) or []:
            if dep not in nodes: out.append(finding('ERROR','SCHEDULE_STARTS_AFTER_UNKNOWN',f'{nid}.starts_after references unknown node {dep}',nid,dep)); continue
            if dep not in assignments and dep not in precompleted:
                out.append(finding('ERROR','SCHEDULE_STARTS_AFTER_UNSCHEDULED',f'{nid}.starts_after={dep}, but {dep} is neither scheduled nor a completed prerequisite',nid,dep))
            if dep in assignments and order.get(dep,10**9)>=order.get(nid,-1) and schedule.get('mode')=='serial':
                out.append(finding('ERROR','SCHEDULE_STARTS_AFTER_ORDER',f'{nid} starts_after {dep}, but serial assignment order does not place {dep} first',nid,dep))
    # Plan dependencies must be respected by schedule semantics.
    for nid,a in assignments.items():
        for dep in nodes[nid].get('depends_on',[]):
            if dep in assignments:
                same_group=a.get('concurrency_group') and a.get('concurrency_group')==assignments[dep].get('concurrency_group')
                if same_group:
                    out.append(finding('ERROR','SCHEDULE_DEP_CONCURRENT',f'{nid} depends on {dep} but both are in concurrency group {a.get("concurrency_group")}',nid,dep))
                if schedule.get('mode')=='serial':
                    if order.get(dep,10**9)>=order.get(nid,-1): out.append(finding('ERROR','SCHEDULE_DEP_ORDER',f'{nid} depends on {dep}, but serial order schedules dependency too late',nid,dep))
                elif dep not in (a.get('starts_after',[]) or []):
                    out.append(finding('ERROR','SCHEDULE_DEP_ORDER_UNDECLARED',f'{nid} depends on {dep}; parallel/hybrid schedule must declare starts_after dependency',nid,dep))
            elif dep not in precompleted and ledger_status.get(dep)!='verified_complete':
                out.append(finding('ERROR','SCHEDULE_DEP_UNSATISFIED',f'{nid} depends on {dep}, which is neither scheduled nor verified complete',nid,dep))
    ancestors=_ancestors(nodes)
    for group,items in bygroup.items():
        ids=[a['node_id'] for a in items if a.get('node_id') in nodes]
        for i in range(len(ids)):
            for j in range(i+1,len(ids)):
                a,b=ids[i],ids[j]
                if a in ancestors.get(b,set()) or b in ancestors.get(a,set()):
                    out.append(finding('ERROR','PARALLEL_DEPENDENCY_CONFLICT',f'concurrency group {group} contains ancestor/descendant nodes {a} and {b}',a,b))
        for i in range(len(items)):
            for j in range(i+1,len(items)):
                a,b=items[i],items[j]; na,nb=nodes.get(a.get('node_id')),nodes.get(b.get('node_id'))
                if not na or not nb: continue
                aw=set(na.get('write_set',[])); bw=set(nb.get('write_set',[])); ar=set(na.get('read_set',[])); br=set(nb.get('read_set',[]))
                lock_overlap=set(na.get('resource_locks',[])) & set(nb.get('resource_locks',[]))
                rw_conflict=(aw & (bw|br)) | (bw & ar)
                safely_isolated=a.get('isolation_mode') in ('isolated_workspace','transactional') and b.get('isolation_mode') in ('isolated_workspace','transactional')
                if (rw_conflict or lock_overlap) and not safely_isolated:
                    refs=sorted(rw_conflict|lock_overlap)
                    out.append(finding('ERROR','PARALLEL_STATE_CONFLICT',f'concurrency group {group} has shared mutable/resource conflict between {a["node_id"]} and {b["node_id"]}: {refs}',a['node_id'],b['node_id']))
    return out

def validate_capability_snapshot(snapshot, root: Path):
    out=validate_schema(snapshot,root/'schemas'/'capability-snapshot.schema.json'); seen=set()
    for c in snapshot.get('capabilities',[]):
        cid=c.get('capability_id')
        if cid in seen: out.append(finding('ERROR','CAPABILITY_DUPLICATE',f'duplicate capability snapshot entry {cid}',cid))
        seen.add(cid)
    return out

def evaluate_capabilities(plan, capability_snapshot, root: Path|None=None):
    out=[]
    if root is not None: out += validate_capability_snapshot(capability_snapshot,root)
    caps={c['capability_id']:c for c in capability_snapshot.get('capabilities',[]) if 'capability_id' in c}; routes={}
    for n in plan.get('nodes',[]):
        nid=n['node_id']; missing=[]; weaker=[]; chosen=[]; authorization=[]
        fallbacks=(n.get('degradation_policy') or {}).get('fallbacks',[])
        by_required=defaultdict(list)
        for fb in fallbacks: by_required[fb.get('required_capability')].append(fb)
        for req in n.get('required_capabilities',[]):
            c=caps.get(req)
            if c and c.get('availability') in ('available','degraded'):
                auth=c.get('authorization')
                if auth=='allowed': chosen.append(req); continue
                if auth=='approval_required':
                    authorization.append(req); out.append(finding('ERROR','AUTHORIZATION_REQUIRED',f'{nid} has capability {req} but approval is required before execution',nid,req)); continue
                if auth=='denied':
                    authorization.append(req); out.append(finding('ERROR','AUTHORIZATION_DENIED',f'{nid} capability {req} is available but authorization is denied',nid,req)); continue
            candidates=[]
            for fb in by_required.get(req,[]):
                cid=fb.get('fallback_capability'); meta=caps.get(cid)
                if not meta or meta.get('availability') not in ('available','degraded'): continue
                if meta.get('authorization')!='allowed':
                    if meta.get('authorization')=='approval_required': out.append(finding('ERROR','FALLBACK_AUTHORIZATION_REQUIRED',f'{nid} fallback {cid} for {req} requires approval',nid,req,cid))
                    continue
                candidates.append((cid,fb.get('equivalence'),fb.get('contract_delta')))
            equiv=[x for x in candidates if x[1]=='equivalent']; weak=[x for x in candidates if x[1]=='weaker']
            if equiv: chosen.append(equiv[0][0])
            elif weak:
                weaker.append((req,weak[0][0],weak[0][2])); out.append(finding('WARNING','CAPABILITY_WEAKER_FALLBACK',f'{nid} uses weaker fallback {weak[0][0]} for required {req}; original acceptance/evidence contract is not silently satisfied',nid,req,weak[0][0]))
            else:
                missing.append(req); out.append(finding('ERROR','CAPABILITY_BLOCKED',f'{nid} lacks required capability {req} and no authorized equivalent fallback is available',nid,req))
        routes[nid]={'chosen':chosen,'weaker':weaker,'missing':missing,'authorization_blocked':authorization,'executable':not missing and not authorization}
    return out,routes

def validate_node_ledger(plan, ledger, root: Path):
    out=validate_schema(ledger,root/'schemas'/'execution-node-state.schema.json')
    if ledger.get('plan_id')!=plan.get('plan_id'): out.append(finding('ERROR','NODE_LEDGER_PLAN_ID','node ledger plan_id does not match plan'))
    if ledger.get('plan_version')!=plan.get('plan_version'): out.append(finding('ERROR','NODE_LEDGER_PLAN_VERSION','node ledger is based on stale plan_version'))
    nodes={n['node_id']:n for n in plan.get('nodes',[])}; seen=set()
    for s in ledger.get('nodes',[]):
        nid=s.get('node_id')
        if nid in seen: out.append(finding('ERROR','NODE_LEDGER_DUPLICATE',f'duplicate node state {nid}',nid))
        seen.add(nid)
        if nid not in nodes: out.append(finding('ERROR','NODE_LEDGER_UNKNOWN_NODE',f'node ledger contains unknown node {nid}',nid)); continue
        if s.get('node_contract_hash')!=nodes[nid].get('node_contract_hash'): out.append(finding('ERROR','NODE_LEDGER_STALE_CONTRACT',f'{nid} node state uses stale contract hash',nid))
        if s.get('effective_status') in ('leased','running') and not s.get('active_attempt_id'): out.append(finding('ERROR','NODE_LEDGER_ATTEMPT_REQUIRED',f'{nid} is {s.get("effective_status")} without active_attempt_id',nid))
        if s.get('effective_status')=='leased' and not s.get('lease_id'): out.append(finding('ERROR','NODE_LEDGER_LEASE_REQUIRED',f'{nid} is leased without lease_id',nid))
        if s.get('effective_status')=='verified_complete' and nodes[nid].get('verification_contract') and not s.get('verification_refs'):
            out.append(finding('ERROR','NODE_LEDGER_VERIFICATION_REQUIRED',f'{nid} is verified_complete but has no verification_refs for a non-empty verification contract',nid))
        replay=s.get('replay_safety') or nodes[nid].get('replay_safety','safe')
        if replay in ('detectable','unsafe') and s.get('effective_status') in ('proposed_complete','verifying','verified_complete') and nodes[nid].get('side_effect_class')!='none' and not s.get('side_effect_receipts'):
            out.append(finding('ERROR','SIDE_EFFECT_RECEIPT_REQUIRED',f'{nid} replay_safety={replay} and side effects require a receipt before completion can be trusted',nid))
    return out

def compute_ready_nodes(plan, statuses_or_ledger, capability_routes=None):
    if isinstance(statuses_or_ledger,dict) and isinstance(statuses_or_ledger.get('nodes'),list):
        statuses={n.get('node_id'):n.get('effective_status') for n in statuses_or_ledger.get('nodes',[]) if isinstance(n,dict)}
    else: statuses=statuses_or_ledger or {}
    ready=[]
    for n in plan.get('nodes',[]):
        nid=n['node_id']; st=statuses.get(nid,'planned')
        if st not in ('planned','ready','stale','blocked'): continue
        if not all(statuses.get(d)=='verified_complete' for d in n.get('depends_on',[])): continue
        if capability_routes and not capability_routes.get(nid,{}).get('executable',False): continue
        ready.append(nid)
    return ready

def validate_worker_proposal(plan, proposal, root: Path|None=None, current_state_version: int|None=None):
    out=[]
    if root is not None: out += validate_schema(proposal,root/'schemas'/'worker-proposal.schema.json')
    nodes={n['node_id']:n for n in plan.get('nodes',[])}; nid=proposal.get('node_id')
    if proposal.get('plan_version')!=plan.get('plan_version'): out.append(finding('ERROR','WORKER_STALE_PLAN','worker proposal is based on stale plan_version',nid))
    if nid not in nodes: out.append(finding('ERROR','WORKER_UNKNOWN_NODE',f'worker proposal targets unknown node {nid}',nid)); return out
    node=nodes[nid]
    if proposal.get('node_contract_hash')!=node.get('node_contract_hash'): out.append(finding('ERROR','WORKER_STALE_CONTRACT',f'{nid} worker proposal uses stale node contract hash',nid))
    if proposal.get('writes_canonical_state') is True: out.append(finding('ERROR','WORKER_CANONICAL_WRITE','worker may propose state patches but may not directly commit canonical state',nid))
    if proposal.get('declared_status')=='verified_complete': out.append(finding('ERROR','WORKER_AUTHORITATIVE_COMPLETION','worker may declare proposed_complete, not verified_complete',nid))
    if current_state_version is not None and proposal.get('input_state_version')!=current_state_version:
        out.append(finding('ERROR','WORKER_STALE_INPUT_STATE',f'{nid} proposal is based on state_version {proposal.get("input_state_version")}, current is {current_state_version}',nid))
    allowed_writes=set(node.get('write_set',[])); proposed=set(proposal.get('write_set_proposed',[]) or [])
    extra=proposed-allowed_writes
    if extra: out.append(finding('ERROR','WORKER_WRITE_SCOPE',f'{nid} proposal writes outside node write_set: {sorted(extra)}',nid,*sorted(extra)))
    return out

def classify_worker_proposals(plan, proposals, root: Path|None=None, current_state_version: int|None=None):
    findings=[]; accepted=[]; stale=[]; conflicting=set()
    for p in proposals:
        fs=validate_worker_proposal(plan,p,root,current_state_version); findings += fs
        if any(f.severity=='ERROR' for f in fs): stale.append(p.get('proposal_id')); continue
        accepted.append(p)
    for i in range(len(accepted)):
        for j in range(i+1,len(accepted)):
            a,b=accepted[i],accepted[j]; overlap=set(a.get('write_set_proposed',[])) & set(b.get('write_set_proposed',[]))
            if overlap:
                conflicting.update([a.get('proposal_id'),b.get('proposal_id')])
                findings.append(finding('ERROR','WORKER_PATCH_CONFLICT',f'worker proposals {a.get("proposal_id")} and {b.get("proposal_id")} overlap write set {sorted(overlap)}',a.get('proposal_id'),b.get('proposal_id')))
    return findings,{
        'mergeable':[p.get('proposal_id') for p in accepted if p.get('proposal_id') not in conflicting],
        'conflicting':sorted(x for x in conflicting if x),
        'stale_or_invalid':[x for x in stale if x]
    }

def _component_payload(ref, root: Path, resolver=None):
    if resolver:
        try: return resolver(ref)
        except Exception: return None
    p=Path(ref)
    if not p.is_absolute(): p=root/ref
    if p.is_file(): return p.read_bytes()
    return None

def _payload_hash(payload):
    if payload is None: return None
    if isinstance(payload,bytes): return _sha_bytes(payload)
    if isinstance(payload,str): return _sha_bytes(payload.encode())
    return _sha_bytes(_canon(payload).encode())

def validate_checkpoint(checkpoint, root: Path, plan: dict|None=None, schedule: dict|None=None, component_resolver=None, parent_index: dict|None=None):
    out=validate_schema(checkpoint,root/'schemas'/'checkpoint-manifest.schema.json')
    comps=checkpoint.get('components',{}); required=checkpoint.get('required_components',[])
    for name in required:
        comp=comps.get(name)
        if not comp or comp.get('status')!='saved' or not comp.get('ref') or not comp.get('hash'):
            out.append(finding('ERROR','CHECKPOINT_COMPONENT_INCOMPLETE',f'required checkpoint component {name} is not durably saved with ref/hash',name)); continue
        bindings=comp.get('bindings') or {}
        for key in ('plan_version','schedule_version','state_version'):
            if bindings.get(key) is not None and bindings.get(key)!=checkpoint.get(key):
                out.append(finding('ERROR','CHECKPOINT_BINDING_MISMATCH',f'{name} component binds {key}={bindings.get(key)} but manifest says {checkpoint.get(key)}',name,key))
        if bindings.get('event_seq_end') is not None and checkpoint.get('event_seq_end') is not None and bindings.get('event_seq_end')!=checkpoint.get('event_seq_end'):
            out.append(finding('ERROR','CHECKPOINT_BINDING_MISMATCH',f'{name} component event_seq_end does not match manifest',name))
        if comp.get('integrity_proof','hash')=='hash':
            payload=_component_payload(comp.get('ref'),root,component_resolver); actual=_payload_hash(payload)
            if actual is None:
                out.append(finding('WARNING','CHECKPOINT_HASH_UNVERIFIED',f'{name} hash is declared but component content could not be resolved by this validator',name))
            elif actual!=comp.get('hash'):
                out.append(finding('ERROR','CHECKPOINT_HASH_MISMATCH',f'{name} component hash does not match referenced content',name))
        elif comp.get('integrity_proof')=='external_attestation' and not comp.get('attestation_ref'):
            out.append(finding('ERROR','CHECKPOINT_ATTESTATION_MISSING',f'{name} uses external_attestation without attestation_ref',name))
    groups={'completed':set(checkpoint.get('completed_nodes',[]) or []),'running':set(checkpoint.get('running_nodes',[]) or []),'blocked':set(checkpoint.get('blocked_nodes',[]) or [])}
    names=list(groups)
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            overlap=groups[names[i]] & groups[names[j]]
            if overlap: out.append(finding('ERROR','CHECKPOINT_NODE_STATE_OVERLAP',f'checkpoint nodes appear in both {names[i]} and {names[j]}: {sorted(overlap)}',*sorted(overlap)))
    if plan is not None:
        known={n['node_id'] for n in plan.get('nodes',[])}
        if checkpoint.get('plan_version')!=plan.get('plan_version'): out.append(finding('ERROR','CHECKPOINT_PLAN_VERSION',f'checkpoint plan_version {checkpoint.get("plan_version")} != plan {plan.get("plan_version")}'))
        unknown=(groups['completed']|groups['running']|groups['blocked'])-known
        if unknown: out.append(finding('ERROR','CHECKPOINT_UNKNOWN_NODE',f'checkpoint contains nodes not in current plan: {sorted(unknown)}',*sorted(unknown)))
    if schedule is not None:
        if checkpoint.get('schedule_version')!=schedule.get('schedule_version'): out.append(finding('ERROR','CHECKPOINT_SCHEDULE_VERSION','checkpoint schedule_version does not match schedule'))
        if checkpoint.get('plan_version')!=schedule.get('based_on_plan_version'): out.append(finding('ERROR','CHECKPOINT_SCHEDULE_PLAN_VERSION','checkpoint plan_version does not match schedule basis'))
    parent_id=checkpoint.get('parent_checkpoint_id')
    if parent_id:
        if not parent_index or parent_id not in parent_index:
            out.append(finding('WARNING','CHECKPOINT_PARENT_UNVERIFIED',f'parent checkpoint {parent_id} is not available to validate lineage',parent_id))
        else:
            parent=parent_index[parent_id]
            for k in ('plan_version','schedule_version','state_version'):
                if checkpoint.get(k,0)<parent.get(k,0): out.append(finding('ERROR','CHECKPOINT_VERSION_REGRESSION',f'{k} regressed from parent {parent.get(k)} to {checkpoint.get(k)}',checkpoint.get('checkpoint_id'),parent_id))
            if checkpoint.get('event_seq_end') is not None and parent.get('event_seq_end') is not None and checkpoint['event_seq_end']<parent['event_seq_end']:
                out.append(finding('ERROR','CHECKPOINT_EVENT_REGRESSION','event_seq_end regressed from parent checkpoint',checkpoint.get('checkpoint_id'),parent_id))
    if checkpoint.get('commit_status')=='complete' and any(f.severity=='ERROR' for f in out):
        out.append(finding('ERROR','CHECKPOINT_FALSE_COMPLETE','checkpoint declares complete but integrity/consistency checks fail',checkpoint.get('checkpoint_id')))
    if checkpoint.get('commit_status')!='complete': out.append(finding('WARNING','CHECKPOINT_NOT_COMMITTED','checkpoint is not a committed recovery point',checkpoint.get('checkpoint_id')))
    return out

def validate_checkpoint_chain(checkpoints, root: Path):
    out=[]; idx={c.get('checkpoint_id'):c for c in checkpoints if c.get('checkpoint_id')}
    # Parent existence + cycle + monotonic checks through validate_checkpoint.
    for c in checkpoints: out += validate_checkpoint(c,root,parent_index=idx)
    parent_adj={cid:[c.get('parent_checkpoint_id')] if c.get('parent_checkpoint_id') else [] for cid,c in idx.items()}
    for cyc in _cycles(idx,parent_adj): out.append(finding('ERROR','CHECKPOINT_LINEAGE_CYCLE',f'checkpoint lineage cycle: {" -> ".join(cyc)}',*cyc))
    return out

def compute_resume_actions(plan, ledger, checkpoint):
    """Return deterministic resume obligations. Restore is never equivalent to continue."""
    nodes={n['node_id']:n for n in plan.get('nodes',[])}; state={n.get('node_id'):n for n in (ledger or {}).get('nodes',[]) if isinstance(n,dict)}; actions=[]
    for nid in checkpoint.get('running_nodes',[]) or []:
        node=nodes.get(nid); ns=state.get(nid,{})
        if not node: continue
        replay=ns.get('replay_safety') or node.get('replay_safety','safe')
        receipts=ns.get('side_effect_receipts',[]) or []
        if replay=='safe': actions.append({'node_id':nid,'resume_action':'rerun_allowed'})
        elif replay=='idempotent': actions.append({'node_id':nid,'resume_action':'rerun_with_idempotency_key'})
        elif replay=='detectable': actions.append({'node_id':nid,'resume_action':'check_external_commit_before_retry','receipt_present':bool(receipts)})
        else: actions.append({'node_id':nid,'resume_action':'external_confirmation_required','receipt_present':bool(receipts)})
    return actions
