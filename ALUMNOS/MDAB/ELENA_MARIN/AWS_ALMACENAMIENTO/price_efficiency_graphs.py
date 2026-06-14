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

print("🎨 Redesigning charts for maximum readability...")

# Set clean visual theme
sns.set_theme(style="whitegrid")

# --- DATA EXTRACTION ---
query_month = """
SELECT TO_CHAR(fecha, 'YYYY-MM') AS month, SUM(precio_individual) AS total_value
FROM wellhub_trainings
WHERE tipo_registro = 'Checkin' AND estado = 'COMPLETED'
GROUP BY month ORDER BY month;
"""
df_month = pd.read_sql(query_month, connection_url)

query_gym = """
SELECT gimnasio AS gym, SUM(precio_individual) AS gym_value, COUNT(*) AS visits
FROM wellhub_trainings
WHERE tipo_registro = 'Checkin' AND estado = 'COMPLETED'
GROUP BY gym ORDER BY gym_value DESC;
"""
df_gym = pd.read_sql(query_gym, connection_url)


# 📊 CHART 1: Monthly Market Value (Vertical Bars)
plt.figure(figsize=(12, 6))
barplot_month = sns.barplot(data=df_month, x='month', y='total_value', palette='Blues_r')

# Add values on top of each bar for clarity
for p in barplot_month.patches:
    barplot_month.annotate(f"{p.get_height():.0f}€", 
                           (p.get_x() + p.get_width() / 2., p.get_height()), 
                           ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontsize=10, fontweight='bold')

plt.title('Total Value of Attended Classes at Market Price (RRP Equivalent)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Equivalent Total Value (€)', fontsize=12)
plt.xticks(rotation=45)
plt.ylim(0, df_month['total_value'].max() * 1.15) # Leave space at the top for labels
plt.tight_layout()
plt.savefig('monthly_market_value.png', dpi=300)


# 📊 CHART 2: Value Distribution per Gym (Horizontal Bars - Clean Layout)
plt.figure(figsize=(12, 8)) # Taller figure size so gym names have room to breathe
barplot_gym = sns.barplot(data=df_gym, x='gym_value', y='gym', palette='viridis')

# Add value and visit count at the end of each horizontal bar
for i, p in enumerate(barplot_gym.patches):
    value = df_gym.iloc[i]['gym_value']
    visits = df_gym.iloc[i]['visits']
    barplot_gym.annotate(f" {value:.0f}€ ({visits} vis.)", 
                         (p.get_width(), p.get_y() + p.get_height() / 2.), 
                         va='center', ha='left', fontsize=10, fontweight='bold')

plt.title('Subscription Cost-Efficiency per Gym (Accumulated Value and Total Visits)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Equivalent Accumulated Value (€)', fontsize=12)
plt.ylabel('Gym / Fitness Center', fontsize=12)
plt.xlim(0, df_gym['gym_value'].max() * 1.15) # Leave space on the right for labels
plt.tight_layout()
plt.savefig('gym_efficiency_report.png', dpi=300)

print("\n🚀 Charts successfully updated!")
print("🖼️  'monthly_market_value.png' -> Shows the RRP value you would have paid without a flat rate.")
print("🖼️  'gym_efficiency_report.png' -> Perfectly ordered, highly legible breakdown of your gym usage.")