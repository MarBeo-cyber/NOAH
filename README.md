# NOAH v0.3 - Collective Cognitive Field

NOAH v0.3 extends the v0.2 four-node MVP into a first **Collective Cognitive Field** layer.

## What changed from v0.2

- Field-level state, not only pairwise gap.
- Tension score and dispersion.
- Consent-gated geometry filtering.
- k-anonymity threshold.
- Optional bounded noise for DP-style experimentation.
- XAAA Wisdom Trace ingestion through an Experience Exchange Protocol.
- TAAA pre-brief generation.

## Quickstart

```bash
python examples/run_demo.py
python -m pytest tests -q
```

## Boundary

NOAH does not translate and does not expose private Schema Memory. It predicts where TAAA should translate, using only consented geometry and abstracted wisdom traces.
