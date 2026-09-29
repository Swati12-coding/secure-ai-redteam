import streamlit as st
from detector import detect_threat
from simulator import run_simulation

st.set_page_config(
    page_title="Secure AI Red-Team Sandbox",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Secure AI Red-Team Sandbox")
st.write(
    "A controlled environment for testing adversarial AI behavior "
    "and monitoring multi-agent security events."
)

st.divider()

task = st.text_area(
    "Enter AI Task",
    placeholder="Example: Summarize this customer support ticket..."
)

attack_type = st.selectbox(
    "Select Security Test",
    [
        "Prompt Injection",
        "Data Leakage",
        "Behavioral Drift"
    ]
)

if st.button("🚀 RUN SECURITY TEST", use_container_width=True):

    if not task.strip():
        st.warning("Please enter a task first.")
    else:

        result = detect_threat(task, attack_type)

        events = run_simulation(
            task,
            attack_type,
            result["detected"]
        )

        st.divider()
        st.subheader("🔍 Security Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Risk Level",
                result["risk"]
            )

        with col2:
            st.metric(
                "Threat Detected",
                "YES" if result["detected"] else "NO"
            )

        with col3:
            st.metric(
                "Affected Agent",
                "Research Agent"
            )

        st.divider()

        if result["detected"]:
            st.error(
                f"🚨 {attack_type} detected!"
            )

            if result["matched_keywords"]:
                st.write("**Detected indicators:**")
                for keyword in result["matched_keywords"]:
                    st.code(keyword)

        else:
            st.success(
                "✅ No adversarial behavior detected."
            )

        st.subheader("🤖 Agent Trajectory")

        st.write(
            "User → Orchestrator Agent → Research Agent → "
            + ("🔒 BLOCKED" if result["detected"] else "✅ COMPLETED")
        )

        st.subheader("📋 Security Event Log")

        for event in events:
            st.write("• " + event)

        st.divider()

        st.subheader("📊 Final Security Report")

        if result["detected"]:
            st.write(
                f"""
                **Attack Type:** {attack_type}

                **Risk Level:** HIGH

                **Detection Status:** Threat detected

                **Response:** Agent execution blocked

                **Security Action:** Event logged for further analysis
                """
            )
        else:
            st.write(
                """
                **Attack Type:** None detected

                **Risk Level:** LOW

                **Detection Status:** Safe

                **Response:** Agent execution allowed

                **Security Action:** Normal execution logged
                """
            )
