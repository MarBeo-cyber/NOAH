from noah_core.orchestrator import NOAHCollectiveFieldOrchestrator

noah = NOAHCollectiveFieldOrchestrator()
prebrief = noah.build_prebrief("silence")

print("NOAH v0.3 Collective Cognitive Field")
print("------------------------------------")
print("concept:", prebrief.concept)
print("active_nodes:", prebrief.field_state.active_nodes)
print("dispersion:", prebrief.field_state.dispersion)
print("tension:", prebrief.field_state.tension_score)
print("risk:", prebrief.field_state.risk.value)
print("recommendations:", len(prebrief.recommendations))
for rec in prebrief.recommendations:
    print("-", rec.source_node, "->", rec.target_node, rec.risk.value, rec.message)
