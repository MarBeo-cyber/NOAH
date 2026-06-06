from __future__ import annotations

from .models import CognitiveNode, ConceptProjection, WisdomTrace, ConsentProfile, ConsentScope


class RosettaConceptLibrary:
    """Concept projections for the shared cognitive space.

    In production this is a model-aligned embedding layer. In the MVP it is an
    interpretable low-dimensional semantic space.
    """

    def concept(self, name: str) -> ConceptProjection:
        if name == "silence":
            return ConceptProjection("silence", {
                "absence": 0.80,
                "respect": 0.10,
                "processing_time": 0.20,
                "ethical_withholding": 0.35,
                "system_quiet": 0.25,
            }, "Ambiguous pause/non-utterance in interaction.")
        if name == "urgency":
            return ConceptProjection("urgency", {
                "speed": 0.85,
                "hierarchy": 0.35,
                "system_balance": 0.20,
                "kairos": 0.40,
                "risk_reduction": 0.55,
            }, "Need for timely action under constraint.")
        if name == "responsibility":
            return ConceptProjection("responsibility", {
                "ownership": 0.80,
                "role_obligation": 0.55,
                "care": 0.40,
                "ethical_answerability": 0.45,
                "evidence": 0.35,
            }, "Who must answer for action, evidence and consequences.")
        if name == "reasonable_efforts":
            return ConceptProjection("reasonable_efforts", {
                "legal_standard": 0.75,
                "operational_evidence": 0.30,
                "ownership": 0.45,
                "ambiguity": 0.80,
                "contract_execution": 0.65,
            }, "Contractual expression requiring operational disambiguation.")
        raise KeyError(name)


class SyntheticNodeFactory:
    """Four canonical nodes used in the NOAH working paper line."""

    def build_default_nodes(self) -> list[CognitiveNode]:
        tanaka_consent = ConsentProfile()
        chen_consent = ConsentProfile()
        # Allow aggregate learning for Chen to demonstrate opt-in difference.
        chen_consent.scopes[ConsentScope.AGGREGATED_LEARNING] = True

        return [
            CognitiveNode(
                "david",
                "David",
                {
                    "absence": .88,
                    "ownership": .84,
                    "speed": .78,
                    "explicit_commitment": .90,
                    "operational_evidence": .72,
                },
                metadata={"profile": "engineering / explicit commitment"},
            ),
            CognitiveNode(
                "tanaka",
                "Tanaka",
                {
                    "respect": .86,
                    "processing_time": .76,
                    "hierarchy": .82,
                    "role_obligation": .70,
                    "implicit_commitment": .72,
                },
                consent=tanaka_consent,
                metadata={"profile": "management / implicit hierarchy"},
            ),
            CognitiveNode(
                "chen",
                "Dr. Chen",
                {
                    "system_balance": .84,
                    "care": .76,
                    "system_quiet": .80,
                    "processing_time": .58,
                    "risk_reduction": .52,
                },
                consent=chen_consent,
                metadata={"profile": "clinical-systemic / balance"},
            ),
            CognitiveNode(
                "muller",
                "Prof. Mueller",
                {
                    "ethical_withholding": .84,
                    "kairos": .64,
                    "ethical_answerability": .86,
                    "ambiguity": .62,
                    "dialogue": .74,
                },
                metadata={"profile": "hermeneutics / ethical answerability"},
            ),
        ]


class WisdomTraceFactory:
    def build_demo_traces(self) -> list[WisdomTrace]:
        return [
            WisdomTrace(
                concept="silence",
                operational_rule="Do not translate silence with your own schema before contextualizing it.",
                vector={"absence": .20, "respect": .65, "processing_time": .75, "explicit_bridge": .78},
                confidence=.82,
                export_consent=True,
            ),
            WisdomTrace(
                concept="reasonable_efforts",
                operational_rule="Convert ambiguous standards into thresholds, examples and evidence.",
                vector={"legal_standard": .60, "operational_evidence": .90, "contract_execution": .80, "ambiguity": .45},
                confidence=.78,
                export_consent=True,
            ),
            WisdomTrace(
                concept="urgency",
                operational_rule="Urgency may mean speed, priority, hierarchy or risk reduction; ask which one.",
                vector={"speed": .70, "hierarchy": .45, "risk_reduction": .80, "kairos": .55},
                confidence=.74,
                export_consent=False,
            ),
        ]
