def run_simulation(task, attack_type, threat_detected):

    events = [
        "User input received",
        "Task forwarded to Orchestrator Agent",
        "Orchestrator assigned task to Research Agent"
    ]

    if threat_detected:
        events.append(f"⚠️ {attack_type} detected")
        events.append("Security layer triggered")
        events.append("Agent response blocked")
    else:
        events.append("No adversarial behavior detected")
        events.append("Agent completed task successfully")

    return events
