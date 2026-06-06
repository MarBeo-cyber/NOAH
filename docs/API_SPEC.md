# API Spec

## Build prebrief

```python
from noah_core.orchestrator import NOAHCollectiveFieldOrchestrator

noah = NOAHCollectiveFieldOrchestrator()
prebrief = noah.build_prebrief("silence")
```

## FieldState

```json
{
  "concept": "silence",
  "active_nodes": 4,
  "dispersion": 0.47,
  "tension_score": 0.61,
  "risk": "HIGH"
}
```

## BridgeRecommendation

```json
{
  "target": "TAAA",
  "message": "Pre-brief TAAA: chiarire che il silenzio può indicare riflessione, non rifiuto.",
  "reason": "collective_field_high_gap"
}
```
