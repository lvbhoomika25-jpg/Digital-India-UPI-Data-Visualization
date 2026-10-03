# =========================================================
# DIGITAL INDIA: GROWTH OF UPI TRANSACTIONS
# COMPLETE DVP PROJECT CODE
# =========================================================

# -------------------------
# IMPORT LIBRARIES
# -------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# LOAD DATASET
# -------------------------

df = pd.read_csv("upi_transactions_india.csv")

# -------------------------
# DISPLAY BASIC INFORMATION
# -------------------------

print("\nFIRST 5 ROWS")
print(df.head())

print("\nDATASET INFO")
print(df.info())

print("\nSTATISTICAL SUMMARY")
print(df.describe())

print("\nNULL VALUES")
print(df.isnull().sum())

print("\nDUPLICATE VALUES")
print(df.duplicated().sum())

# =========================================================
# DATA PREPROCESSING
# =========================================================

month_map = {
    'January':1,
    'February':2,
    'March':3,
    'April':4,
    'May':5,
    'June':6,
    'July':7,
    'August':8,
    'September':9,
    'October':10,
    'November':11,
    'December':12
}

df['Month_Num'] = df['Month'].map(month_map)

df['Date'] = pd.to_datetime(
    df[['Year', 'Month_Num']]
    .rename(columns={'Year':'year', 'Month_Num':'month'})
    .assign(day=1)
)

# =========================================================
# OUTLIER DETECTION
# =========================================================

Q1 = df['UPI_Transactions_Million'].quantile(0.25)

Q3 = df['UPI_Transactions_Million'].quantile(0.75)

IQR = Q3 - Q1

outliers = df[
    (df['UPI_Transactions_Million'] < Q1 - 1.5 * IQR) |
    (df['UPI_Transactions_Million'] > Q3 + 1.5 * IQR)
]

print("\nNUMBER OF OUTLIERS")
print(len(outliers))

# =========================================================
# FIGURE 5.1 BAR CHART
# =========================================================

annual = (
    df.groupby('Year')['UPI_Transactions_Million']
    .sum()
    .reset_index()
)

plt.figure(figsize=(12,6))

bars = plt.bar(
    annual['Year'].astype(str),
    annual['UPI_Transactions_Million']
)

for bar, val in zip(bars, annual['UPI_Transactions_Million']):
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 50,
        f'{val:.0f}M',
        ha='center'
    )

plt.title(
    'Fig 5.1: Year-wise Total UPI Transactions (2018-2025)'
)

plt.xlabel('Year')
plt.ylabel('Transactions (Millions)')

plt.tight_layout()

plt.savefig('fig5_1_bar_chart.png')

plt.show()

# =========================================================
# FIGURE 5.2 HISTOGRAM
# =========================================================

fig, axes = plt.subplots(1,3, figsize=(16,5))

fig.suptitle(
    'Fig 5.2: Distribution of UPI Metrics',
    fontsize=14
)

axes[0].hist(
    df['UPI_Transactions_Million'],
    bins=20
)

axes[0].set_title('UPI Transactions')

axes[1].hist(
    df['Success_Rate'],
    bins=15
)

axes[1].set_title('Success Rate')

axes[2].hist(
    df['Active_Users_Million'],
    bins=20
)

axes[2].set_title('Active Users')

plt.tight_layout()

plt.savefig('fig5_2_histogram.png')

plt.show()

# =========================================================
# FIGURE 5.3 BOXPLOT
# =========================================================

plt.figure(figsize=(14,7))

sns.boxplot(
    data=df,
    x='Year',
    y='UPI_Transactions_Million'
)

plt.title(
    'Fig 5.3: Monthly Transaction Distribution by Year'
)

plt.xlabel('Year')
plt.ylabel('Transactions (Millions)')

plt.tight_layout()

plt.savefig('fig5_3_boxplot.png')

plt.show()

# =========================================================
# FIGURE 5.4 HEATMAP
# =========================================================

num_cols = [
    'UPI_Transactions_Million',
    'Transaction_Value_Crore',
    'Merchant_Transactions',
    'Peer_to_Peer_Transactions',
    'Success_Rate',
    'Failed_Transactions',
    'Active_Users_Million'
]

corr = df[num_cols].corr()

plt.figure(figsize=(10,8))

sns.heatmap(
    corr,
    annot=True,
    cmap='RdYlGn',
    fmt='.2f'
)

plt.title(
    'Fig 5.4: Correlation Heatmap of UPI Features'
)

plt.tight_layout()

