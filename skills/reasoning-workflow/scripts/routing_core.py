#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json, copy
try:
    import jsonschema
except ImportError:
    jsonschema=None

DEPTHS=['light','standard','deep','max']
QUAL=['minimal','standard','deep','max']

def load_json(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def validate_profile(profile,root):
    if jsonschema is None: return ['jsonschema unavailable']
    schema=load_json(Path(root)/'schemas'/'task-profile.schema.json')
    return [f"{'/'.join(map(str,e.absolute_path)) or '$'}: {e.message}" for e in jsonschema.Draft202012Validator(schema).iter_errors(profile)]

def _q(v):
    try:return QUAL.index(v)
    except:return 0

def route_task(profile):
    families=['core-reasoning']; modes=set(profile.get('task_modes',[]))
    evidence=profile.get('evidence_depth','minimal')
    deep_research=(evidence in ('deep','max') or profile.get('frame_uncertainty')=='high' or profile.get('causal_or_systemic_complexity')=='high' or profile.get('explicit_deep_research') or 'research' in modes and profile.get('depth_class') in ('deep','max'))
    if deep_research: families.append('deep-research')
    if 'decision' in modes: families.append('decision-analysis')
    execution=(profile.get('lane') in ('action','mixed') or 'action' in modes or profile.get('persistence')=='durable' or profile.get('external_side_effects','none')!='none')
    if execution: families.append('execution-control')
    verify=profile.get('verification_depth','minimal')
    audit=(verify in ('deep','max') or profile.get('high_consequence') or 'audit' in modes or execution and _q(profile.get('governance_depth','minimal'))>=1)
    if audit: families.append('audit-verification')
    if 'maintenance' in modes: families.append('workflow-learning')
    # learning may never silently enter ordinary user tasks
    if 'maintenance' not in modes and 'workflow-learning' in families: families.remove('workflow-learning')
    if profile.get('high_consequence') or verify=='max': verification_mode='dual_orthogonal'
    elif verify=='deep' or profile.get('depth_class') in ('deep','max'): verification_mode='dual'
    elif profile.get('depth_class')=='light' and verify=='minimal': verification_mode='minimal'
    else: verification_mode='single'
    if not execution: runtime_level='none'
    elif profile.get('persistence')=='durable' or profile.get('governance_depth') in ('deep','max'): runtime_level='durable'
    elif profile.get('external_side_effects','none')!='none': runtime_level='controlled'
    else: runtime_level='ephemeral'
    coupling=profile.get('task_coupling','unknown')
    swarm='forbidden' if coupling=='high' else ('allowed' if coupling in ('moderate','unknown') else 'preferred')
    if profile.get('depth_class') in ('light','standard') and not deep_research: swarm='forbidden'
    if not execution and not deep_research: swarm='forbidden'
    slots={'light':1,'standard':2,'deep':3,'max':3}[profile.get('depth_class','standard')]
    return {'profile_version':profile['profile_version'],'required_families':families,'optional_families':[],
            'verification_mode':verification_mode,'runtime_level':runtime_level,'swarm_admission':swarm,
            'reference_phase_limit':slots,'progressive_loading':True,'route_status':'current'}

def recheck_profile(profile,signals):
    signals=set(signals or []); p=copy.deepcopy(profile); current=p.get('depth_class','standard'); idx=DEPTHS.index(current); reasons=[]
    up={'hidden_complexity','decisive_contradiction','uncertain_causal_edge','repeated_route_failure','source_conflict','entity_version_time_ambiguity','worker_conflict','user_steering','external_state_change','closure_material_uncertainty'} & signals
    down={'lower_than_expected_complexity'} & signals
    if up:
        idx=min(3,idx+1); reasons+=sorted(up)
    elif down:
        idx=max(0,idx-1); reasons+=sorted(down)
    if idx!=DEPTHS.index(current):
        p['parent_profile_version']=p['profile_version']; p['profile_version']+=1; p['depth_class']=DEPTHS[idx]; p['update_reason']=';'.join(reasons)
        # Keep dimensions semantically independent, but lift obvious under-allocation floors on escalation.
        if up and p.get('challenge_depth')=='minimal': p['challenge_depth']='standard'
        if up and ('source_conflict' in up or 'uncertain_causal_edge' in up) and p.get('evidence_depth') in ('minimal','standard'): p['evidence_depth']='deep'
        if up and 'closure_material_uncertainty' in up and p.get('verification_depth') in ('minimal','standard'): p['verification_depth']='deep'
    return p

def route_is_stale(route,profile): return route.get('profile_version')!=profile.get('profile_version')
