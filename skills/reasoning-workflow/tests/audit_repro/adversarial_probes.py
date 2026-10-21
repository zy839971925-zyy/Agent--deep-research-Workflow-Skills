from pathlib import Path
import sys,json,copy,importlib.util,tempfile,hashlib
HERE=Path(__file__).resolve().parent
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--skill',type=Path,default=HERE/'new/Reasoning Workflow');ap.add_argument('--output',type=Path,default=HERE/'adversarial_results.json');args=ap.parse_args()
ROOT=args.skill.resolve();sys.path.insert(0,str(ROOT/'scripts'))
import runtime_core as rt
from routing_core import route_task,recheck_profile,validate_profile
from route_resources import select
from learning_core import admit_record,retrieve
from validate_workflow import fingerprint,validate_bridge
from validate_state import validate as state_valid
spec=importlib.util.spec_from_file_location('suite',ROOT/'tests/run_regression.py');suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)
FIX=ROOT/'tests/fixtures';load=lambda n:json.loads((FIX/n).read_text());err=lambda fs:[f.code for f in fs if f.severity=='ERROR']
results=[]
def log(id,expected,actual,**kw):
 results.append(dict(id=id,expected=expected,actual=actual,**kw))
# B1: forbid parallel, no display-group label
x=load('legal_parallel_independent_input.json')
for n in x['plan']['nodes']:
 n['parallel_policy']='forbidden';n['node_contract_hash']=rt.compute_node_contract_hash(n)
