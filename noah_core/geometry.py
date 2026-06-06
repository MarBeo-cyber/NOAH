from __future__ import annotations

from math import sqrt
from .models import CognitiveNode, ConceptProjection, PairwiseGap, GapRisk


class CognitiveGeometryEngine:
    """Collective cognitive geometry.

    v0.3 uses concept-relevant subspace distance and driver extraction.
    """

    def relevant_axes(self, a: CognitiveNode, b: CognitiveNode, concept: ConceptProjection) -> list[str]:
        keys = set(concept.vector) | set(a.schema_signature) | set(b.schema_signature)
        axes = [
            k for k in keys
            if concept.vector.get(k, 0.0) > 0.15
            or a.schema_signature.get(k, 0.0) > 0.45
            or b.schema_signature.get(k, 0.0) > 0.45
        ]
        return axes or list(keys)

    def pair_gap(self, a: CognitiveNode, b: CognitiveNode, concept: ConceptProjection) -> PairwiseGap:
        axes = self.relevant_axes(a, b, concept)
        s = 0.0
        axis_gaps = []
        for k in axes:
            delta = abs(a.schema_signature.get(k, 0.0) - b.schema_signature.get(k, 0.0))
            s += delta ** 2
            axis_gaps.append((k, delta))
        distance = min(1.0, sqrt(s) / max(1.0, sqrt(len(axes))))
        drivers = [k for k, _ in sorted(axis_gaps, key=lambda x: x[1], reverse=True)[:3]]
        return PairwiseGap(
            source_node=a.node_id,
            target_node=b.node_id,
            concept=concept.concept,
            distance=round(distance, 4),
            risk=self._risk(distance),
            drivers=drivers,
        )

    def centroid(self, nodes: list[CognitiveNode], concept: ConceptProjection) -> dict[str, float]:
        axes = set(concept.vector)
        for n in nodes:
            axes |= set(n.schema_signature)
        out = {}
        for k in axes:
            out[k] = round(sum(n.schema_signature.get(k, 0.0) for n in nodes) / max(1, len(nodes)), 4)
        return out

    def dispersion(self, nodes: list[CognitiveNode], concept: ConceptProjection) -> float:
        if len(nodes) <= 1:
            return 0.0
        pairs = []
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                pairs.append(self.pair_gap(a, b, concept).distance)
        return round(sum(pairs) / len(pairs), 4)

    def _risk(self, d: float) -> GapRisk:
        if d >= 0.65:
            return GapRisk.CRITICAL
        if d >= 0.45:
            return GapRisk.HIGH
        if d >= 0.25:
            return GapRisk.MEDIUM
        return GapRisk.LOW
