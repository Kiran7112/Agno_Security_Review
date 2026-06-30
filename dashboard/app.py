import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Agno Security Dashboard", layout="wide")

API_URL = "http://localhost:8000/api/v1"

st.title("🛡️ Agno Security Review Dashboard")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Overview", "Statistics", "Compliance", "Developers", "Reports"])

try:
    stats_response = requests.get(f"{API_URL}/stats")
    stats = stats_response.json() if stats_response.status_code == 200 else {}
except:
    stats = {}

if page == "Overview":
    st.header("Security Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Reviews", stats.get("total_reviews", 0))

    with col2:
        st.metric("Total Issues", stats.get("total_issues", 0), delta=None)

    with col3:
        st.metric("Critical", stats.get("critical", 0), delta_color="inverse")

    with col4:
        st.metric("High", stats.get("high", 0), delta_color="inverse")

    st.subheader("Recent Issues")

    try:
        audits_response = requests.get(f"{API_URL}/audits?limit=10")
        audits = audits_response.json() if audits_response.status_code == 200 else []

        if audits:
            df = pd.DataFrame(audits)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No audits found")
    except Exception as e:
        st.error(f"Error loading audits: {e}")

elif page == "Statistics":
    st.header("Statistics & Trends")

    try:
        metrics_response = requests.get(f"{API_URL}/metrics")
        metrics = metrics_response.json() if metrics_response.status_code == 200 else {}

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Vulnerability Breakdown")
            vulnerabilities = metrics.get("vulnerabilities", {})
            vuln_data = vulnerabilities.get("vulnerability_types", {})

            if vuln_data:
                st.bar_chart(vuln_data)
            else:
                st.info("No vulnerability data")

        with col2:
            st.subheader("ROI Metrics")
            roi = metrics.get("roi", {})

            col2_1, col2_2 = st.columns(2)

            with col2_1:
                st.metric("Hours Saved", f"{roi.get('total_analysis_hours', 0):.1f}")

            with col2_2:
                st.metric("Estimated Savings", f"${roi.get('estimated_savings', 0):.0f}")

    except Exception as e:
        st.error(f"Error loading metrics: {e}")

elif page == "Compliance":
    st.header("Compliance Reports")

    standard = st.selectbox("Select Standard", ["SOC2", "HIPAA", "GDPR", "PCI-DSS"])

    if st.button("Generate Report"):
        try:
            response = requests.post(f"{API_URL}/compliance/{standard}/generate")

            if response.status_code == 200:
                report = response.json()
                st.success("Report generated successfully!")

                report_data = report.get("report", {})
                st.metric("Compliance Status", f"{report_data.get('percentage_compliant', 0):.0f}%")

                st.subheader("Requirements Met")
                for req in report_data.get("requirements_met", []):
                    st.success(req)

                if report_data.get("requirements_failed"):
                    st.subheader("Requirements Failed")
                    for req in report_data.get("requirements_failed", []):
                        st.error(req)
            else:
                st.error("Failed to generate report")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Previous Reports")

    try:
        reports_response = requests.get(f"{API_URL}/compliance")
        reports = reports_response.json() if reports_response.status_code == 200 else []

        if reports:
            reports_df = pd.DataFrame(reports)
            st.dataframe(reports_df, use_container_width=True)
        else:
            st.info("No compliance reports found")
    except Exception as e:
        st.error(f"Error loading reports: {e}")

elif page == "Developers":
    st.header("Developer Metrics")

    try:
        leaderboard_response = requests.get(f"{API_URL}/metrics/leaderboard")
        leaderboard_data = leaderboard_response.json() if leaderboard_response.status_code == 200 else {}
        leaderboard = leaderboard_data.get("leaderboard", [])

        if leaderboard:
            df = pd.DataFrame(leaderboard)
            st.dataframe(df, use_container_width=True)

            st.subheader("Security Score Distribution")
            scores = {dev["developer"]: dev["security_score"] for dev in leaderboard}
            st.bar_chart(scores)
        else:
            st.info("No developer data found")
    except Exception as e:
        st.error(f"Error loading developer metrics: {e}")

elif page == "Reports":
    st.header("Reports")

    report_type = st.selectbox("Report Type", ["Daily", "Weekly", "Compliance"])

    if st.button("Generate Report"):
        if report_type == "Daily":
            try:
                response = requests.get(f"{API_URL}/reports/daily")

                if response.status_code == 200:
                    report = response.json()
                    st.markdown(report.get("report", ""))
                else:
                    st.error("Failed to generate daily report")
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.info("🛡️ Agno Security Review\nv1.0.0")
