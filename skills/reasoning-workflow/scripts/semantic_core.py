#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict, deque
import json

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

COLLECTION_TYPES = {
    "requirements":"requirement", "acceptance_criteria":"acceptance_criterion", "questions":"question", "answers":"answer",
    "observations":"observation", "evidence":"evidence", "premises":"premise", "assumptions":"assumption", "hypotheses":"hypothesis",
    "uncertainties":"uncertainty", "relationships":"relationship", "inferences":"inference", "judgments":"judgment", "objectives":"objective",
    "constraints":"constraint", "alternatives":"alternative", "consequences":"consequence", "measurements":"measurement", "recommendations":"recommendation",
    "decisions":"decision", "risks":"risk", "actions":"action", "artifacts":"artifact", "verification":"verification", "effectiveness":"effectiveness",
}
CURRENT_LIKE = {"current","answered","bounded","passed","effective","satisfied","completed","ready","leading"}
BAD_EFFECTIVE = {"stale","invalidated","superseded","needs_recompute"}

@dataclass
class Finding:
    severity: str
    code: str
    message: str
    refs: list[str]
    def as_dict(self): return asdict(self)

def finding(sev, code, msg, *refs): return Finding(sev, code, msg, [r for r in refs if r])

def load_json(path: Path): return json.loads(path.read_text(encoding="utf-8"))

def validate_schema(data, schema_path: Path):
    if jsonschema is None:
        return [finding("ERROR","SCHEMA_RUNTIME_MISSING","Python package jsonschema is required for Draft 2020-12 machine validation")]
    schema=load_json(schema_path)
    validator=jsonschema.Draft202012Validator(schema)
    out=[]
    for e in sorted(validator.iter_errors(data), key=lambda x:list(x.absolute_path)):
        path="/".join(str(x) for x in e.absolute_path) or "$"
        out.append(finding("ERROR","SCHEMA",f"{path}: {e.message}"))
    return out

def build_registry(state):
    registry={}; findings=[]
    for col,rtype in COLLECTION_TYPES.items():
        for rec in state.get(col,[]) or []:
            rid=rec.get("id")
            if not rid: continue
            if rid in registry: findings.append(finding("ERROR","DUPLICATE_ID",f"duplicate record id {rid}",rid)); continue
            actual=rec.get("record_type")
            if actual!=rtype: findings.append(finding("ERROR","TYPE_COLLECTION_MISMATCH",f"{rid} record_type={actual!r} but collection {col} requires {rtype}",rid))
            registry[rid]={"record_type":rtype,"collection":col,"record":rec,"declared_status":rec.get("declared_status"),"effective_status":rec.get("declared_status"),"reasons":[]}
    return registry,findings

def load_policy(root: Path): return load_json(root/"schemas"/"edge-policy.json")

def typed_reference_findings(registry, policy):
    out=[]; edges=[]
    for rid,node in registry.items():
        rec=node["record"]
        for field,spec in policy["edges"].items():
            vals=rec.get(field,[]) or []
            if not isinstance(vals,list): continue
            for target in vals:
                if target not in registry:
                    out.append(finding("ERROR","DANGLING_REF",f"{rid}.{field} references missing {target}",rid,target)); continue
                allowed=spec.get("targets",["*"])
                tr=registry[target]["record_type"]
                if "*" not in allowed and tr not in allowed:
                    out.append(finding("ERROR","REF_TYPE",f"{rid}.{field} expects {allowed}, got {target} ({tr})",rid,target))
                edges.append((rid,field,target,spec))
        # fields governed outside policy
        if node['record_type']=='relationship':
            for f in ('from_ref','to_ref'):
                t=rec.get(f)
                if t and t not in registry: out.append(finding("ERROR","DANGLING_REF",f"{rid}.{f} references missing {t}",rid,t))
        if node['record_type']=='question':
            for f in ('parent_question_ref',):
                t=rec.get(f)
                if t:
                    if t not in registry: out.append(finding("ERROR","DANGLING_REF",f"{rid}.{f} references missing {t}",rid,t))
                    elif registry[t]['record_type']!='question': out.append(finding("ERROR","REF_TYPE",f"{rid}.{f} must target question, got {registry[t]['record_type']}",rid,t))
            for t in rec.get('child_question_refs',[]) or []:
                if t not in registry: out.append(finding("ERROR","DANGLING_REF",f"{rid}.child_question_refs references missing {t}",rid,t))
                elif registry[t]['record_type']!='question': out.append(finding("ERROR","REF_TYPE",f"{rid}.child_question_refs must target question, got {registry[t]['record_type']}",rid,t))
        if node['record_type']=='verification':
            for t in rec.get('target_refs',[]) or []:
                if t not in registry: out.append(finding("ERROR","DANGLING_REF",f"{rid}.target_refs references missing {t}",rid,t))
    return out,edges