for a,n in zip(x['schedule']['assignments'],x['plan']['nodes']):a['node_contract_hash']=n['node_contract_hash']
log('B1_parallel_forbidden_without_group','validation refuses unsequenced parallel forbidden nodes',dict(plan_errors=err(rt.validate_plan(x['plan'],ROOT)),schedule_errors=err(rt.validate_schedule(x['plan'],x['schedule'],ROOT))))
for a in x['schedule']['assignments']:a['concurrency_group']='G'
log('C1_parallel_group_control','refuses same schedule with group',err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
# B2: Ultra resources can remain permanently out of batch
p=load('standard_profile.json');p.update(requested_depth='ultra',task_modes=['research'],active_gap_tags=[]);p=recheck_profile(p,[]);r=route_task(p);index=json.loads((ROOT/'routing-index.json').read_text());selected=select(index,r,p,[])
log('B2_explicit_ultra_not_selected','Ultra method reachable on explicit Ultra even without extra tags',dict(profile_valid=validate_profile(p,ROOT),route=r,selected=[s['reference_id'] for s in selected],repeat_selected=[s['reference_id'] for s in select(index,r,p,[])]))
p['active_gap_tags']=['ultra'];selected=select(index,route_task(p),p,[])
log('C2_ultra_tag_control','ultra tag selects overlay',[s['reference_id'] for s in selected])
p['active_gap_tags']=['ultra','delegation','recovery','orthogonal-verification'];selected=select(index,route_task(p),p,[])
log('B2b_multi_gap_coverage','recovery control either selected or explicitly queued',[s['reference_id'] for s in selected])
# B3: tier3 required evidence not resolved
q=load('learning_intrinsic_flag_false.json');q.update(tier=3,status='promoted',source_eval_refs=['eval-good'],regression_refs=['missing-regression'],held_out_eval_refs=['missing-heldout'],baseline_comparison_ref='missing-baseline',dual_review_ref='missing-review',rollback_ref='missing-rollback');q['provenance']={'feedback_types':['deterministic_verifier'],'intrinsic_reflection_only':False}
seen=[]
def resolver(ref):seen.append(ref);return ref=='eval-good'
fs=admit_record(q,ROOT,resolver)
log('B3_tier3_unresolved_promotion_gates','must resolve required promotion evidence',dict(findings=fs,resolver_calls=seen.copy(),maintenance_retrieved=[x['learning_id'] for x in retrieve([q],['deep_research'],[],maintenance=True,validation_resolver=resolver)]))
import subprocess
with tempfile.TemporaryDirectory() as td:
 d=Path(td);(d/'receipt.txt').write_text('actual one external evaluation receipt')
 (d/'index.json').write_text(json.dumps({'eval-good':{'verdict':'pass','kind':'external_evaluation','path':'receipt.txt','sha256':hashlib.sha256((d/'receipt.txt').read_bytes()).hexdigest()}}))
 (d/'record.json').write_text(json.dumps(q))
 proc=subprocess.run([sys.executable,str(ROOT/'scripts/validate_learning.py'),str(d/'record.json'),'--validation-evidence',str(d/'index.json')],capture_output=True,text=True)
 log('B3_cli_promotion_gate','missing tier3 gate references rejected even if source eval is real',dict(exit_code=proc.returncode,stdout=json.loads(proc.stdout)))
log('C3_ordinary_tier3_control','tier3 excluded from ordinary retrieval',[x['learning_id'] for x in retrieve([q],['deep_research'],[],validation_resolver=resolver)])
# B4: strict review fingerprint omits relationship endpoint payload
case=suite.Regression();case.setUp()
try:
 p,r,s,m,b=case.bridge()
 s['observations']=[{'id':'o1','record_type':'observation','declared_status':'current','text':'critical original observation'}]
 s['relationships']=[{'id':'rel1','record_type':'relationship','declared_status':'current','relation_type':'causes','epistemic_status':'inferred','from_ref':'o1','to_ref':'e1'}]
 s['answers'][0]['depends_on'].append('rel1')
 fs,reg,closure=state_valid(s,ROOT)
 log('B4_fixture_schema_check','valid fixture',dict(errors=err(fs),closure=closure))
 for entry in b['reviews']:
  entry['target_fingerprint']=fingerprint(s,entry['target_refs'])
  for v in s['verification']:
   if v['id']==entry['record']['verification_id']:v['metadata']['target_fingerprint']=entry['target_fingerprint']
 before=validate_bridge(p,r,s,m,b,case.d)
 oldfp=fingerprint(s,['a1']);s['observations'][0]['text']='opposite critical observation, not reviewed'
 after=validate_bridge(p,r,s,m,b,case.d)
 log('B4_singular_endpoint_fingerprint','source endpoint change invalidates old target review',dict(before=before,after=after,fingerprint_unchanged=oldfp==fingerprint(s,['a1'])))
 oldfp=fingerprint(s,['a1']);s['evidence'][0]['text']='direct evidence changed'
 log('C4_direct_evidence_control','direct evidence mutation invalidates review',dict(fingerprint_changed=oldfp!=fingerprint(s,['a1']),bridge_passed=validate_bridge(p,r,s,m,b,case.d)['passed']))
 # B5: Question lane required acceptance incomplete
 p,r,s,m,b=case.bridge()
 s['requirements'][0]['closure_effect']='blocking';s['acceptance_criteria'][0]['closure_effect']='blocking'
 s['requirements'][0]['declared_status']='blocked';m['requirements'][0]['declared_status']='blocked'
 s['acceptance_criteria'][0]['declared_status']='blocked';m['acceptance_criteria'][0]['declared_status']='blocked'
 fs,result=__import__('validate_delivery').validate(s,m,case.d)
 out=validate_bridge(p,r,s,m,b,case.d)
 log('B5_question_requirements_blocked','material blocking explicit requirements prevent delivery',dict(delivery_errors=err(fs),delivery_ready=result['computed_delivery_ready'],bridge=out))
 s['lane']='mixed'
 fs,result=__import__('validate_delivery').validate(s,m,case.d)
 log('C5_mixed_lane_control','same obligations block mixed lane',dict(errors=err(fs),delivery_ready=result['computed_delivery_ready']))
finally:case.tearDown()
args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
