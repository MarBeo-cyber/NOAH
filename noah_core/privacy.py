from __future__ import annotations

import random
from .models import CognitiveNode, ConsentScope


class PrivacyGovernor:
    """Privacy gate for cognitive geometry.

    Production NOAH requires differential privacy for rare schema signatures.
    This MVP implements consent gating, k-anonymity threshold and optional bounded noise.
    """

    def __init__(self, k_min: int = 3, noise_epsilon: float = 0.0, seed: int = 42) -> None:
        self.k_min = k_min
        self.noise_epsilon = max(0.0, noise_epsilon)
        self.random = random.Random(seed)

    def filter_nodes_for_geometry(self, nodes: list[CognitiveNode]) -> list[CognitiveNode]:
        return [n for n in nodes if n.consent.allows(ConsentScope.GEOMETRY_EXPORT)]

    def k_anonymity_ok(self, nodes: list[CognitiveNode]) -> bool:
        return len(nodes) >= self.k_min

    def privatize_centroid(self, centroid: dict[str, float]) -> dict[str, float]:
        if self.noise_epsilon <= 0:
            return dict(centroid)
        out = {}
        for k, v in centroid.items():
            noise = self.random.uniform(-self.noise_epsilon, self.noise_epsilon)
            out[k] = round(max(0.0, min(1.0, v + noise)), 4)
        return out
