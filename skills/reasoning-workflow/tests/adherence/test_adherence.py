import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from evaluate_run import validate
from routing_core import route_task
P={'profile_version':1,'lane':'question','depth_class':'deep','autonomy_class':'B','reasoning_breadth':'deep','evidence_depth':'deep','challenge_depth':'deep','verification_depth':'deep','governance_depth':'minimal','routing_confidence':'high','task_modes':['research']}
class Adherence(unittest.TestCase):
 def test_orientation_is_not_evidence_retrieval(self):
  run={'task_profile':P,'route':route_task(P),'events':[{'event':'epistemic_task_identified'},{'event':'orientation_retrieval','orientation_goal':'map frame'}]};self.assertNotIn('EVIDENCE_RETRIEVAL_WITHOUT_NEED',{x['code'] for x in validate({'task_profile':P},run)})
 def test_evidence_precondition(self):
  run={'task_profile':P,'route':route_task(P),'events':[{'event':'epistemic_task_identified'},{'event':'evidence_retrieval','problem_model_ref':'PM'}]};self.assertIn('EVIDENCE_RETRIEVAL_WITHOUT_NEED',{x['code'] for x in validate({'task_profile':P},run)})
