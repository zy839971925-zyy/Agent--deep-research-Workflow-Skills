from __future__ import annotations
import json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import runtime_core, evaluate_run

class RuntimeFixtures(unittest.TestCase):
    def test_runtime_regression_fixtures(self):
        fixtures=sorted((ROOT/'tests'/'runtime').glob('*.json'))
        self.assertGreaterEqual(len(fixtures),6)
        for path in fixtures:
            with self.subTest(fixture=path.name):
                d=json.loads(path.read_text())
                kind=d['kind']
                if kind=='schedule':
                    fs=runtime_core.validate_schedule(d['plan'],d['schedule'],ROOT)
                    codes={f.code for f in fs}
                elif kind=='capabilities':
                    fs,_=runtime_core.evaluate_capabilities(d['plan'],d['snapshot'],ROOT); codes={f.code for f in fs}
                elif kind=='checkpoint':
                    fs=runtime_core.validate_checkpoint(d['checkpoint'],ROOT,plan=d['plan']); codes={f.code for f in fs}
                elif kind=='worker_merge':
                    fs,_=runtime_core.classify_worker_proposals(d['plan'],d['proposals'],ROOT,d.get('current_state_version')); codes={f.code for f in fs}
                elif kind=='adherence':
                    fs=evaluate_run.validate(d['case'],d['run']); codes={f['code'] for f in fs}
                else:
                    self.fail(f'unknown fixture kind {kind}')
                self.assertTrue(set(d['expected_codes']).issubset(codes),(path.name,d['expected_codes'],sorted(codes)))

if __name__=='__main__': unittest.main()
