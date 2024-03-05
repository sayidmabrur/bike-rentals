import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# helper functions
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

days_df = pd.read_csv("days_cleaned.csv")
hours_df = pd.read_csv("hours_cleaned.csv")

days_df['dteday'] = pd.to_datetime(days_df['dteday'])
hours_df['dteday'] = pd.to_datetime(hours_df['dteday'])
days_df['yr'] = days_df['yr'].astype(str)
hours_df['yr'] = hours_df['yr'].astype(str)
days_df.rename(columns={"yr":"Year", "mnth":"Month", "cnt":"Count"}, inplace=True)
hours_df.rename(columns={"yr":"Year", "hr":"Hour", "mnth":"Month", "cnt":"Count"}, inplace=True)

yearly_rentals_df = days_df.groupby("Year").Count.sum().sort_index()
seasonal_rentals_df = days_df.groupby(['Year', 'Month', 'season'])['Count'].sum().reset_index().sort_values(by=['Year', 'Month', 'season'])
temp = seasonal_rentals_df.iloc[6]
seasonal_rentals_df.iloc[6] = seasonal_rentals_df.iloc[7]
seasonal_rentals_df.iloc[7] = temp

temp = seasonal_rentals_df.iloc[14]
seasonal_rentals_df.iloc[14] = seasonal_rentals_df.iloc[15]
seasonal_rentals_df.iloc[15] = temp

temp = seasonal_rentals_df.iloc[22]
seasonal_rentals_df.iloc[22] = seasonal_rentals_df.iloc[23]
seasonal_rentals_df.iloc[23] = temp

temp = seasonal_rentals_df.iloc[30]
seasonal_rentals_df.iloc[30] = seasonal_rentals_df.iloc[31]
seasonal_rentals_df.iloc[31] = temp
seasonal_rentals_df['Season/Month'] = seasonal_rentals_df.apply(lambda row: f"{row['season']} / {row['Month']}", axis=1)
seasonal_rentals_df.drop(['season', 'Month'], axis=1, inplace=True)


monthly_rentals_df = days_df.groupby(['Year', 'Month'])['Count'].sum().reset_index()
weather_rentals_df = hours_df.groupby('weathersit')['Count'].sum().sort_values(ascending=False).reset_index()
temperature_rentals_df = hours_df.groupby('temp')['Count'].sum().reset_index()
humidity_rentals_df = hours_df.groupby('hum')['Count'].sum().reset_index()
windspeed_rentals_df = hours_df.groupby('windspeed')['Count'].sum().reset_index()

st.header('Dashboard Analisis Penyewaan Sepeda (Bike Sharing)')
st.subheader('Time Series Rentals:')

col1, col2 = st.columns(2)
with col1:
    total_rentals = days_df.Count.sum()
    st.metric("Total Rentals", value=human_format(total_rentals))

with col2:
    st.write(yearly_rentals_df)
    # st.wr/("Yearly Rentals", value=yearly_rentals)

# Mengelompokkan data berdasarkan bulan dan tahun, kemudian menghitung jumlah total penyewaan

# Membuat plot
fig, ax = plt.subplots(figsize=(18, 12))
ax = sns.lineplot(data=monthly_rentals_df, x='Month', y='Count', hue='Year', marker='o')
plt.title('Monthly Rentals (2011-2012)')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Year')
plt.grid(True)
st.pyplot(fig)

st.subheader("Seasonal Rentals")

col1, col2 = st.columns(2)
with col1:
    seasonal_count_df = days_df.groupby("season").Count.sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="Count", 
        x="season",
        data=seasonal_count_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Best Seasonal Rentals", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    st.write(seasonal_count_df)


fig, ax = plt.subplots(figsize=(20, 15))
sns.lineplot(data=seasonal_rentals_df, x='Season/Month', y='Count', hue='Year', marker='o')
plt.title('Time Series Seasonal Rentals')
plt.xlabel('Season / Month')
plt.ylabel('Total Rentals')
plt.legend(title='Year')
plt.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("Weather and Condition Rentals")

col1, col2 = st.columns(2)

with col1:
    st.write(weather_rentals_df)
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="Count", 
        x="weathersit",
        data=weather_rentals_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Best Seasonal Rentals", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


fig, axes = plt.subplots(3, 1, figsize=(10, 18))
sns.lineplot(data=temperature_rentals_df, x='temp', y='Count', ax=axes[0])
axes[0].set_title('Total Rentals Based on Temperature')
axes[0].set_xlabel('Temp')
axes[0].set_ylabel('Total Rentals')
sns.lineplot(data=humidity_rentals_df, x='hum', y='Count', color='blue', ax=axes[1])
axes[1].set_title('Total Rentals Based on Humidity')
axes[1].set_xlabel('Hum')
axes[1].set_ylabel('Total Rentals')
sns.lineplot(data=windspeed_rentals_df, x='windspeed', y='Count', color='blue', ax=axes[2])
axes[2].set_title('Total Rentals Based on Windspeed')
axes[2].set_xlabel('Windspeed')
axes[2].set_ylabel('Total Rentals')

plt.tight_layout()
st.pyplot(fig)