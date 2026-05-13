import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="AI Session Tracker",
    page_icon="📊",
    layout="wide"
)

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv(
    "database/app_sessions.csv",
    names=["App", "Start_Time", "End_Time", "Duration"]
)

df = df.dropna()

# ----------------------------
# SIDEBAR MENU
# ----------------------------
st.sidebar.title("📊 AI Tracker Menu")

menu = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "📈 Usage Analytics", "⏰ Sessions", "🧠 AI Insights"]
)

st.sidebar.markdown("---")
st.sidebar.info("🚀 Real Session Tracking System")

# ----------------------------
# OVERVIEW
# ----------------------------
if menu == "🏠 Overview":

    st.title("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("📱 Sessions", len(df))
    col2.metric("🧠 Unique Apps", df["App"].nunique())
    col3.metric("⏱️ Total Time", df["Duration"].sum())

    st.markdown("---")

    st.subheader("🏆 Top App")

    top_app = df.groupby("App")["Duration"].sum().idxmax()
    st.success(f"{top_app}")

# ----------------------------
# USAGE ANALYTICS (WITH OPTIONS INSIDE PAGE)
# ----------------------------
elif menu == "📈 Usage Analytics":

    st.title("📈 Usage Analytics")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"]
    )

    chart_data = df.groupby("App")["Duration"].sum()

    st.subheader("📊 Visualization")

    if chart_type == "Bar Chart":
        st.bar_chart(chart_data)

    elif chart_type == "Pie Chart":
        fig, ax = plt.subplots()
        chart_data.plot.pie(
            autopct="%1.1f%%",
            ax=ax
        )
        ax.set_ylabel("")
        st.pyplot(fig)

    elif chart_type == "Line Chart":
        st.line_chart(chart_data)

    elif chart_type == "Area Chart":
        st.area_chart(chart_data)

    st.markdown("---")

    st.subheader("📋 Raw Data")
    st.dataframe(df)

# ----------------------------
# SESSIONS
# ----------------------------
elif menu == "⏰ Sessions":

    st.title("⏰ Session History (Open → Close)")

    st.dataframe(df, use_container_width=True)

# ----------------------------
# AI INSIGHTS
# ----------------------------
elif menu == "🧠 AI Insights":

    st.title("🧠 AI Productivity Insights")

    productive = ["code", "chrome"]
    distraction = ["youtube", "instagram", "whatsapp"]

    def score(app):
        if any(x in app for x in productive):
            return 1
        elif any(x in app for x in distraction):
            return -1
        return 0

    df["Score"] = df["App"].apply(score)

    total_score = df["Score"].sum()

    st.metric("Productivity Score", total_score)

    if total_score > 0:
        st.success("🔥 Good productive behavior")
    else:
        st.warning("⚠️ Distracted usage detected")

    focus = int((df["App"].str.contains("code|chrome").sum() / len(df)) * 100)

    st.metric("Focus %", f"{focus}%")