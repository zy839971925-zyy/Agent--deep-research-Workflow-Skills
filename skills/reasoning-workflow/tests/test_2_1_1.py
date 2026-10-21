#!/usr/bin/env python3
"""2.1.1 deterministic boundary tests, paired with the unchanged 2.1 suite."""
from pathlib import Path
import copy,hashlib,json,sys,unittest,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from run_regression import Regression,load,err
import runtime_core as rt
from validate_workflow import fingerprint,validate_bridge
from validate_delivery import validate as delivery
from learning_core import admit_record,retrieve,file_evidence_resolver,learning_subject_fingerprint
from routing_core import route_task,recheck_profile
from route_resources import select
from prepare_task import prepare

class PatchRegression(unittest.TestCase):
 setUp=Regression.setUp
 tearDown=Regression.tearDown
 cli=Regression.cli
 save=Regression.save
 baseline=Regression.baseline
 bridge=Regression.bridge
 def relation_case(self):
  p,r,s,m,b=self.bridge()
  s['observations']=[{'id':'o1','record_type':'observation','declared_status':'current','text':'original'}]
  s['relationships']=[{'id':'rel1','record_type':'relationship','declared_status':'current','relation_type':'causes','epistemic_status':'inferred','from_ref':'o1','to_ref':'e1'}]
  s['answers'][0]['depends_on'].append('rel1')
  for entry in b['reviews']:
   entry['target_fingerprint']=fingerprint(s,entry['target_refs'])
   for v in s['verification']:
    if v['id']==entry['record']['verification_id']:v['metadata']['target_fingerprint']=entry['target_fingerprint']
  return p,r,s,m,b
 def test_40_relationship_from_mutation_invalidates(self):
  p,r,s,m,b=self.relation_case();self.assertTrue(validate_bridge(p,r,s,m,b,self.d)['passed'])
  s['observations'][0]['text']='opposite';self.assertFalse(validate_bridge(p,r,s,m,b,self.d)['passed'])
 def test_41_relationship_to_mutation_invalidates(self):
  p,r,s,m,b=self.relation_case();before=fingerprint(s,['a1']);s['evidence'][0]['text']='changed'
  self.assertNotEqual(before,fingerprint(s,['a1']))
 def test_42_transitive_cycle_terminates_and_tracks(self):
  p,r,s,m,b=self.relation_case();s['observations'][0]['depends_on']=['rel1']
  before=fingerprint(s,['a1']);s['observations'][0]['text']='changed';self.assertNotEqual(before,fingerprint(s,['a1']))
 def test_43_missing_dependency_fails_closed(self):
  p,r,s,m,b=self.relation_case();s['relationships'][0]['from_ref']='missing'
  with self.assertRaisesRegex(ValueError,'unknown target/dependency'):fingerprint(s,['a1'])
 def test_44_duplicate_registry_fails_closed(self):
  p,r,s,m,b=self.relation_case();s['observations'][0]['id']='e1'
  with self.assertRaisesRegex(ValueError,'invalid canonical registry'):fingerprint(s,['a1'])
 def blocked(self,lane='question'):
  s,m=self.baseline();s['lane']=lane;s['declared_status']='blocked'
  for col in ('requirements','acceptance_criteria'):
   s[col][0].update(declared_status='blocked',closure_effect='blocking');m[col][0]['declared_status']='blocked'
  return s,m
 def test_45_question_hard_obligation_blocks(self):
  s,m=self.blocked();fs,out=delivery(s,m,self.d);self.assertFalse(out['computed_delivery_ready']);self.assertIn('DELIVERY_CLOSURE_BLOCKED',err(fs))
  self.cli('validate_delivery.py',[s,m],['--root',self.d,'--json'],expect=1)
 def test_46_all_lanes_same_hard_obligation(self):
  for lane in ('question','action','mixed'):
   s,m=self.blocked(lane);self.assertFalse(delivery(s,m,self.d)[1]['computed_delivery_ready'])
 def test_47_closed_question_cannot_hide_runtime_obligation(self):
  s,m=self.blocked();s['declared_status']='closed'
  self.assertIn('RUNTIME_CLOSURE_BLOCKED',err(delivery(s,m,self.d)[0]))
 def partial(self):
  s,m=self.blocked();m.update(delivery_kind='partial',declared_delivery_ready=False,remaining_work='Await the missing required input; answer.txt is only an interim result.',remaining_obligation_refs=['req1','acc1']);return s,m
 def test_48_partial_handoff_never_complete(self):
  s,m=self.partial();fs,out=delivery(s,m,self.d);self.assertFalse(err(fs),err(fs));self.assertTrue(out['computed_partial_ready']);self.assertFalse(out['computed_delivery_ready']);self.assertFalse(out['computed_task_complete'])
  self.cli('validate_delivery.py',[s,m],['--root',self.d,'--json'])
 def test_49_partial_omission_rejected(self):
  s,m=self.partial();m['remaining_obligation_refs']=['req1'];self.assertIn('PARTIAL_OMITTED_OBLIGATION',err(delivery(s,m,self.d)[0]))
 def test_50_partial_ready_claim_rejected(self):
  s,m=self.partial();m['declared_delivery_ready']=True;self.assertTrue(err(delivery(s,m,self.d)[0]))
 def schedule(self,forbidden=True):
  x=load('legal_parallel_independent_input.json')
  if forbidden:
   for n in x['plan']['nodes']:n['parallel_policy']='forbidden';n['node_contract_hash']=rt.compute_node_contract_hash(n)
   for a,n in zip(x['schedule']['assignments'],x['plan']['nodes']):a['node_contract_hash']=n['node_contract_hash']
  return x
 def test_51_forbidden_without_group_rejected(self):
  x=self.schedule();self.assertIn('PARALLEL_FORBIDDEN',err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
  self.cli('validate_runtime.py',flags=['--plan',self.save('plan',x['plan']),'--schedule',self.save('schedule',x['schedule'])],expect=1)
 def test_52_different_groups_not_isolation(self):
  x=self.schedule()
  for a in x['schedule']['assignments']:a['concurrency_group']=a['node_id']
  self.assertIn('PARALLEL_FORBIDDEN',err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
 def test_53_forbidden_sequenced_hybrid_legal(self):
  x=self.schedule();x['schedule']['mode']='hybrid';x['schedule']['assignments'][1]['starts_after']=['A']
  self.assertFalse(err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
 def test_54_forbidden_serial_and_allowed_parallel_controls(self):
  x=self.schedule();x['schedule']['mode']='serial';self.assertFalse(err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
  x=self.schedule(False);self.assertFalse(err(rt.validate_schedule(x['plan'],x['schedule'],ROOT)))
 def ultra(self):
  p=load('standard_profile.json');p.update(requested_depth='ultra',active_gap_tags=[]);return recheck_profile(p,[])
 def test_55_ultra_untagged_method_required(self):
  p=self.ultra();r=route_task(p);index=json.loads((ROOT/'routing-index.json').read_text());selected=select(index,r,p,[])
  self.assertIn('ultra-research',[x['reference_id'] for x in selected]);self.assertIn('ultra-research',r['required_reference_ids'])
 def test_56_ultra_missing_method_fails_closed(self):
  p=self.ultra();index=json.loads((ROOT/'routing-index.json').read_text());index['references']=[x for x in index['references'] if x['id']!='ultra-research']
  with self.assertRaisesRegex(ValueError,'UNSUPPORTED_REQUIRED_REFERENCE'):select(index,route_task(p,index),p,[])
 def test_57_prepare_profile_route_resources_cli(self):
  p=load('standard_profile.json');out=self.cli('prepare_task.py',[p],['--signal','ultra_requested']);self.assertEqual(out['task_profile']['requested_depth'],'ultra');self.assertFalse(out['authority_granted']);self.assertFalse(out['task_executed'])
  self.assertIn('ultra-research',[x['reference_id'] for x in out['selected_references']])
 def test_58_prepare_light_stays_light(self):
  p=load('standard_profile.json');p.update(depth_class='light',evidence_depth='minimal',verification_depth='minimal',active_gap_tags=[])
  # use exact passing light control from the original suite
  p.update(task_modes=[],frame_uncertainty='low',causal_or_systemic_complexity='low')
  out=prepare(p);self.assertTrue(out['passed'],out);self.assertEqual(out['selected_references'],[])
 def test_59_prepare_missing_file_blocked_no_downgrade(self):
  root=self.d/'package';shutil.copytree(ROOT/'schemas',root/'schemas');shutil.copy2(ROOT/'routing-index.json',root/'routing-index.json')
  out=prepare(self.ultra(),root=root);self.assertFalse(out['passed']);self.assertEqual(out['status'],'blocked');self.assertEqual(out['task_profile']['depth_class'],'ultra')
 def test_60_pending_gap_resources_visible(self):
  p=self.ultra();p['active_gap_tags']=['ultra','delegation','recovery','orthogonal-verification'];out=prepare(p)
  self.assertTrue(out['passed']);self.assertIn('synchronization-and-recovery',{x['reference_id'] for x in out['selected_references']+out['deferred_references']})
 def promoted(self):
  q=load('learning_intrinsic_flag_false.json');q.update(tier=3,status='promoted',source_eval_refs=['eval'],regression_refs=['reg'],held_out_eval_refs=['held'],baseline_comparison_ref='baseline',dual_review_ref='review',rollback_ref='rollback');q['provenance']={'feedback_types':['deterministic_verifier'],'intrinsic_reflection_only':False}
  (self.d/'receipt.txt').write_text('Synthetic host-curated evidence fixture; not an actual model evaluation.')
  h=hashlib.sha256((self.d/'receipt.txt').read_bytes()).hexdigest();index={'eval':{'verdict':'pass','kind':'deterministic_test','path':'receipt.txt','sha256':h}}
  for ref,role,kind in [('reg','regression','deterministic_test'),('held','held_out','external_evaluation'),('baseline','baseline','baseline_comparison'),('review','dual_review','independent_review'),('rollback','rollback','rollback_plan')]:
   index[ref]={'verdict':'pass','kind':kind,'path':'receipt.txt','sha256':h,'roles':[role],'learning_ids':[q['learning_id']],'current':True,'subject_sha256':learning_subject_fingerprint(q),'independence_verified':True}
  return q,index
 def resolver(self,index):return file_evidence_resolver(self.save('index',index))
 def test_61_unresolved_gate_rejected_with_good_source(self):
  q,index=self.promoted();del index['held'];self.assertTrue(admit_record(q,ROOT,self.resolver(index)))
  self.cli('validate_learning.py',[q],['--validation-evidence',self.save('index',index)],expect=1)
 def test_62_all_typed_scoped_gates_pass(self):
  q,index=self.promoted();resolver=self.resolver(index);self.assertFalse(admit_record(q,ROOT,resolver));self.assertFalse(retrieve([q],['deep_research'],[],validation_resolver=resolver));self.assertEqual(len(retrieve([q],['deep_research'],[],maintenance=True,validation_resolver=resolver)),1)
  self.cli('validate_learning.py',[q],['--validation-evidence',self.save('index',index)])
  out=self.cli('retrieve_learnings.py',[[q]],['--task-tag','deep_research','--maintenance','--validation-evidence',self.save('index',index)]);self.assertTrue(out['advisory_only'])
 def test_63_wrong_type_scope_verdict_stale_gate_rejected(self):
  for field,value in [('kind','external_observation'),('learning_ids',['other']),('current',False),('verdict','fail'),('roles',['wrong']),('subject_sha256','0'*64)]:
   q,index=self.promoted();index['reg'][field]=value;self.assertTrue(admit_record(q,ROOT,self.resolver(index)),field)
 def test_64_changed_heuristic_invalidates_promotion_evidence(self):
  q,index=self.promoted();q['heuristic']='Entirely different lesson';self.assertTrue(admit_record(q,ROOT,self.resolver(index)))
 def test_65_boolean_only_resolver_cannot_grant_promotion(self):
  q,index=self.promoted();self.assertTrue(admit_record(q,ROOT,lambda ref:True))
 def test_66_review_independence_and_file_bytes_required(self):
  q,index=self.promoted();index['review']['independence_verified']=False;self.assertTrue(admit_record(q,ROOT,self.resolver(index)))
  q,index=self.promoted();(self.d/'receipt.txt').write_text('Changed');self.assertTrue(admit_record(q,ROOT,self.resolver(index)))

 def test_67_ultra_cannot_be_erased_by_forged_light_route(self):
  p=self.ultra();r=route_task(p);r['required_families']=['core-reasoning'];r['reference_phase_limit']=0;r['required_reference_ids']=[]
  with self.assertRaisesRegex(ValueError,'ROUTE_REQUIREMENTS_MISMATCH'):select(json.loads((ROOT/'routing-index.json').read_text()),r,p,[])
 def test_68_partial_no_closed_state_or_unknown_ref(self):
  s,m=self.partial();s['declared_status']='closed';self.assertIn('PARTIAL_FALSE_COMPLETION',err(delivery(s,m,self.d)[0]))
  s,m=self.partial();m['remaining_obligation_refs'].append('missing');self.assertIn('PARTIAL_UNKNOWN_OBLIGATION',err(delivery(s,m,self.d)[0]))
 def test_69_tier2_heldout_requires_evidence(self):
  q,index=self.promoted();q['tier']=2
  self.assertTrue(admit_record(q,ROOT,self.resolver(index)))
  index['held']['subject_sha256']=learning_subject_fingerprint(q)
  self.assertFalse(admit_record(q,ROOT,self.resolver(index)))

if __name__=='__main__':unittest.main(verbosity=2)
