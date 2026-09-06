#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, tempfile, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
def mod(name):
    p=ROOT/'scripts'/f'{name}.py'; spec=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
validate_skill=mod('validate_skill'); validate_links=mod('validate_links'); validate_state=mod('validate_state'); validate_delivery=mod('validate_delivery'); validate_events=mod('validate_events'); validate_raw=mod('validate_raw'); evaluate_run=mod('evaluate_run')

def base_question():
    return {"schema_version":"2.0","work_id":"W","state_version":2,"lane":"question","declared_status":"active","objective":"answer","root_question_ref":"Q-1","updated_at":"2026-09-06T20:00:00+08:00",
      "questions":[{"id":"Q-1","record_type":"question","declared_status":"answered","materiality":"material","closure_effect":"blocking","text":"x?","question_type":"fact","answer_refs":["ANS-1"],"child_question_refs":[],"recomposition_status":"not_required","drift_check":"pass"}],
      "answers":[{"id":"ANS-1","record_type":"answer","declared_status":"current","materiality":"material","closure_effect":"blocking","text":"x","question_refs":["Q-1"],"premise_refs":["P-1"]}],
      "premises":[{"id":"P-1","record_type":"premise","declared_status":"current","materiality":"material","closure_effect":"blocking","text":"p","source_kind":"user_definition"}],
      "stale_items":[],"blocked_items":[]}