def _find_cycles(nodes, adj):
    WHITE,GRAY,BLACK=0,1,2; color={n:WHITE for n in nodes}; cycles=[]; stack=[]
    def dfs(u):
        color[u]=GRAY; stack.append(u)
        for v in adj.get(u,[]):
            if color.get(v,WHITE)==WHITE: dfs(v)
            elif color.get(v)==GRAY:
                try:i=stack.index(v); cycles.append(stack[i:]+[v])
                except ValueError: pass
        stack.pop(); color[u]=BLACK
    for n in nodes:
        if color[n]==WHITE: dfs(n)
    return cycles

def cycle_findings(registry, edges, policy):
    out=[]
    logical=defaultdict(list)
    for src,field,target,spec in edges:
        if spec.get('direction')=='dependency' and spec.get('cycle')=='forbid' and spec.get('effect') in ('hard','recompute'):
            logical[src].append(target)
    for cyc in _find_cycles(registry.keys(),logical):
        out.append(finding("ERROR","LOGICAL_DEPENDENCY_CYCLE",f"dependency cycle across edge types: {' -> '.join(cyc)}",*cyc))
    # field dependency cycles
    byfam=defaultdict(lambda:defaultdict(list))
    for src,field,target,spec in edges:
        if spec.get('cycle')=='forbid': byfam[field][src].append(target)
    for field,adj in byfam.items():
        for cyc in _find_cycles(registry.keys(),adj): out.append(finding("ERROR","CYCLE_FORBIDDEN",f"forbidden cycle via {field}: {' -> '.join(cyc)}",*cyc))
    # relationship semantic cycles by relation type
    rel_adj=defaultdict(lambda:defaultdict(list))
    for rid,node in registry.items():
        if node['record_type']!='relationship': continue
        r=node['record']; rt=r.get('relation_type'); a=r.get('from_ref'); b=r.get('to_ref')
        if a in registry and b in registry: rel_adj[rt][a].append(b)
    for rt,adj in rel_adj.items():
        cp=policy.get('relationship_cycle_policy',{}).get(rt,'audit')
        cycles=_find_cycles(registry.keys(),adj)
        for cyc in cycles:
            sev='ERROR' if cp=='forbid' else ('WARNING' if cp=='audit' else None)
            if sev: out.append(finding(sev,"RELATION_CYCLE",f"{rt} cycle: {' -> '.join(cyc)}",*cyc))
    # circular support is warning
    sadj=defaultdict(list)
    for src,field,target,spec in edges:
        if field=='supports': sadj[src].append(target)
    for cyc in _find_cycles(registry.keys(),sadj): out.append(finding("WARNING","CIRCULAR_SUPPORT",f"circular support requires independent grounding: {' -> '.join(cyc)}",*cyc))
    return out

def compute_effective(registry, edges):
    # Monotone severity joins make the fixed point independent of edge order.
    rank={'needs_recompute':1,'stale':2,'superseded':3,'invalidated':4}
    reasons=defaultdict(list)
    for node in registry.values():
        node['effective_status']=node['declared_status']
    def promote(rid,status,reason):
        if rank.get(status,0) <= rank.get(registry[rid]['effective_status'],0):
            return False
        registry[rid]['effective_status']=status
        reasons[rid].append(reason)
        return True
    for src,field,target,spec in edges:
        if spec.get('effect')=='invalidate_target':
            promote(target,'invalidated',(src,field,'invalidated'))
        elif spec.get('effect')=='supersede_target':
            promote(target,'superseded',(src,field,'superseded'))
    # explicit declared stale/invalid/superseded and task-temporal applicability
    for rid,node in registry.items():
        if node['record'].get('current_for_task') is False and node['declared_status'] not in ('historical','superseded','invalidated'):
            promote(rid,'stale',('temporal_scope','current_for_task','stale'))
    changed=True
    while changed:
        changed=False
        for downstream,field,upstream,spec in edges:
            if spec.get('direction')!='dependency': continue
            us=registry[upstream]['effective_status']; ds=registry[downstream]['effective_status']; eff=spec.get('effect')
            bad=us in BAD_EFFECTIVE
            if not bad: continue
            new=None
            if eff=='hard': new='invalidated' if us=='invalidated' else 'stale'
            elif eff=='recompute': new='needs_recompute'
            if new and promote(downstream,new,(upstream,field,new)):
                changed=True
    for rid,node in registry.items(): node['reasons']=reasons.get(rid,[])
    return registry

def effective_chain(registry,rid):
    seen=set(); parts=[]; cur=rid
    # choose first reason recursively for concise path
    def walk(x):
        if x in seen:return
        seen.add(x)
        rs=registry.get(x,{}).get('reasons',[])
        if rs:
            upstream,field,effect=rs[0]; walk(upstream); parts.append(f"{upstream} --{field}--> {x} ({effect})")
    walk(cur)
    return parts

