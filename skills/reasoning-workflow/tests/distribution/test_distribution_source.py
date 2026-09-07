import unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class Distribution(unittest.TestCase):
 def test_six_families(self):self.assertEqual(len(json.loads((ROOT/'routing-index.json').read_text())['families']),6)
 def test_builder_exists(self):self.assertTrue((ROOT/'scripts'/'build_distributions.py').is_file())
