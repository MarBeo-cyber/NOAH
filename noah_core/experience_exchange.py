from __future__ import annotations

from .models import WisdomTrace, ConsentScope, CognitiveNode


class ExperienceExchangeProtocol:
    """Accepts XAAA Wisdom Traces only with export consent.

    NOAH does not ingest raw experience. It receives abstracted Wisdom Traces:
    operational rules + low-dimensional pattern vectors.
    """

    def accepted_traces(self, traces: list[WisdomTrace]) -> list[WisdomTrace]:
        return [t for t in traces if t.export_consent and t.confidence >= 0.70]

    def collective_hint(self, concept: str, traces: list[WisdomTrace]) -> str:
        accepted = [t for t in self.accepted_traces(traces) if t.concept == concept]
        if not accepted:
            return "No consented collective wisdom trace available."
        # MVP: choose highest-confidence trace.
        best = max(accepted, key=lambda t: t.confidence)
        return best.operational_rule
