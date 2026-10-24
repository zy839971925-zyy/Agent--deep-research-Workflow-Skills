#!/usr/bin/env python3
"""Run deterministic synthetic package tests; never writes receipts unless requested."""
from pathlib import Path
import argparse, importlib.metadata, json, sys, unittest
from run_regression import Regression, RECEIPTS
from test_2_1_1 import PatchRegression
from test_harness_bridge_reconciliation import LostReceiptReconciliation
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,help='optional disposable directory for versioned test receipts')
    args=parser.parse_args()
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(Regression),unittest.defaultTestLoader.loadTestsFromTestCase(PatchRegression),unittest.defaultTestLoader.loadTestsFromTestCase(LostReceiptReconciliation)])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    summary={'version':'3.0.0','tests':result.testsRun,'baseline_tests':39,'additional_tests':result.testsRun-39,'failures':len(result.failures),'errors':len(result.errors),'real_cli_invocations':len(RECEIPTS),'python':sys.version,'jsonschema':importlib.metadata.version('jsonschema'),'model_evaluated':False,'business_actions_executed':False,'receipts_written':bool(args.output_dir)}
    if args.output_dir:
        out=args.output_dir.expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
        (out/'cli_receipts_3_0_0.json').write_text(json.dumps(RECEIPTS,indent=2)+'\n',encoding='utf-8')
        (out/'summary_3_0_0.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
    return 0 if result.wasSuccessful() else 1
if __name__=='__main__': raise SystemExit(main())
