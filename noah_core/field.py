from __future__ import annotations

from .models import CognitiveNode, ConceptProjection, FieldState, GapRisk, PairwiseGap
from .geometry import CognitiveGeometryEngine
from .privacy import PrivacyGovernor


class CollectiveCognitiveField:
    """Builds collective field state from consented nodes."""

    def __init__(self, privacy: PrivacyGovernor | None = None) -> None:
        self.geometry = CognitiveGeometryEngine()
        self.privacy = privacy or PrivacyGovernor()

    def evaluate(self, nodes: list[CognitiveNode], concept: ConceptProjection) -> FieldState:
        active = self.privacy.filter_nodes_for_geometry(nodes)
        if not self.privacy.k_anonymity_ok(active):
            return FieldState(
                concept=concept.concept,
                active_nodes=len(active),
                centroid={},
                dispersion=0.0,
                tension_score=0.0,
                risk=GapRisk.LOW,
                high_gap_pairs=[],
            )

        gaps: list[PairwiseGap] = []
        for i, a in enumerate(active):
            for b in active[i + 1:]:
                gaps.append(self.geometry.pair_gap(a, b, concept))

        high = [g for g in gaps if g.risk in {GapRisk.HIGH, GapRisk.CRITICAL}]
        dispersion = self.geometry.dispersion(active, concept)
        tension = round(max([g.distance for g in gaps] or [0.0]) * 0.65 + dispersion * 0.35, 4)
        risk = self._risk(tension)
        centroid = self.privacy.privatize_centroid(self.geometry.centroid(active, concept))

        return FieldState(
            concept=concept.concept,
            active_nodes=len(active),
            centroid=centroid,
            dispersion=dispersion,
            tension_score=tension,
            risk=risk,
            high_gap_pairs=high,
        )

    def _risk(self, score: float) -> GapRisk:
        if score >= 0.65:
            return GapRisk.CRITICAL
        if score >= 0.45:
            return GapRisk.HIGH
        if score >= 0.25:
            return GapRisk.MEDIUM
        return GapRisk.LOW
