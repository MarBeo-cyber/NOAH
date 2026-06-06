from __future__ import annotations

from .models import FieldState, BridgeRecommendation, BridgeTarget, GapRisk


class BridgePrioritizer:
    """Turns high-gap pairs into bridge recommendations for TAAA/XAAA."""

    def recommend(self, field: FieldState, collective_hint: str = "") -> list[BridgeRecommendation]:
        recs: list[BridgeRecommendation] = []
        for pair in sorted(field.high_gap_pairs, key=lambda p: p.distance, reverse=True):
            if pair.concept == "silence":
                msg = "Pre-brief TAAA: chiarire che il silenzio può indicare riflessione, non rifiuto."
            elif pair.concept == "reasonable_efforts":
                msg = "Pre-brief TAAA: convertire 'reasonable efforts' in soglie, esempi ed evidenze."
            else:
                msg = f"Pre-brief TAAA consigliato sul concetto '{pair.concept}'."

            if collective_hint and not collective_hint.startswith("No consented"):
                msg += f" XAAA hint: {collective_hint}"

            recs.append(BridgeRecommendation(
                concept=pair.concept,
                target=BridgeTarget.TAAA,
                source_node=pair.source_node,
                target_node=pair.target_node,
                message=msg,
                risk=pair.risk,
                priority=round(pair.distance, 4),
                allowed=True,
                reason="collective_field_high_gap",
            ))

        if not recs and field.risk in {GapRisk.MEDIUM, GapRisk.HIGH}:
            recs.append(BridgeRecommendation(
                concept=field.concept,
                target=BridgeTarget.HUMAN_FACILITATOR,
                message="Moderatore: monitorare possibili divergenze di schema nel gruppo.",
                risk=field.risk,
                priority=field.tension_score,
                allowed=True,
                reason="group_tension_without_pair_criticality",
            ))
        return recs
