import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

# 1. Connect to the RDS Database
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connection_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

print("📊 Analyzing training habits and generating new insights...")

# Set visual theme
sns.set_theme(style="whitegrid")

# --- DATA EXTRACTION ---
# We extract the day of the week and the hour from the 'fecha' column
# --- DATA EXTRACTION WITH TIMEZONE CORRECTION ---
# We convert the UTC timestamp to Spain's local time ('Europe/Madrid')
query_habits = """
SELECT 
    TO_CHAR(fecha AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Madrid', 'Day') AS day_of_week,
    EXTRACT(DOW FROM fecha AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Madrid') AS day_num,
    EXTRACT(HOUR FROM fecha AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Madrid') AS training_hour
FROM wellhub_trainings
WHERE tipo_registro = 'Checkin' AND estado = 'COMPLETED';
"""

df = pd.read_sql(query_habits, connection_url)

# Clean up day names (remove trailing spaces that PostgreSQL adds)
df['day_of_week'] = df['day_of_week'].str.strip()

# Map to order days logically starting on Monday
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# 📅 CHART 1: Attendance by Day of the Week (Bar Chart)
plt.figure(figsize=(10, 5))
# Calculate counts per day and reindex to guarantee Monday to Sunday order
df_days = df['day_of_week'].value_counts().reindex(days_order).fillna(0).reset_index()
df_days.columns = ['Day of the Week', 'Total Checkins']

barplot_days = sns.barplot(data=df_days, x='Day of the Week', y='Total Checkins', palette='magma')

# Add values on top of bars
for p in barplot_days.patches:
    barplot_days.annotate(f"{p.get_height():.0f}", 
                           (p.get_x() + p.get_width() / 2., p.get_height()), 
                           ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')

plt.title('Weekly Routine: Attendance Distribution by Day of the Week', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Number of Workouts', fontsize=12)
plt.ylim(0, df_days['Total Checkins'].max() * 1.15)
plt.tight_layout()
plt.savefig('attendance_by_day.png', dpi=300)


# ⏰ CHART 2: Peak Training Hours (Line/Area Chart)
plt.figure(figsize=(10, 5))
# Group by hour and count sessions
df_hours = df['training_hour'].value_counts().sort_index().reset_index()
df_hours.columns = ['Hour of the Day', 'Total Checkins']

# Plotting a smooth line chart with a shaded area underneath
plt.plot(df_hours['Hour of the Day'], df_hours['Total Checkins'], marker='o', color='#1f77b4', linewidth=2.5)
plt.fill_between(df_hours['Hour of the Day'], df_hours['Total Checkins'], color='#1f77b4', alpha=0.15)

plt.title('Hourly Habits: Peak Training Times Throughout the Day', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Hour of the Day (24h Format)', fontsize=12)
plt.ylabel('Number of Workouts', fontsize=12)
plt.xticks(range(0, 24)) # Show every hour slot on X axis
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('attendance_by_hour.png', dpi=300)

print("\n🚀 New behavioral charts successfully created!")
print("🖼️  'attendance_by_day.png'  -> Discover your favorite days to exercise.")
print("🖼️  'attendance_by_hour.png' -> See your preferred time slots visualized.")