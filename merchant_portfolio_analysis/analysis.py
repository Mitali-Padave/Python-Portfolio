"""
Merchant Portfolio Performance Analysis
---------------------------------------
Goal: analyse a merchant transaction portfolio to measure performance and
diagnose what is driving lost (declined) revenue.

Approach: clean the data, compute portfolio KPIs, then investigate the decline
rate by segment to isolate the root cause rather than reporting the top-line number.

Author: Mitali Padave
"""
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

# ---------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------
df = pd.read_csv('merchant_transactions.csv', parse_dates=['transaction_date'])
print(f"Loaded {len(df):,} rows")

# ---------------------------------------------------------------
# 2. CLEAN  (verify the data before trusting it)
# ---------------------------------------------------------------
before = len(df)

# 2a. drop exact duplicate transactions
df = df.drop_duplicates(subset='transaction_id')
print(f"Removed {before - len(df):,} duplicate transactions")

# 2b. standardise inconsistent category casing (e.g. 'RETAIL' -> 'Retail')
df['category'] = df['category'].str.title()

# 2c. handle missing region
missing_region = df['region'].isna().sum()
df['region'] = df['region'].fillna('Unknown')
print(f"Filled {missing_region:,} missing region values as 'Unknown'")

# derived fields
df['month'] = df['transaction_date'].dt.to_period('M').astype(str)
df['is_declined'] = (df['status'] == 'Declined').astype(int)
df['approved_amount'] = df['amount'].where(df['status'] == 'Approved', 0)

# ---------------------------------------------------------------
# 3. PORTFOLIO KPIs
# ---------------------------------------------------------------
total_txns = len(df)
approved_rev = df['approved_amount'].sum()
overall_decline = df['is_declined'].mean()
# revenue lost = value of declined transactions
lost_rev = df.loc[df['status'] == 'Declined', 'amount'].sum()

print("\n===== PORTFOLIO KPIs =====")
print(f"Total transactions   : {total_txns:,}")
print(f"Approved revenue     : ${approved_rev:,.0f}")
print(f"Overall decline rate : {overall_decline:.1%}")
print(f"Declined (lost) value: ${lost_rev:,.0f}")

# ---------------------------------------------------------------
# 4. INVESTIGATION — why are transactions declining?
#    Test the obvious dimensions, then drill into the interaction.
# ---------------------------------------------------------------
print("\n===== DECLINE RATE BY DIMENSION =====")

by_cat = df.groupby('category')['is_declined'].mean().sort_values(ascending=False)
by_channel = df.groupby('channel')['is_declined'].mean().sort_values(ascending=False)
print("\nBy category:\n", (by_cat * 100).round(1))
print("\nBy channel:\n", (by_channel * 100).round(1))

# category alone and channel alone look only mildly elevated —
# drill into the INTERACTION of channel x category
pivot = (df.pivot_table(index='category', columns='channel',
                        values='is_declined', aggfunc='mean') * 100).round(1)
print("\nDecline rate (%) by category x channel:\n", pivot)

# isolate the worst cell
inter = (df.groupby(['category', 'channel'])
           .agg(txns=('transaction_id', 'count'),
                decline_rate=('is_declined', 'mean'),
                lost_value=('amount', lambda s: s[df.loc[s.index, 'status'] == 'Declined'].sum()))
           .reset_index()
           .sort_values('decline_rate', ascending=False))
worst = inter.iloc[0]
print("\n===== ROOT CAUSE =====")
print(f"Worst segment: {worst['category']} / {worst['channel']}")
print(f"  Decline rate : {worst['decline_rate']:.1%}")
print(f"  Transactions : {int(worst['txns']):,}")
print(f"  Lost value   : ${worst['lost_value']:,.0f}")

baseline = df.loc[~((df['category'] == worst['category']) & (df['channel'] == worst['channel'])),
                  'is_declined'].mean()
print(f"  Baseline decline rate elsewhere: {baseline:.1%}")
print(f"  => This one segment declines ~{worst['decline_rate']/baseline:.1f}x the rest of the portfolio.")

# quantify the opportunity: if this segment declined at the baseline rate instead
seg = df[(df['category'] == worst['category']) & (df['channel'] == worst['channel'])]
excess_declines = int((worst['decline_rate'] - baseline) * len(seg))
recoverable = seg.loc[seg['status'] == 'Declined', 'amount'].mean() * excess_declines
print(f"  Est. recoverable revenue if fixed to baseline: ${recoverable:,.0f}")

# ---------------------------------------------------------------
# 5. VISUALS
# ---------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')

# Chart 1: decline rate by category x channel (the key finding)
ax = pivot.plot(kind='bar', figsize=(9, 5), color=['#4C72B0', '#DD8452'])
ax.set_ylabel('Decline rate (%)')
ax.set_title('Decline Rate by Category x Channel — Online Travel is the outlier')
ax.set_xlabel('')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('chart_decline_by_segment.png', dpi=120)
plt.close()

# Chart 2: approved revenue by category
rev = df.groupby('category')['approved_amount'].sum().sort_values(ascending=False)
ax = rev.plot(kind='bar', figsize=(9, 5), color='#4C72B0')
ax.set_ylabel('Approved revenue ($)')
ax.set_title('Approved Revenue by Merchant Category')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('chart_revenue_by_category.png', dpi=120)
plt.close()

# Chart 3: monthly approved revenue trend
monthly = df.groupby('month')['approved_amount'].sum()
ax = monthly.plot(kind='line', marker='o', figsize=(9, 5), color='#4C72B0')
ax.set_ylabel('Approved revenue ($)')
ax.set_title('Monthly Approved Revenue Trend')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('chart_monthly_trend.png', dpi=120)
plt.close()

print("\nSaved 3 charts. Analysis complete.")
