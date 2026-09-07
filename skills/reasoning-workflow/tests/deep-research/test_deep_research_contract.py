import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class DeepResearch(unittest.TestCase):
 def test_required_categories_present(self):
  d=json.loads((ROOT/'tests'/'deep-research'/'eval-task-categories.json').read_text());self.assertGreaterEqual(len(d['categories']),12)
 def test_metrics_not_universal_score(self):
  m=json.loads((ROOT/'evals'/'deep-research'/'metrics.json').read_text());self.assertIn('citation_accuracy',m['metrics']);self.assertNotIn('universal_score',m['metrics'])
