#!/usr/bin/env python3
"""Portable real-code regression suite, all inputs synthetic. No business side effects."""
from pathlib import Path
import sys,json,tempfile,subprocess,copy,hashlib,unittest,datetime,shutil
ROOT=Path(__file__).resolve().parents[1]; FIX=ROOT/'tests/fixtures'
sys.path.insert(0,str(ROOT/'scripts'))
import jsonschema
import runtime_core as rt
from routing_core import route_task,recheck_profile
from route_resources import select
from validate_delivery import validate as delivery
from validate_workflow import validate_bridge,fingerprint
from validate_dual_verification import validate as review_valid,verification_passed
from learning_core import admit_record,retrieve,file_evidence_resolver
from host_adapter import verify_submission_context
RECEIPTS=[]
def load(name):return json.loads((FIX/name).read_text())
def err(fs):return [f.code for f in fs if f.severity=='ERROR']
class Regression(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def cli(self,script,inputs=(),flags=(),expect=0):
  paths=[]
  for i,obj in enumerate(inputs):
   p=self.d/f'input{i}.json';p.write_text(json.dumps(obj));paths.append(str(p))
  cmd=[sys.executable,str(ROOT/'scripts'/script),*paths,*map(str,flags)]
  if script=='validate_runtime.py':cmd.append('--json')
  p=subprocess.run(cmd,cwd=self.d,text=True,capture_output=True)
  RECEIPTS.append({'test':self.id(),'argv':cmd,'cwd':'temporary directory outside Skill','exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
  self.assertEqual(p.returncode,expect,p.stdout+p.stderr)
  if p.stdout.strip():return json.loads(p.stdout)
 def test_01_explicit_ultra(self):
  p=load('standard_profile.json')
  for depth in ('light','standard','deep','max','ultra'):
   p['depth_class']=depth
   out=recheck_profile(p,['ultra_requested','lower_than_expected_complexity'])
   # API returns profile directly.
   self.assertEqual(out['depth_class'],'ultra')
 def test_02_route_cli_and_cwd(self):
  out=self.cli('route_task.py',[load('standard_profile.json')],['--signal','ultra_requested'])
  self.assertIn('ultra',json.dumps(out))
 def test_03_routing_mandatory_families(self):
  index=json.loads((ROOT/'routing-index.json').read_text())
  for name in ('ultra_delegated_profile.json','R2-orthogonal-gap-missing-family_profile.json','R4-light-high-consequence-reference-filter_profile.json','R4-light-action-governance-reference-filter_profile.json'):
   p=load(name);r=route_task(p);selected=select(index,r,p,[])
   families={x['family'] for x in selected}
   self.assertTrue(set(r['required_families'])<=families,(name,r,selected))
 def test_04_short_light_no_reference_ritual(self):
  p=load('standard_profile.json');p.update(depth_class='light',task_modes=['explain'],task_coupling='high')
  r=route_task(p);self.assertEqual(select(json.loads((ROOT/'routing-index.json').read_text()),r,p,[]),[])
 def test_05_strict_raw_envelope(self):
  self.cli('validate_raw.py',[{}],['--json'],1)
  self.cli('validate_raw.py',[{'recrods':[{}]}],['--json'],1)
  self.cli('validate_raw.py',[[]],['--json'])
 def test_06_raw_hash_and_lineage_schema(self):
  raw={'schema_version':'2.0','raw_id':'R1','record_kind':'raw','source_type':'synthetic_fixture','source_locator':'fixture:test','observed_at':'2026-10-21T00:00:00Z','local_path':'raw.txt'}
  (self.d/'raw.txt').write_text('synthetic original')
  raw['content_hash']=hashlib.sha256((self.d/'raw.txt').read_bytes()).hexdigest();raw['hash_algorithm']='sha256'
  self.cli('validate_raw.py',[[raw]],['--root',self.d,'--json'])
  raw['hash_algorithm']=None;self.cli('validate_raw.py',[[raw]],['--root',self.d,'--json'],1)
  raw['hash_algorithm']='sha256';raw['content_hash']='bogus';self.cli('validate_raw.py',[[raw]],['--root',self.d,'--json'],1)
  raw.pop('local_path');raw.pop('content_hash');raw.pop('hash_algorithm')
  child=copy.deepcopy(raw);child.update(raw_id='D1',record_kind='derived',transformations=['synthetic transform'])
  self.cli('validate_raw.py',[[raw,child]],['--json'],1)
  child['derived_from']=[];self.cli('validate_raw.py',[[raw,child]],['--json'],1)
  child['derived_from']=['R1'];self.cli('validate_raw.py',[[raw,child]],['--json'])
 def test_07_runtime_explicit_empty(self):
  x=load('legal_parallel_independent_input.json');plan=x['plan']
  self.cli('validate_runtime.py',flags=['--plan',self.save('plan',plan),'--ledger',self.save('empty',{})],expect=1)
  self.cli('validate_runtime.py',flags=['--plan',self.save('plan',plan),'--schedule',self.save('empty',{})],expect=1)
 def save(self,name,obj):
  p=self.d/(name+'.json');p.write_text(json.dumps(obj));return p
 def test_08_schedule_legal_and_cycles(self):
  x=load('legal_parallel_independent_input.json')
  self.assertFalse(err(rt.validate_plan(x['plan'],ROOT)))
  self.assertFalse(err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
  self.cli('validate_runtime.py',flags=['--plan',self.save('plan',x['plan']),'--schedule',self.save('sch',x['schedule'])])
  for name in ('parallel_self_cycle_input.json','parallel_two_cycle_input.json','hybrid_two_cycle_input.json','mixed_plan_schedule_cycle_input.json'):
   x=load(name);fs=rt.validate_schedule(x['plan'],x['schedule'],ROOT)
   self.assertIn('SCHEDULE_WAIT_CYCLE',err(fs),name)
   self.cli('validate_runtime.py',flags=['--plan',self.save('plan',x['plan']),'--schedule',self.save('sch',x['schedule'])],expect=1)
 def test_09_resume_terminal_and_versions(self):
  x=load('resume_safe_cancelled_input.json')
  for status in ('cancelled','verified_complete','failed'):
   x['ledger']['nodes'][0]['effective_status']=status
   self.assertEqual(rt.compute_resume_actions(x['plan'],x['ledger'],x['checkpoint'])[0]['resume_action'],'blocked_terminal_state')
  x['ledger']['nodes'][0]['effective_status']='running'
  self.assertEqual(rt.compute_resume_actions(x['plan'],x['ledger'],x['checkpoint'])[0]['resume_action'],'reconcile_required')
  x['checkpoint']['state_version']=x['ledger']['state_version']
  self.assertEqual(rt.compute_resume_actions(x['plan'],x['ledger'],x['checkpoint'])[0]['resume_action'],'rerun_allowed')
  x['plan']['nodes'][0]['side_effect_class']='irreversible'
  self.assertNotEqual(rt.compute_resume_actions(x['plan'],x['ledger'],x['checkpoint'])[0]['resume_action'],'rerun_allowed')
 def test_10_replay_missing_fails_closed(self):
  p=load('legal_parallel_independent_input.json')['plan'];n=p['nodes'][0];n['side_effect_class']='irreversible';n.pop('replay_safety',None);n['node_contract_hash']=rt.compute_node_contract_hash(n)
  self.assertIn('REPLAY_SAFETY_SUSPICIOUS',err(rt.validate_plan(p,ROOT)))
 def proposal(self):
  x=load('resume_safe_cancelled_input.json');p=x['plan'];n=p['nodes'][0];n['write_set']=['observations'];n['node_contract_hash']=rt.compute_node_contract_hash(n)
  q={'schema_version':'1.1','proposal_id':'p1','node_id':n['node_id'],'plan_version':p['plan_version'],'node_contract_hash':n['node_contract_hash'],'attempt_id':'a1','executor_id':'worker1','input_state_version':2,'input_refs':[],'evidence_refs':[],'output_refs':[],'proposed_state_patch':{'observations':[]},'read_set_observed':[],'write_set_proposed':['observations'],'result_fingerprint':'sha256:'+'0'*64,'declared_status':'proposed_complete'}
  return p,q
 def test_11_patch_actual_scope(self):
  p,q=self.proposal();self.assertFalse(err(rt.validate_worker_proposal(p,q,ROOT,2)))
  q['proposed_state_patch']={'decisions':[]}
  self.assertIn('WORKER_WRITE_SCOPE',err(rt.validate_worker_proposal(p,q,ROOT,2)))
  q['write_set_proposed']=[]
  self.assertIn('WORKER_PATCH_DECLARATION',err(rt.validate_worker_proposal(p,q,ROOT,2)))
 def test_12_patch_host_and_conflict(self):
  p,q=self.proposal()
  fs,r=rt.classify_worker_proposals(p,[q],ROOT,2);self.assertFalse(r['mergeable'])
  fs,r=rt.classify_worker_proposals(p,[q],ROOT,2,lambda *args:True);self.assertEqual(r['mergeable'],['p1'])
  q2=copy.deepcopy(q);q2['proposal_id']='p2'
  fs,r=rt.classify_worker_proposals(p,[q,q2],ROOT,2,lambda *args:True);self.assertFalse(r['mergeable']);self.assertEqual(set(r['conflicting']),{'p1','p2'})
 def test_13_host_context(self):
  p,q=self.proposal();e={'node_id':'N','effective_status':'running','executor_id':'worker1','active_attempt_id':'a1','node_contract_hash':q['node_contract_hash'],'lease_id':'lease1','lease_expires_at':'2026-10-21T12:00:00Z'}
  ledger={'plan_id':p['plan_id'],'plan_version':p['plan_version'],'state_version':2,'nodes':[e]};now=datetime.datetime(2026,10,21,11,tzinfo=datetime.timezone.utc)
  call=lambda:verify_submission_context(p,q,ledger,'worker1',now,lambda *args:True)
  self.assertTrue(call()[0],call());e['active_attempt_id']='old';self.assertFalse(call()[0]);e['active_attempt_id']='a1';e['effective_status']='cancelled';self.assertFalse(call()[0]);e['effective_status']='running';e['lease_expires_at']='2020-01-01T00:00:00Z';self.assertFalse(call()[0])
 def baseline(self):
  s=load('baseline_state.json');m=load('baseline_manifest.json');shutil.copy2(FIX/'answer.txt',self.d/'answer.txt');shutil.copy2(FIX/'old_answer.txt',self.d/'old_answer.txt');return s,m
 def test_14_delivery_identity_and_refs(self):
  s,m=self.baseline();fs,result=delivery(s,m,self.d);self.assertFalse(err(fs),(err(fs),result));self.assertTrue(result['computed_delivery_ready'])
  m['artifacts'][0]['path']='old_answer.txt';self.assertIn('ART_IDENTITY_MISMATCH',err(delivery(s,m,self.d)[0]))
 def test_15_delivery_acceptance_refs(self):
  s,m=self.baseline();m['acceptance_criteria'][0]['artifact_refs']=['e1'];self.assertTrue(err(delivery(s,m,self.d)[0]))
 def test_16_old_unaffected_basis_legal(self):
  s,m=self.baseline();s['artifacts'][0]['based_on_state_version']=6;m['artifacts'][0]['based_on_state_version']=6
  self.assertFalse(err(delivery(s,m,self.d)[0]))
 def test_17_review_valid_is_not_passed(self):
  record=load('failed_review_record.json');self.assertFalse(review_valid(record,ROOT));self.assertFalse(verification_passed(record))
  result=self.cli('validate_dual_verification.py',[record]);self.assertTrue(result['record_valid']);self.assertFalse(result['verification_passed'])
 def test_18_learning_intrinsic_rejected(self):
  record=load('learning_intrinsic_flag_false.json');self.assertTrue(admit_record(record,ROOT));self.cli('validate_learning.py',[record],expect=1)
  self.cli('retrieve_learnings.py',[[record]],['--task-tag','deep_research'],expect=1)
 def learning(self):
  r=load('learning_intrinsic_flag_false.json');r['provenance']={'feedback_types':['external_evaluation'],'intrinsic_reflection_only':False};r['source_eval_refs']=['eval1'];return r
 def test_19_learning_tiers_and_evidence(self):
  r=self.learning();schema=json.loads((ROOT/'schemas/learning-record.schema.json').read_text());allowed=schema['properties']['provenance']['properties']['feedback_types']['items']['enum']
  r['provenance']['feedback_types']=[next(x for x in allowed if x!='intrinsic_reflection')]
  self.assertTrue(admit_record(r,ROOT))
  (self.d/'eval.txt').write_text('Synthetic deterministic evaluation: pass')
  index={'eval1':{'path':'eval.txt','sha256':hashlib.sha256((self.d/'eval.txt').read_bytes()).hexdigest(),'verdict':'pass','kind':'deterministic_test'}}
  indexpath=self.save('evidence_index',index);resolver=file_evidence_resolver(indexpath)
  self.assertFalse(admit_record(r,ROOT,resolver));self.assertEqual(len(retrieve([r],['deep_research'],[],validation_resolver=resolver)),1)
  r['tier']=3;self.assertFalse(retrieve([r],['deep_research'],[],validation_resolver=resolver));self.assertEqual(len(retrieve([r],['deep_research'],[],maintenance=True,validation_resolver=resolver)),1)
  self.cli('validate_learning.py',[r],['--validation-evidence',indexpath]);self.cli('retrieve_learnings.py',[[r]],['--task-tag','deep_research','--validation-evidence',indexpath])
 def test_20_learning_malformed(self):
  self.cli('retrieve_learnings.py',[{'recrods':[]}],expect=1)
  self.cli('retrieve_learnings.py',[[{'learning_id':'bad','status':'validated'}]],expect=1)
 def bridge(self):
  s,m=self.baseline();p=load('standard_profile.json');route=route_task(p)
  for i,target in enumerate(('a1','art1')):
   rid='v'+str(i+1);rec={'id':rid,'record_type':'verification','declared_status':'passed','target_refs':[target],'metadata':{},'materiality':'material','closure_effect':'blocking'}
   if i==0:s['verification']=[rec]
   else:s['verification'].append(rec)
   for col in ('answers','artifacts'):
    for row in s.get(col,[]):
     if row['id']==target:row['verification_refs']=[rid]
  h=hashlib.sha256((self.d/'answer.txt').read_bytes()).hexdigest();s['artifacts'][0].setdefault('metadata',{})['content_sha256']=h;m['artifacts'][0]['content_sha256']=h
  b={'schema_version':'1.0','work_id':s['work_id'],'reviews':[]}
  for i,target in enumerate(('a1','art1')):
   rid='v'+str(i+1);fp=fingerprint(s,[target]);s['verification'][i]['metadata']['target_fingerprint']=fp
   record=load('single_review_record.json');record['verification_id']=rid;record['layer1']['verification_refs']=['e1']
   b['reviews'].append({'record':record,'target_refs':[target],'target_fingerprint':fp,'context_exposure':'unknown'})
  return p,route,s,m,b
 def test_21_strict_bridge(self):
  p,r,s,m,b=self.bridge();result=validate_bridge(p,r,s,m,b,self.d);self.assertTrue(result['passed'],result)
  args=[]
  for name,obj in zip(('profile','route','state','manifest','reviews'),(p,r,s,m,b)):args+=['--'+name,self.save(name,obj)]
  self.cli('validate_workflow.py',flags=args+['--root',self.d])
  b['reviews'][0]['record']['layer1']['verdict']='fail';self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
 def test_22_strict_bridge_stale_and_bytes(self):
  p,r,s,m,b=self.bridge();s['answers'][0]['text']='different answer';self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
  p,r,s,m,b=self.bridge();(self.d/'answer.txt').write_text('tampered');self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
 def test_24_external_locks_not_workspace_isolation(self):
  x=load('legal_parallel_independent_input.json')
  for n in x['plan']['nodes']:
   n['resource_locks']=['merchant-order'];n['node_contract_hash']=rt.compute_node_contract_hash(n)
  hashes={n['node_id']:n['node_contract_hash'] for n in x['plan']['nodes']}
  for mode in ('shared','isolated_workspace','transactional'):
   for a in x['schedule']['assignments']:a['node_contract_hash']=hashes[a['node_id']];a['isolation_mode']=mode
   self.assertIn('PARALLEL_STATE_CONFLICT',err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
 def test_25_proposal_cli_no_host_bypass(self):
  p,q=self.proposal();out=self.cli('validate_runtime.py',flags=['--plan',self.save('p',p),'--worker-proposal',self.save('q',q)],expect=1)
  self.assertIn('WORKER_HOST_CONTEXT_REQUIRED',[f['code'] for f in out['findings']])
 def test_26_resource_cli_other_cwd(self):
  p=load('R4-light-high-consequence-reference-filter_profile.json');r=route_task(p)
  out=self.cli('route_resources.py',[p,r]);self.assertIn('audit-verification',{x['family'] for x in out['selected_references']})
 def test_27_artifact_role_binding(self):
  s,m=self.baseline();m['artifacts'][0]['role']='unreviewed-role'
  self.assertIn('ART_IDENTITY_MISMATCH',err(delivery(s,m,self.d)[0]))
 def test_28_unresolved_review_evidence(self):
  p,r,s,m,b=self.bridge();b['reviews'][0]['record']['layer1']['verification_refs']=['missing']
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
 def test_29_host_authority_and_executor(self):
  p,q=self.proposal();e={'node_id':'N','effective_status':'running','executor_id':'worker1','active_attempt_id':'a1','node_contract_hash':q['node_contract_hash'],'lease_id':'lease1','lease_expires_at':'2026-10-21T12:00:00Z'}
  ledger={'plan_id':p['plan_id'],'plan_version':p['plan_version'],'state_version':2,'nodes':[e]};now=datetime.datetime(2026,10,21,11,tzinfo=datetime.timezone.utc)
  self.assertFalse(verify_submission_context(p,q,ledger,'worker1',now,lambda *args:False)[0])
  self.assertFalse(verify_submission_context(p,q,ledger,'another-worker',now,lambda *args:True)[0])
  e.pop('lease_id');self.assertFalse(verify_submission_context(p,q,ledger,'worker1',now,lambda *args:True)[0])
 def test_30_review_mode_and_route_binding(self):
  p,r,s,m,b=self.bridge();p['depth_class']='ultra';r=route_task(p)
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
  p,r,s,m,b=self.bridge();r['verification_mode']='minimal'
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
 def test_31_implicit_root_proposal_schema(self):
  p,q=self.proposal();q.pop('attempt_id');self.assertTrue(err(rt.validate_worker_proposal(p,q)))
 def test_32_manifest_flag_cannot_skip_digest(self):
  p,r,s,m,b=self.bridge();(self.d/'answer.txt').write_text('tampered bytes')
  m['artifacts'][0]['declared_current']=False
  result=validate_bridge(p,r,s,m,b,self.d);self.assertFalse(result['passed'],result)
  self.assertIn('ART_CURRENT_DOWNGRADE',err(delivery(s,m,self.d)[0]))
  args=[]
  for name,obj in zip(('profile','route','state','manifest','reviews'),(p,r,s,m,b)):args+=['--'+name,self.save(name,obj)]
  self.cli('validate_workflow.py',flags=args+['--root',self.d],expect=1)
 def test_33_historical_optional_artifact_control(self):
  p,r,s,m,b=self.bridge()
  s['artifacts'].append({'id':'old1','record_type':'artifact','declared_status':'historical','path':'old_answer.txt','based_on_state_version':1,'role':'history','materiality':'supporting'})
  m['artifacts'].append({'id':'old1','path':'old_answer.txt','based_on_state_version':1,'role':'history','declared_current':False})
  result=validate_bridge(p,r,s,m,b,self.d);self.assertTrue(result['passed'],result)
 def test_34_explicit_depth_api_cli_consistency(self):
  p=load('standard_profile.json');original=copy.deepcopy(p);p['requested_depth']='ultra'
  normalized=recheck_profile(p,[]);api=route_task(p)
  self.assertEqual(normalized['depth_class'],'ultra');self.assertEqual(normalized['profile_version'],p['profile_version']+1)
  self.assertEqual(api['verification_mode'],'dual');self.assertEqual(api,route_task(normalized))
  self.assertEqual(p['depth_class'],'standard');self.assertEqual(normalized['autonomy_class'],original['autonomy_class'])
  out=self.cli('route_task.py',[p]);self.assertEqual(out['route'],api);self.assertEqual(out['task_profile'],normalized)
  self.assertEqual(route_task(original)['verification_mode'],'single')
 def test_35_bridge_refuses_unnormalized_explicit_depth(self):
  p,r,s,m,b=self.bridge();p['requested_depth']='ultra';r=route_task(p)
  result=validate_bridge(p,r,s,m,b,self.d);self.assertFalse(result['passed'],result)
  self.assertIn('PROFILE_RECHECK_REQUIRED',' '.join(result['errors']))
  args=[]
  for name,obj in zip(('profile','route','state','manifest','reviews'),(p,r,s,m,b)):args+=['--'+name,self.save(name,obj)]
  self.cli('validate_workflow.py',flags=args+['--root',self.d],expect=1)
  p=recheck_profile(p,[]);r=route_task(p)
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed']) # single cannot satisfy Ultra
  index=json.loads((ROOT/'routing-index.json').read_text())
  bad=load('standard_profile.json');bad['requested_depth']='ultra'
  with self.assertRaisesRegex(ValueError,'PROFILE_RECHECK_REQUIRED'):select(index,route_task(bad),bad,[])
 def orthogonal_bridge(self):
  p,r,s,m,b=self.bridge();p['high_consequence']=True;r=route_task(p)
  for entry in b['reviews']:
   rec=entry['record'];rid=rec['verification_id'];rec['mode']='dual_orthogonal'
   rec['layer1']['verification_refs']=['check1_'+rid]
   rec['layer2']={'reviewer_id':'synthetic-reviewer','reviewer_context_id':'synthetic-fresh-context','solver_transcript_included':False,'independence_basis':['orthogonal_tool'],'verification_refs':['check2_'+rid],'verdict':'pass'}
   entry['independence_evidence_refs']=['e1']
   for ref in rec['layer1']['verification_refs']+rec['layer2']['verification_refs']:
    s['verification'].append({'id':ref,'record_type':'verification','declared_status':'passed','target_refs':entry['target_refs'],'metadata':{'target_fingerprint':entry['target_fingerprint']}})
  return p,r,s,m,b
 def synthetic_review_verifier(self,entry,state):
  # Synthetic trusted-host fixture, NOT a production authenticator/eval result.
  rec=entry['record']
  return {'verification_id':rec['verification_id'],'target_fingerprint':entry['target_fingerprint'],'layer1_verification_refs':rec['layer1']['verification_refs'],'layer2_verification_refs':rec['layer2']['verification_refs'],'evidence_authenticated':True,'orthogonality_verified':True}
 def test_36_no_self_reported_orthogonal_credit(self):
  p,r,s,m,b=self.orthogonal_bridge()
  for entry in b['reviews']:
   entry['record']['layer1']['verification_refs']=[];entry['record']['layer2']['verification_refs']=[]
  out=validate_bridge(p,r,s,m,b,self.d);self.assertFalse(out['passed']);self.assertFalse(out['orthogonality_verified']);self.assertFalse(out['evidence_authenticated'])
  out=validate_bridge(p,r,s,m,b,self.d,self.synthetic_review_verifier);self.assertFalse(out['orthogonality_verified'])
 def test_37_trusted_bound_review_receipt_control(self):
  p,r,s,m,b=self.orthogonal_bridge()
  out=validate_bridge(p,r,s,m,b,self.d);self.assertTrue(out['structural_valid'],out);self.assertFalse(out['passed']);self.assertFalse(out['orthogonality_verified'])
  out=validate_bridge(p,r,s,m,b,self.d,self.synthetic_review_verifier);self.assertTrue(out['passed'],out);self.assertTrue(out['evidence_authenticated']);self.assertTrue(out['orthogonality_verified'])
  def stale_receipt(entry,state):
   value=self.synthetic_review_verifier(entry,state);value['target_fingerprint']='sha256:'+'0'*64;return value
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d,stale_receipt)['passed'])
  b['reviews'][0]['record']['layer2']['verification_refs']=['e1']
  self.assertFalse(validate_bridge(p,r,s,m,b,self.d,self.synthetic_review_verifier)['passed'])
 def test_38_orthogonal_cli_without_host_receipt(self):
  p,r,s,m,b=self.orthogonal_bridge();args=[]
  for name,obj in zip(('profile','route','state','manifest','reviews'),(p,r,s,m,b)):args+=['--'+name,self.save(name,obj)]
  out=self.cli('validate_workflow.py',flags=args+['--root',self.d],expect=1)
  self.assertTrue(out['structural_valid']);self.assertFalse(out['evidence_authenticated']);self.assertFalse(out['orthogonality_verified'])
  p,r,s,m,b=self.bridge();out=validate_bridge(p,r,s,m,b,self.d)
  self.assertTrue(out['passed']);self.assertFalse(out['evidence_authenticated']);self.assertIsNone(out['orthogonality_verified'])
 def test_39_cross_task_protocol_integrity(self):
  data=json.loads((ROOT/'evals/cross_task_cases.json').read_text())
  self.assertEqual(data['status'],'protocol_only_not_model_evaluated')
  self.assertEqual(len(data['cases']),6);self.assertEqual(len({c['id'] for c in data['cases']}),6)
  self.assertTrue(all(c['task'] and c['acceptance'] and c['forbidden'] for c in data['cases']))
 def test_23_all_schema_metas_valid(self):
  for path in (ROOT/'schemas').glob('*.json'):jsonschema.Draft202012Validator.check_schema(json.loads(path.read_text()))
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Regression);result=unittest.TextTestRunner(verbosity=2).run(suite)
 out=ROOT/'tests/results';out.mkdir(exist_ok=True)
 (out/'cli_receipts.json').write_text(json.dumps(RECEIPTS,indent=2))
 summary={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'real_cli_invocations':len(RECEIPTS),'jsonschema':__import__('importlib.metadata',fromlist=['version']).version('jsonschema'),'python':sys.version,'model_evaluated':False,'business_actions_executed':False}
 (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary));sys.exit(0 if result.wasSuccessful() else 1)
