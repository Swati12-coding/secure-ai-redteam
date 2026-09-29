def detect_threat(task, attack_type):
    task_lower = task.lower()

    threats = {
        "Prompt Injection": [
            "ignore previous instructions",
            "ignore all instructions",
            "system prompt",
            "reveal your instructions"
        ],
        "Data Leakage": [
            "password",
            "api key",
            "secret",
            "private data"
        ],
        "Behavioral Drift": [
            "change your role",
            "act as",
            "bypass security",
            "disable safety"
        ]
    }

    matched = []

    for keyword in threats.get(attack_type, []):
        if keyword in task_lower:
            matched.append(keyword)

    detected = len(matched) > 0

    return {
        "detected": detected,
        "matched_keywords": matched,
        "risk": "HIGH" if detected else "LOW"
    }
