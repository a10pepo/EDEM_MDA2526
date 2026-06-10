import pandas as pd
import plotly.express as px
import streamlit as st

from config import load_redshift_config
from database import get_redshift_connection

st.set_page_config(page_title="Workout Analytics", layout="wide")


@st.cache_data(ttl=600)
def load_data() -> pd.DataFrame:
    config = load_redshift_config()
    conn = get_redshift_connection(config)
    try:
        df = pd.read_sql("SELECT * FROM fact_sets;", conn)
    finally:
        conn.close()

    df["start_time"] = pd.to_datetime(df["start_time"])
    df["end_time"] = pd.to_datetime(df["end_time"])
    return df


df = load_data()

st.title("🏋️ Workout History Dashboard")

if df.empty:
    st.warning("No data found in fact_sets.")
    st.stop()

# =============================================================================
# Progression Tracker
# =============================================================================
st.header("Progression Tracker")

exercise = st.selectbox(
    "Select an exercise",
    sorted(df["exercise_title"].dropna().unique()),
)

exercise_df = df[df["exercise_title"] == exercise]

col1, col2 = st.columns(2)

with col1:
    max_weight = (
        exercise_df.groupby(exercise_df["start_time"].dt.date)["weight_kg"]
        .max()
        .reset_index()
        .rename(columns={"start_time": "date"})
    )
    fig = px.line(
        max_weight, x="date", y="weight_kg",
        title=f"Max Weight Lifted Over Time — {exercise}",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    avg_weight = (
        exercise_df.groupby(exercise_df["start_time"].dt.date)["weight_kg"]
        .mean()
        .reset_index()
        .rename(columns={"start_time": "date"})
    )
    fig = px.line(
        avg_weight, x="date", y="weight_kg",
        title=f"Average Weight per Set Over Time — {exercise}",
        markers=True,
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# Training Habits
# =============================================================================
st.header("Training Habits")

col3, col4 = st.columns(2)

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

with col3:
    workouts = df.drop_duplicates(subset=["workout_id"]).copy()
    workouts["day_of_week"] = workouts["start_time"].dt.day_name()
    day_counts = (
        workouts["day_of_week"]
        .value_counts()
        .reindex(DAY_ORDER)
        .reset_index()
    )
    day_counts.columns = ["day_of_week", "count"]
    fig = px.bar(
        day_counts, x="day_of_week", y="count",
        title="Training Frequency by Day of Week",
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    workouts["hour"] = workouts["start_time"].dt.hour
    hour_counts = (
        workouts["hour"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    hour_counts.columns = ["hour", "count"]
    fig = px.bar(
        hour_counts, x="hour", y="count",
        title="Training Frequency by Hour of Day",
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# Workout Metadata
# =============================================================================
st.header("Workout Metadata")

col5, col6 = st.columns(2)

with col5:
    workouts["duration_minutes"] = (
        (workouts["end_time"] - workouts["start_time"]).dt.total_seconds() / 60
    )
    fig = px.histogram(
        workouts, x="duration_minutes",
        title="Distribution of Workout Durations (minutes)",
        nbins=20,
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    exercise_counts = df['exercise_title'].value_counts().reset_index()
    exercise_counts.columns = ['exercise_title', 'count']
    fig = px.bar(
        exercise_counts, x='exercise_title', y='count',
        title="Most Frequent Exercises Distribution")
    st.plotly_chart(fig, use_container_width=True)

# Contar cuántas veces aparece cada ejercicio en tu histórico


# Pintar el gráfico interactivo con Plotly usando 'exercise_title'

