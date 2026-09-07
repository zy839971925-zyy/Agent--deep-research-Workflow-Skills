import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from learning_core import validate_learning_semantics,retrieve
class Learning(unittest.TestCase):
 def test_reflection_candidate_only(self):self.assertTrue(validate_learning_semantics({'tier':1,'status':'promoted','provenance':{'intrinsic_reflection_only':True}}))
 def test_deprecated_not_retrieved(self):self.assertEqual(retrieve([{'learning_id':'x','status':'deprecated','task_signature':['x']}],['x'],[],3),[])
