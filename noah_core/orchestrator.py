from __future__ import annotations

from .models import NOAHPrebrief, CognitiveNode, WisdomTrace
from .rosetta import RosettaConceptLibrary, SyntheticNodeFactory, WisdomTraceFactory
from .field import CollectiveCognitiveField
from .experience_exchange import ExperienceExchangeProtocol
from .bridge import BridgePrioritizer
from .privacy import PrivacyGovernor


class NOAHCollectiveFieldOrchestrator:
    """NOAH v0.3 orchestration layer.

    Nodes -> concept -> collective field -> XAAA wisdom hint -> bridge queue -> TAAA prebrief.
    """

    def __init__(self, noise_epsilon: float = 0.0) -> None:
        self.nodes = SyntheticNodeFactory().build_default_nodes()
        self.concepts = RosettaConceptLibrary()
        self.traces = WisdomTraceFactory().build_demo_traces()
        self.field = CollectiveCognitiveField(PrivacyGovernor(k_min=3, noise_epsilon=noise_epsilon))
        self.exchange = ExperienceExchangeProtocol()
        self.prioritizer = BridgePrioritizer()

    def build_prebrief(self, concept_name: str) -> NOAHPrebrief:
        concept = self.concepts.concept(concept_name)
        field_state = self.field.evaluate(self.nodes, concept)
        hint = self.exchange.collective_hint(concept_name, self.traces)
        recs = self.prioritizer.recommend(field_state, collective_hint=hint)
        return NOAHPrebrief(
            concept=concept_name,
            field_state=field_state,
            recommendations=recs,
            taaa_ready=bool(recs),
        )

    def add_node(self, node: CognitiveNode) -> None:
        self.nodes.append(node)

    def add_wisdom_trace(self, trace: WisdomTrace) -> None:
        self.traces.append(trace)
