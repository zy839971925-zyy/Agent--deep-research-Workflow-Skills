import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from routing_core import route_task,recheck_profile,route_is_stale
B={'profile_version':1,'lane':'question','depth_class':'light','autonomy_class':'A','reasoning_breadth':'minimal','evidence_depth':'minimal','challenge_depth':'minimal','verification_depth':'minimal','governance_depth':'minimal','routing_confidence':'high'}
class Routing(unittest.TestCase):
 def test_negative_control(self):
  r=route_task(B);self.assertEqual(r['required_families'],['core-reasoning']);self.assertEqual(r['runtime_level'],'none')
 def test_dynamic_update_stales_route(self):
  r=route_task(B);p=recheck_profile(B,['hidden_complexity']);self.assertTrue(route_is_stale(r,p))
