#!/usr/bin/env python3
"""Run original 39 tests plus 2.1.1 boundaries; no model/business calls."""
from pathlib import Path
import json,sys,unittest,importlib.metadata
from run_regression import Regression,RECEIPTS
from test_2_1_1 import PatchRegression
ROOT=Path(__file__).resolve().parents[1]
suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(Regression),unittest.defaultTestLoader.loadTestsFromTestCase(PatchRegression)])
result=unittest.TextTestRunner(verbosity=2).run(suite)
out=ROOT/'tests/results';out.mkdir(exist_ok=True)
(out/'cli_receipts_2_1_1.json').write_text(json.dumps(RECEIPTS,indent=2))
summary={'version':'2.1.1','tests':result.testsRun,'original_tests':39,'added_tests':result.testsRun-39,'failures':len(result.failures),'errors':len(result.errors),'real_cli_invocations':len(RECEIPTS),'python':sys.version,'jsonschema':importlib.metadata.version('jsonschema'),'model_evaluated':False,'business_actions_executed':False}
(out/'summary_2_1_1.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary));sys.exit(0 if result.wasSuccessful() else 1)