plt.savefig('fig5_4_heatmap.png')

plt.show()

# =========================================================
# FIGURE 5.5 PIE CHART
# =========================================================

app_share = (
    df.groupby('App_Name')
    ['UPI_Transactions_Million']
    .sum()
)

plt.figure(figsize=(8,8))

plt.pie(
    app_share,
    labels=app_share.index,
    autopct='%1.1f%%'
)

plt.title(
    'Fig 5.5: App-wise Market Share of UPI Transactions'
)

plt.tight_layout()

plt.savefig('fig5_5_pie_chart.png')

plt.show()

# =========================================================
# FIGURE 5.6 LINE GRAPH
# =========================================================

monthly = (
    df.groupby(['Year','Month_Num'])
    ['UPI_Transactions_Million']
    .sum()
    .reset_index()
)

monthly['Date'] = pd.to_datetime(
    monthly[['Year','Month_Num']]
    .rename(columns={'Year':'year','Month_Num':'month'})
    .assign(day=1)
)

plt.figure(figsize=(14,6))

plt.plot(
    monthly['Date'],
    monthly['UPI_Transactions_Million'],
    marker='o'
)

plt.axvspan(
    pd.Timestamp('2020-03-01'),
    pd.Timestamp('2020-06-01'),
    alpha=0.3
)

plt.title(
    'Fig 5.6: Monthly UPI Growth Trend'
)

plt.xlabel('Date')
plt.ylabel('Transactions (Millions)')

plt.tight_layout()

plt.savefig('fig5_6_line_graph.png')

plt.show()

# =========================================================
# FIGURE 5.7 SUCCESS RATE GRAPH
# =========================================================

success = (
    df.groupby(['Year','Month_Num'])
    ['Success_Rate']
    .mean()
    .reset_index()
)

success['Date'] = pd.to_datetime(
    success[['Year','Month_Num']]
    .rename(columns={'Year':'year','Month_Num':'month'})
    .assign(day=1)
)

plt.figure(figsize=(14,6))

plt.plot(
    success['Date'],
    success['Success_Rate'],
    marker='o'
)

plt.title(
    'Fig 5.7: Success Rate Improvement (2018-2025)'
)

plt.xlabel('Date')
plt.ylabel('Success Rate (%)')

plt.tight_layout()

plt.savefig('fig5_7_success_rate.png')

plt.show()

# =========================================================
# FIGURE 6.1 STATE BAR CHART
# =========================================================

state_df = (
    df.groupby('State')
    ['UPI_Transactions_Million']
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

state_df.plot(kind='bar')

plt.title(
    'Fig 6.1: Top States by Transaction Volume'
)

plt.xlabel('State')
plt.ylabel('Transactions (Millions)')

plt.tight_layout()

plt.savefig('fig6_1_state_chart.png')

plt.show()

# =========================================================
# FIGURE 6.2 STACKED BAR CHART
# =========================================================

yearly = df.groupby('Year')[
    [
        'Merchant_Transactions',
        'Peer_to_Peer_Transactions'
    ]
].sum()

yearly.plot(
    kind='bar',
    stacked=True,
    figsize=(12,6)
)

plt.title(
    'Fig 6.2: Merchant vs P2P Transactions'
)

plt.xlabel('Year')
plt.ylabel('Transactions (Millions)')

plt.tight_layout()

plt.savefig('fig6_2_stacked_bar.png')

plt.show()

# =========================================================
# CORRELATION MATRIX
# =========================================================

print("\nCORRELATION MATRIX")
print(corr)

# =========================================================
# YEAR-WISE SUMMARY
# =========================================================

year_summary = df.groupby('Year').agg({
    'UPI_Transactions_Million':'sum',
    'Transaction_Value_Crore':'sum',
    'Success_Rate':'mean',
    'Active_Users_Million':'sum'
})

print("\nYEAR-WISE SUMMARY")
print(year_summary)

# =========================================================
# APP-WISE SUMMARY
# =========================================================

app_summary = (
    df.groupby('App_Name')
    ['UPI_Transactions_Million']
    .sum()
)

print("\nAPP-WISE SUMMARY")
print(app_summary)

# =========================================================
# STATE-WISE SUMMARY
# =========================================================

state_summary = (
    df.groupby('State')
    ['UPI_Transactions_Million']
    .sum()
)

print("\nSTATE-WISE SUMMARY")
print(state_summary)

# =========================================================
# END OF PROJECT
# =========================================================

print("\nPROJECT EXECUTED SUCCESSFULLY")