def effective_state_findings(registry):
    out=[]
    for rid,node in registry.items():
        ds=node['declared_status']; es=node['effective_status']; mat=node['record'].get('materiality','supporting')
        if ds in CURRENT_LIKE and es in BAD_EFFECTIVE:
            chain='; '.join(effective_chain(registry,rid))
            sev='ERROR' if mat=='material' else 'WARNING'
            out.append(finding(sev,"DECLARED_EFFECTIVE_CONFLICT",f"{rid} declares {ds} but computes {es}"+(f": {chain}" if chain else ""),rid))
    return out

def compute_epistemic_closure(state,registry):
    blockers=[]; warnings=[]
    if state.get('lane') not in ('question','mixed'):
        return {'applicable':False,'computed_epistemic_closed':False,'blockers':[],'warnings':[]}
    root=state.get('root_question_ref')
    if not root: blockers.append('No root_question_ref is defined.')
    elif root not in registry or registry[root]['record_type']!='question': blockers.append(f'root_question_ref {root!r} does not resolve to a Question.')
    else:
        q=registry[root]; qr=q['record']; es=q['effective_status']
        if es not in ('answered','bounded'): blockers.append(f'{root} effective status is {es}, not answered/bounded.')
        answers=qr.get('answer_refs',[]) or []
        current_answers=[a for a in answers if a in registry and registry[a]['record_type']=='answer' and registry[a]['effective_status'] in ('current','bounded')]
        if not current_answers: blockers.append(f'{root} has no current/bounded answer.')
        if qr.get('recomposition_status','not_required') not in ('pass','not_required'): blockers.append(f'{root} recomposition_status is {qr.get("recomposition_status")}')
        if qr.get('drift_check','pending')!='pass': blockers.append(f'{root} question drift check is not pass.')
        for child in qr.get('child_question_refs',[]) or []:
            if child in registry:
                cr=registry[child]['record']; ces=registry[child]['effective_status']
                if cr.get('materiality','supporting')=='material':
                    allowed = ces in ('answered','bounded') or (ces=='deferred' and cr.get('closure_effect','blocking')=='nonblocking')
                    if not allowed: blockers.append(f'{child} is a material child question with effective status {ces}.')
        # blocking material uncertainties linked to root or its answers
        relevant=set(qr.get('uncertainty_refs',[]) or [])
        for a in current_answers: relevant.update(registry[a]['record'].get('uncertainty_refs',[]) or [])
        for uid in relevant:
            if uid in registry:
                ur=registry[uid]['record']; ues=registry[uid]['effective_status']
                if ur.get('materiality','supporting')=='material' and ur.get('closure_effect','blocking')=='blocking' and ues=='open': blockers.append(f'{uid} is material, blocking, and open.')
        # decisive premises / dependencies on current answer must be admissible
        for a in current_answers:
            if registry[a]['effective_status'] in BAD_EFFECTIVE: blockers.append(f'{a} is effectively {registry[a]["effective_status"]}.')
    return {'applicable':True,'computed_epistemic_closed':not blockers,'blockers':blockers,'warnings':warnings}


def compute_runtime_closure(state, registry):
    blockers=[]; warnings=[]
    if state.get('lane') not in ('action','mixed'):
        return {'applicable':False,'computed_runtime_closed':False,'blockers':[],'warnings':[]}
    for rid,node in registry.items():
        rec=node['record']; rt=node['record_type']; es=node['effective_status']; mat=rec.get('materiality','supporting'); ce=rec.get('closure_effect','nonblocking')
        if mat!='material':
            continue
        if rt in ('requirement','acceptance_criterion'):
            allowed = es in ('satisfied','not_applicable','superseded') or (es=='deferred' and ce=='nonblocking')
            if not allowed: blockers.append(f'{rid} material {rt} is {es}.')
        elif rt in ('artifact',):
            if es not in ('current','historical','superseded'): blockers.append(f'{rid} material artifact is {es}.')
        elif rt=='verification':
            if ce=='blocking' and es!='passed': blockers.append(f'{rid} material blocking verification is {es}.')
        elif rt=='effectiveness':
            if ce=='blocking' and es not in ('effective',): blockers.append(f'{rid} material blocking effectiveness is {es}.')
        elif rt=='action':
            if es!='completed': blockers.append(f'{rid} material action is {es}.')
        elif rt in ('decision','recommendation','judgment','inference'):
            if es in ('stale','invalidated','needs_recompute','failed','blocked'): blockers.append(f'{rid} material {rt} is {es}.')
    if state.get('blocked_items'): blockers.append('canonical blocked_items is non-empty.')
    return {'applicable':True,'computed_runtime_closed':not blockers,'blockers':blockers,'warnings':warnings}

def summary(registry):
    return {rid:{'record_type':n['record_type'],'declared_status':n['declared_status'],'effective_status':n['effective_status'],'reasons':n['reasons']} for rid,n in registry.items()}
