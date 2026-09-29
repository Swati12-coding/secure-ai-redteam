import streamlit as st
import pandas as pd
from detector import detect_threat
from simulator import run_simulation

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Secure AI Red-Team Sandbox",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------

st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    .hero {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(
            135deg,
            #111827,
            #1f2937
        );
        border: 1px solid #374151;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin-bottom: 0.3rem;
    }

    .status-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #374151;
        background: #111827;
        text-align: center;
    }

    .timeline {
        padding: 0.8rem;
        margin: 0.4rem 0;
        border-left: 3px solid #6b7280;
        background: #111827;
        border-radius: 5px;
    }

    .blocked {
        padding: 1rem;
        border-radius: 10px;
        background: #3f1d1d;
        border: 1px solid #ef4444;
    }

    .allowed {
        padding: 1rem;
        border-radius: 10px;
        background: #14291c;
        border: 1px solid #22c55e;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<div class="hero">

# 🛡️ Secure AI Red-Team Sandbox

**Controlled AI security testing for adversarial inputs and multi-agent workflows.**

Simulate security scenarios, monitor agent behavior, detect threats,
and visualize containment decisions.

</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("⚙️ Test Configuration")

    attack_type = st.selectbox(
        "Security Test",
        [
            "Prompt Injection",
            "Data Leakage",
            "Behavioral Drift"
        ]
    )

    st.divider()

    st.markdown("### Test Environment")

    st.success("🟢 Sandbox Active")

    st.caption(
        "This prototype uses simulated agents and "
        "rule-based threat detection."
    )

# -----------------------------
# INPUT SECTION
# -----------------------------

st.subheader("🎯 Security Test")

task = st.text_area(
    "Enter AI Task / Test Input",
    placeholder=(
        "Example: Summarize this customer support ticket..."
    ),
    height=130
)

run_test = st.button(
    "🚀 RUN SECURITY TEST",
    use_container_width=True
)

# -----------------------------
# RUN ANALYSIS
# -----------------------------

if run_test:

    if not task.strip():

        st.warning("Please enter a task before running the test.")

    else:

        result = detect_threat(
            task,
            attack_type
        )

        events = run_simulation(
            task,
            attack_type,
            result["detected"]
        )

        # -----------------------------
        # CALCULATE SECURITY SCORE
        # -----------------------------

        if result["detected"]:

            if attack_type == "Prompt Injection":
                score = 92
            elif attack_type == "Data Leakage":
                score = 96
            else:
                score = 85

            risk = "HIGH"
            decision = "BLOCKED"

        else:

            score = 12
            risk = "LOW"
            decision = "ALLOWED"

        # -----------------------------
        # TOP METRICS
        # -----------------------------

        st.divider()

        st.subheader("📊 Security Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Security Risk",
                risk
            )

        with col2:
            st.metric(
                "Security Score",
                f"{score}/100"
            )

        with col3:
            st.metric(
                "Threat Detected",
                "YES" if result["detected"] else "NO"
            )

        with col4:
            st.metric(
                "Decision",
                decision
            )

        # -----------------------------
        # ATTACK INFORMATION
        # -----------------------------

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("🎯 Attack Analysis")

            st.write(
                f"**Attack Type:** {attack_type}"
            )

            st.write(
                f"**Affected Agent:** Research Agent"
            )

            if result["detected"]:

                st.error(
                    "🚨 Adversarial behavior detected"
                )

                if result["matched_keywords"]:

                    st.write("**Detection indicators:**")

                    for keyword in result["matched_keywords"]:
                        st.code(keyword)

            else:

                st.success(
                    "✅ No threat indicators detected"
                )

        with right:

            st.subheader("🤖 Agent Workflow")

            st.write("👤 **User**")

            st.write("↓")

            st.write("🧠 **Orchestrator Agent**")

            st.write("↓")

            st.write("🔬 **Research Agent**")

            st.write("↓")

            if result["detected"]:

                st.error("🔒 SECURITY LAYER → BLOCKED")

            else:

                st.success("🟢 SECURITY LAYER → ALLOWED")

        # -----------------------------
        # EVENT TIMELINE
        # -----------------------------

        st.divider()

        st.subheader("📜 Security Event Timeline")

        for index, event in enumerate(events, start=1):

            st.markdown(
                f"""
                <div class="timeline">
                    <b>Event {index}</b><br>
                    {event}
                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # DECISION PANEL
        # -----------------------------

        st.divider()

        st.subheader("🔐 Security Decision")

        if result["detected"]:

            st.markdown(
                """
                <div class="blocked">

                ### 🔴 EXECUTION BLOCKED

                The security layer detected indicators
                associated with the selected adversarial scenario.

                **Action taken:**
                - Agent execution blocked
                - Security event logged
                - Threat indicators recorded

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="allowed">

                ### 🟢 EXECUTION ALLOWED

                No configured threat indicators were detected.

                **Action taken:**
                - Agent execution allowed
                - Normal event logged

                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # REPORT
        # -----------------------------

        st.divider()

        st.subheader("🧾 Security Report")

        report_data = {
            "Metric": [
                "Attack Type",
                "Risk Level",
                "Security Score",
                "Threat Detected",
                "Affected Agent",
                "Final Decision"
            ],
            "Result": [
                attack_type,
                risk,
                f"{score}/100",
                "YES" if result["detected"] else "NO",
                "Research Agent",
                decision
            ]
        }

        report_df = pd.DataFrame(report_data)

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # DOWNLOAD REPORT
        # -----------------------------

        report_text = f"""
SECURE AI RED-TEAM SANDBOX
===========================

Attack Type: {attack_type}
Risk Level: {risk}
Security Score: {score}/100
Threat Detected: {"YES" if result["detected"] else "NO"}
Affected Agent: Research Agent
Final Decision: {decision}

SECURITY EVENTS
---------------

"""

        report_text += "\n".join(
            f"- {event}"
            for event in events
        )

        st.download_button(
            "⬇️ Download Security Report",
            report_text,
            file_name="security_report.txt",
            mime="text/plain"
        )

else:

    # -----------------------------
    # EMPTY STATE
    # -----------------------------

    st.divider()

    st.info(
        "👆 Enter a test input and click "
        "**RUN SECURITY TEST** to begin."
    )

    st.subheader("🧪 Available Security Scenarios")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            ### 💉 Prompt Injection

            Detect attempts to manipulate an AI agent
            through conflicting instructions.
            """
        )

    with c2:
        st.markdown(
            """
            ### 🔐 Data Leakage

            Detect simulated attempts to expose
            sensitive information.
            """
        )

    with c3:
        st.markdown(
            """
            ### 🧠 Behavioral Drift

            Detect simulated changes to an agent's
            intended behavior.
            """
        )
            
