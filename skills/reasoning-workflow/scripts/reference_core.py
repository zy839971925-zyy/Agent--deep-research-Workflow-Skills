"""Canonical record dependency traversal; not external source authentication."""
from semantic_core import build_registry
EXTRA_REFERENCE_FIELDS = {'depends_on', 'derived_from', 'supports', 'contradicts', 'represents', 'implements'}

def record_dependencies(record):
    for key, value in record.items():
        if key == 'verification_refs':  # review backlink, not underlying target evidence
            continue
        if key.endswith('_ref') or key.endswith('_refs') or key in EXTRA_REFERENCE_FIELDS:
            if value is None:
                continue
            values = value if isinstance(value, list) else [value]
            for ref in values:
                if not isinstance(ref, str) or not ref:
                    raise ValueError('invalid canonical dependency ' + key)
                yield ref

def dependency_closure(state, refs):
    registry, findings = build_registry(state)
    if findings:
        raise ValueError('invalid canonical registry: ' + ','.join(f.code for f in findings))
    pending = list(refs)
    found = {}
    while pending:
        ref = pending.pop()
        if ref in found:
            continue
        if ref not in registry:
            raise ValueError('unknown target/dependency ' + ref)
        record = registry[ref]['record']
        found[ref] = record
        pending.extend(record_dependencies(record))
    if not found:
        raise ValueError('empty review target scope')
    return found
