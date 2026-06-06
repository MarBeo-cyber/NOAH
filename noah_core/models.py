from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone
from typing import Dict, List, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ConsentScope(str, Enum):
    GEOMETRY_EXPORT = "geometry_export"
    BRIDGE_RECOMMENDATION = "bridge_recommendation"
    AGGREGATED_LEARNING = "aggregated_learning"
    WISDOM_TRACE_EXPORT = "wisdom_trace_export"


class GapRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BridgeTarget(str, Enum):
    TAAA = "TAAA"
    XAAA = "XAAA"
    SAAA = "SAAA"
    HUMAN_FACILITATOR = "human_facilitator"


@dataclass
class ConsentProfile:
    scopes: Dict[ConsentScope, bool] = field(default_factory=lambda: {
        ConsentScope.GEOMETRY_EXPORT: True,
        ConsentScope.BRIDGE_RECOMMENDATION: True,
        ConsentScope.AGGREGATED_LEARNING: False,
        ConsentScope.WISDOM_TRACE_EXPORT: False,
    })

    def allows(self, scope: ConsentScope) -> bool:
        return bool(self.scopes.get(scope, False))


@dataclass
class CognitiveNode:
    node_id: str
    label: str
    schema_signature: Dict[str, float]
    consent: ConsentProfile = field(default_factory=ConsentProfile)
    metadata: Dict = field(default_factory=dict)


@dataclass
class ConceptProjection:
    concept: str
    vector: Dict[str, float]
    description: str = ""


@dataclass
class WisdomTrace:
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    source_module: str = "XAAA"
    concept: str = ""
    operational_rule: str = ""
    vector: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    export_consent: bool = False


@dataclass
class PairwiseGap:
    source_node: str
    target_node: str
    concept: str
    distance: float
    risk: GapRisk
    drivers: List[str] = field(default_factory=list)


@dataclass
class FieldState:
    concept: str
    active_nodes: int
    centroid: Dict[str, float]
    dispersion: float
    tension_score: float
    risk: GapRisk
    high_gap_pairs: List[PairwiseGap] = field(default_factory=list)


@dataclass
class BridgeRecommendation:
    recommendation_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
    concept: str = ""
    target: BridgeTarget = BridgeTarget.TAAA
    source_node: str = ""
    target_node: str = ""
    message: str = ""
    risk: GapRisk = GapRisk.LOW
    priority: float = 0.0
    allowed: bool = True
    reason: str = ""


@dataclass
class NOAHPrebrief:
    prebrief_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
    concept: str = ""
    field_state: Optional[FieldState] = None
    recommendations: List[BridgeRecommendation] = field(default_factory=list)
    taaa_ready: bool = False
    privacy_note: str = "Only consented geometry is used; private Schema Memory is not exported."
