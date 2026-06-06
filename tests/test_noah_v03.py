from noah_core.orchestrator import NOAHCollectiveFieldOrchestrator
from noah_core.privacy import PrivacyGovernor
from noah_core.rosetta import SyntheticNodeFactory, RosettaConceptLibrary, WisdomTraceFactory
from noah_core.field import CollectiveCognitiveField
from noah_core.models import ConsentScope, WisdomTrace
from noah_core.experience_exchange import ExperienceExchangeProtocol


def test_collective_field_detects_silence_tension():
    noah = NOAHCollectiveFieldOrchestrator()
    prebrief = noah.build_prebrief("silence")
    assert prebrief.field_state.active_nodes == 4
    assert prebrief.field_state.tension_score > 0.25
    assert prebrief.taaa_ready is True


def test_prebrief_contains_taaa_recommendation():
    noah = NOAHCollectiveFieldOrchestrator()
    prebrief = noah.build_prebrief("silence")
    assert any(r.target.value == "TAAA" for r in prebrief.recommendations)


def test_k_anonymity_blocks_small_group():
    nodes = SyntheticNodeFactory().build_default_nodes()[:2]
    concept = RosettaConceptLibrary().concept("silence")
    field = CollectiveCognitiveField(PrivacyGovernor(k_min=3))
    state = field.evaluate(nodes, concept)
    assert state.active_nodes == 2
    assert state.centroid == {}
    assert state.tension_score == 0.0


def test_consent_filters_node_from_geometry():
    nodes = SyntheticNodeFactory().build_default_nodes()
    nodes[0].consent.scopes[ConsentScope.GEOMETRY_EXPORT] = False
    concept = RosettaConceptLibrary().concept("silence")
    state = CollectiveCognitiveField(PrivacyGovernor(k_min=3)).evaluate(nodes, concept)
    assert state.active_nodes == 3


def test_experience_exchange_accepts_only_consented_high_confidence():
    traces = WisdomTraceFactory().build_demo_traces()
    accepted = ExperienceExchangeProtocol().accepted_traces(traces)
    assert all(t.export_consent and t.confidence >= 0.70 for t in accepted)
    assert len(accepted) == 2


def test_reasonable_efforts_prebrief_uses_xaaa_hint():
    noah = NOAHCollectiveFieldOrchestrator()
    prebrief = noah.build_prebrief("reasonable_efforts")
    text = " ".join(r.message for r in prebrief.recommendations)
    assert "reasonable efforts" in text.lower() or "soglie" in text.lower()