class Tests(unittest.TestCase):
    def test_package(self):
        self.assertEqual(validate_skill.validate(ROOT),[]); self.assertEqual(validate_links.validate(ROOT),[])
    def test_cases_have_observables(self):
        files=list((ROOT/'tests/cases').glob('*.json')); self.assertGreaterEqual(len(files),24)
        for p in files:
            d=json.loads(p.read_text()); self.assertIn('observables',d); self.assertIn('expected',d)
    def test_valid_question_closure(self):
        s=base_question(); s['declared_status']='closed'; fs,reg,cl=validate_state.validate(s,ROOT); self.assertFalse([f for f in fs if f.severity=='ERROR'],[f.message for f in fs]); self.assertTrue(cl['epistemic']['computed_epistemic_closed'])
    def test_closure_blocks_open_root_no_answer(self):
        s=base_question(); s['declared_status']='closed'; s['questions'][0]['declared_status']='open'; s['questions'][0]['answer_refs']=[]; s['answers']=[]
        fs,reg,cl=validate_state.validate(s,ROOT); self.assertFalse(cl['epistemic']['computed_epistemic_closed']); self.assertTrue(any(f.code=='EPISTEMIC_CLOSURE_BLOCKED' for f in fs))
    def test_material_open_uncertainty_blocks(self):
        s=base_question(); s['declared_status']='closed'; s['questions'][0]['uncertainty_refs']=['U-1']; s['uncertainties']=[{"id":"U-1","record_type":"uncertainty","declared_status":"open","materiality":"material","closure_effect":"blocking","text":"u","uncertainty_type":"missing_evidence"}]
        fs,reg,cl=validate_state.validate(s,ROOT); self.assertFalse(cl['epistemic']['computed_epistemic_closed'])
    def test_nonmaterial_open_uncertainty_does_not_block(self):
        s=base_question(); s['declared_status']='closed'; s['questions'][0]['uncertainty_refs']=['U-1']; s['uncertainties']=[{"id":"U-1","record_type":"uncertainty","declared_status":"open","materiality":"incidental","closure_effect":"nonblocking","text":"u","uncertainty_type":"missing_evidence"}]
        fs,reg,cl=validate_state.validate(s,ROOT); self.assertTrue(cl['epistemic']['computed_epistemic_closed'])
    def test_transitive_invalidation(self):
        s=base_question(); s['premises'][0]['declared_status']='stale'; s['inferences']=[{"id":"INF-1","record_type":"inference","declared_status":"current","materiality":"material","closure_effect":"blocking","conclusion":"i","premise_refs":["P-1"]}]; s['judgments']=[{"id":"JDG-1","record_type":"judgment","declared_status":"current","materiality":"material","closure_effect":"blocking","text":"j","depends_on":["INF-1"]}]
        fs,reg,cl=validate_state.validate(s,ROOT); self.assertEqual(reg['INF-1']['effective_status'],'stale'); self.assertEqual(reg['JDG-1']['effective_status'],'stale')
    def test_typed_ref_rejects_artifact_as_premise(self):
        s=base_question(); s['artifacts']=[{"id":"ART-7","record_type":"artifact","declared_status":"current","materiality":"supporting","closure_effect":"nonblocking"}]; s['answers'][0]['premise_refs']=['ART-7']
        fs,_,_=validate_state.validate(s,ROOT); self.assertTrue(any(f.code=='REF_TYPE' for f in fs))
    def test_relationship_type_and_endpoints_enforced_by_schema(self):
        s=base_question(); s['relationships']=[{"id":"R-1","record_type":"relationship","declared_status":"current","materiality":"supporting","closure_effect":"nonblocking","relation_type":"telepathically_causes","epistemic_status":"inferred"}]
        fs,_,_=validate_state.validate(s,ROOT); self.assertTrue(any(f.code=='SCHEMA' for f in fs))
    def test_delivery_reconciles_requirement_and_verification(self):
        s=base_question(); s['lane']='action'; s['root_question_ref']=None; s['requirements']=[{"id":"REQ-1","record_type":"requirement","declared_status":"blocked","materiality":"material","closure_effect":"blocking"}]; s['verification']=[]
        m={"schema_version":"2.0","work_id":"W","state_version":2,"generated_at":"x","requirements":[{"id":"REQ-1","declared_status":"satisfied","artifact_refs":[],"verification_refs":["VER-404"]}],"acceptance_criteria":[],"artifacts":[],"blocking_items":[],"inconsistencies":[],"declared_delivery_ready":True}
        fs,c=validate_delivery.validate(s,m); self.assertFalse(c['computed_delivery_ready']); self.assertTrue(any(f.code in ('REQ_STATE_DIVERGENCE','REQ_VER_REF') for f in fs))
    def test_event_continuity(self):
        s=base_question(); s['state_version']=3
        ev=[{"schema_version":"2.0","event_id":"E1","work_id":"W","event_seq":1,"timestamp":"t","event_type":"x","from_state_version":1,"to_state_version":2},{"schema_version":"2.0","event_id":"E2","work_id":"W","event_seq":3,"timestamp":"t","event_type":"x","from_state_version":2,"to_state_version":3}]
        fs=validate_events.validate(ev,s,ROOT); self.assertTrue(any(f.code=='EVENT_SEQ_GAP' for f in fs))
    def test_raw_cycle(self):
        rec=[{"schema_version":"2.0","raw_id":"R1","record_kind":"derived","source_type":"file","source_locator":"x","observed_at":"t","visibility":"user_provided","immutable_preserved":True,"derived_from":["R2"],"transformations":[]},{"schema_version":"2.0","raw_id":"R2","record_kind":"derived","source_type":"file","source_locator":"x","observed_at":"t","visibility":"user_provided","immutable_preserved":True,"derived_from":["R1"],"transformations":[]}]
        fs=validate_raw.validate(rec); self.assertTrue(any(f.code=='RAW_LINEAGE_CYCLE' for f in fs))
    def test_behavioral_observable_evaluator(self):
        case={'observables':{'expected_events':['closure_attempted'],'forbidden_events':['closure_committed'],'expected_final_state':{'declared_status':'active'},'expected_findings':['X']}}
        run={'events':[{'event':'closure_attempted'}],'final_state':{'declared_status':'active'},'findings':[{'code':'X'}]}; self.assertEqual(evaluate_run.validate(case,run),[])

    def test_runtime_closure_blocks_material_requirement(self):
        s=base_question(); s['lane']='action'; s['root_question_ref']=None; s['declared_status']='closed'; s['requirements']=[{"id":"REQ-1","record_type":"requirement","declared_status":"blocked","materiality":"material","closure_effect":"blocking"}]
        fs,reg,cl=validate_state.validate(s,ROOT); self.assertFalse(cl['runtime']['computed_runtime_closed']); self.assertTrue(any(f.code=='RUNTIME_CLOSURE_BLOCKED' for f in fs))

if __name__=='__main__': unittest.main()
