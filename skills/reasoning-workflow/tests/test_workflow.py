import json,unittest,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from routing_core import route_task,recheck_profile,route_is_stale
from route_resources import select
from evaluate_run import validate as eval_run
from learning_core import validate_learning_semantics,retrieve
from validate_dual_verification import validate as validate_dual

BASE_PROFILE={'profile_version':1,'lane':'question','depth_class':'light','autonomy_class':'A','reasoning_breadth':'minimal','evidence_depth':'minimal','challenge_depth':'minimal','verification_depth':'minimal','governance_depth':'minimal','frame_uncertainty':'low','freshness':'stable','causal_or_systemic_complexity':'low','task_coupling':'low','persistence':'none','external_side_effects':'none','routing_confidence':'high','recheck_triggers':[],'task_modes':[],'active_gap_tags':[]}
class WorkflowTests(unittest.TestCase):
 def test_simple_task_stays_light(self):
  r=route_task(BASE_PROFILE);self.assertEqual(r['required_families'],['core-reasoning']);self.assertEqual(r['verification_mode'],'minimal');self.assertEqual(r['runtime_level'],'none');self.assertEqual(r['swarm_admission'],'forbidden')
 def test_deep_research_route(self):
  p={**BASE_PROFILE,'depth_class':'deep','evidence_depth':'deep','frame_uncertainty':'high','task_modes':['research'],'active_gap_tags':['evidence-need']};r=route_task(p);self.assertIn('deep-research',r['required_families']);self.assertEqual(r['verification_mode'],'dual')
 def test_max_does_not_load_all_families(self):
  p={**BASE_PROFILE,'depth_class':'max','evidence_depth':'max','task_modes':['research']};r=route_task(p);self.assertNotIn('execution-control',r['required_families']);self.assertNotIn('workflow-learning',r['required_families'])
 def test_underestimate_can_upgrade_and_old_route_stales(self):
  old=route_task(BASE_PROFILE);p=recheck_profile(BASE_PROFILE,['source_conflict']);self.assertEqual(p['profile_version'],2);self.assertEqual(p['depth_class'],'standard');self.assertEqual(p['evidence_depth'],'deep');self.assertTrue(route_is_stale(old,p))
 def test_profile_can_deescalate(self):
  p={**BASE_PROFILE,'profile_version':3,'depth_class':'max'};q=recheck_profile(p,['lower_than_expected_complexity']);self.assertEqual(q['depth_class'],'deep')
 def test_progressive_reference_selection(self):
  idx=json.loads((ROOT/'routing-index.json').read_text());p={**BASE_PROFILE,'depth_class':'deep','evidence_depth':'deep','task_modes':['research'],'active_gap_tags':['evidence-need','provenance']};r=route_task(p);s=select(idx,r,p,p['active_gap_tags']);self.assertLessEqual(len(s),3);self.assertTrue(all(x['family'] in r['required_families'] for x in s))
 def test_related_does_not_cascade(self):
  idx=json.loads((ROOT/'routing-index.json').read_text());p={**BASE_PROFILE,'depth_class':'standard','active_gap_tags':['decomposition']};r=route_task(p);s=select(idx,r,p,p['active_gap_tags']);self.assertEqual([x['reference_id'] for x in s],['reasoning-structure-and-decomposition'])
 def test_orientation_allowed_without_model_with_goal(self):
  case={'task_profile':{**BASE_PROFILE,'depth_class':'deep','evidence_depth':'deep'}};run={'task_profile':case['task_profile'],'route':route_task(case['task_profile']),'events':[{'event':'epistemic_task_identified'},{'event':'orientation_retrieval','orientation_goal':'map terminology'},{'event':'recomposition_checked'},{'event':'independent_review_completed'},{'event':'closure_attempted'}],'final_state':{'recomposition_valid':True}};codes={x['code'] for x in eval_run(case,run)};self.assertNotIn('ORIENTATION_WITHOUT_GOAL',codes)
 def test_evidence_retrieval_needs_need(self):
  p={**BASE_PROFILE,'depth_class':'deep','evidence_depth':'deep'};case={'task_profile':p};run={'task_profile':p,'route':route_task(p),'events':[{'event':'epistemic_task_identified'},{'event':'evidence_retrieval','problem_model_ref':'PM1'},{'event':'recomposition_checked'},{'event':'independent_review_completed'},{'event':'closure_attempted'}]};codes={x['code'] for x in eval_run(case,run)};self.assertIn('EVIDENCE_RETRIEVAL_WITHOUT_NEED',codes)
 def test_resumed_research_can_use_valid_state_without_create_event(self):
  p={**BASE_PROFILE,'depth_class':'deep','evidence_depth':'deep'};case={'task_profile':p};run={'task_profile':p,'route':route_task(p),'initial_state':{'current_problem_model_ref':'PM1','current_evidence_need_ref':'EN1','recomposition_valid':True},'events':[{'event':'epistemic_task_identified'},{'event':'evidence_retrieval','evidence_need_ref':'EN1','problem_model_ref':'PM1'},{'event':'model_updated'},{'event':'independent_review_completed'},{'event':'closure_attempted'}]};codes={x['code'] for x in eval_run(case,run)};self.assertNotIn('EVIDENCE_NEED_WITHOUT_MODEL',codes);self.assertNotIn('CLOSURE_WITHOUT_RECOMPOSITION',codes)
 def test_unselected_family_reference_rejected(self):
  p=BASE_PROFILE;case={'task_profile':p};r=route_task(p);run={'task_profile':p,'route':r,'events':[{'event':'epistemic_task_identified'},{'event':'reference_loaded','reference_id':'runtime-and-delegation','family':'execution-control','load_reason':'because related','current_gap':'none','profile_version':1},{'event':'closure_attempted'}]};self.assertIn('UNROUTED_FAMILY_REFERENCE',{x['code'] for x in eval_run(case,run)})
 def test_skill_default_cannot_override_user(self):
  p=BASE_PROFILE;run={'task_profile':p,'route':route_task(p),'events':[{'event':'epistemic_task_identified'},{'event':'skill_default_overrode_user_instruction','hard_safety_or_authorization':False},{'event':'closure_attempted'}]};self.assertIn('SKILL_OVERRIDE_USER',{x['code'] for x in eval_run({'task_profile':p},run)})
 def test_dual_review_rejects_same_context(self):
  d={'verification_id':'V','mode':'dual','solver_id':'S','solver_context_id':'C','layer1':{'verdict':'pass','verification_refs':['L1']},'layer2':{'reviewer_id':'R','reviewer_context_id':'C','solver_transcript_included':False,'independence_basis':['fresh_context'],'verdict':'pass'},'reconciliation_status':'not_required'};self.assertIn('REVIEW_NOT_FRESH',{x['code'] for x in validate_dual(d,ROOT)})
 def test_orthogonal_review_requires_orthogonal_basis(self):
  d={'verification_id':'V','mode':'dual_orthogonal','solver_id':'S','solver_context_id':'C1','layer1':{'verdict':'pass','verification_refs':['L1']},'layer2':{'reviewer_id':'R','reviewer_context_id':'C2','solver_transcript_included':False,'independence_basis':['fresh_context'],'route_signature':'x','solver_route_signature':'x','verdict':'pass'},'reconciliation_status':'not_required'};self.assertIn('ORTHOGONAL_BASIS_REQUIRED',{x['code'] for x in validate_dual(d,ROOT)})
 def test_intrinsic_reflection_cannot_promote(self):
  r={'tier':1,'status':'promoted','provenance':{'intrinsic_reflection_only':True}};self.assertIn('INTRINSIC_REFLECTION_NOT_VALIDATION',{x['code'] for x in validate_learning_semantics(r)})
 def test_tier3_needs_rollback_and_eval(self):
  r={'tier':3,'status':'promoted','provenance':{'intrinsic_reflection_only':False},'rollback_ref':'','regression_refs':[],'baseline_comparison_ref':None,'dual_review_ref':None};self.assertIn('CANONICAL_PROMOTION_GATE',{x['code'] for x in validate_learning_semantics(r)})
 def test_stale_learning_not_retrieved(self):
  r={'learning_id':'L','tier':1,'status':'stale','task_signature':['research'],'applicability_conditions':[],'anti_conditions':[],'usage':{'helped':10,'harmed':0}};self.assertEqual(retrieve([r],['research'],[],3),[])
if __name__=='__main__':unittest.main()
