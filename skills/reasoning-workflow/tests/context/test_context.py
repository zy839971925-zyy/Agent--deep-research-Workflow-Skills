import unittest,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from route_resources import select
from routing_core import route_task
class Context(unittest.TestCase):
 def test_light_no_gap_loads_no_reference(self):
  p={'profile_version':1,'lane':'question','depth_class':'light','autonomy_class':'A','reasoning_breadth':'minimal','evidence_depth':'minimal','challenge_depth':'minimal','verification_depth':'minimal','governance_depth':'minimal','routing_confidence':'high','active_gap_tags':[]};idx=json.loads((ROOT/'routing-index.json').read_text());self.assertEqual(select(idx,route_task(p),p,[]),[])
 def test_phase_budget(self):
  p={'profile_version':1,'lane':'question','depth_class':'max','autonomy_class':'B','reasoning_breadth':'max','evidence_depth':'max','challenge_depth':'max','verification_depth':'max','governance_depth':'standard','routing_confidence':'high','task_modes':['research'],'active_gap_tags':['provenance','evidence','retrieval','causal-chain']};idx=json.loads((ROOT/'routing-index.json').read_text());r=route_task(p);self.assertLessEqual(len(select(idx,r,p,p['active_gap_tags'])),r['reference_phase_limit'])
