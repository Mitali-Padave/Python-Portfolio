"""
Generates a realistic synthetic merchant-transaction dataset for portfolio analysis.
A deliberate, discoverable business problem is baked in (see README) so the analysis
has a genuine finding to surface, mirroring real merchant-analytics work.
"""
import pandas as pd
import numpy as np

np.random.seed(42)
N = 50000

categories = ['Restaurant', 'Retail', 'Travel', 'Grocery', 'Electronics', 'Fuel']
regions = ['North', 'South', 'East', 'West']
channels = ['In-Store', 'Online']
segments = ['Small', 'Medium', 'Large']

# base frame
df = pd.DataFrame({
    'transaction_id': np.arange(1, N + 1),
    'merchant_id': np.random.randint(1000, 3000, N),
    'category': np.random.choice(categories, N, p=[.24, .26, .10, .18, .12, .10]),
    'region': np.random.choice(regions, N, p=[.28, .24, .22, .26]),
    'channel': np.random.choice(channels, N, p=[.58, .42]),
    'merchant_segment': np.random.choice(segments, N, p=[.55, .32, .13]),
})

# transaction date across 12 months
start = pd.Timestamp('2025-07-01')
df['transaction_date'] = start + pd.to_timedelta(np.random.randint(0, 365, N), unit='D')

# transaction amount depends on category (realistic scale)
cat_mean = {'Restaurant': 850, 'Retail': 1600, 'Travel': 9500,
            'Grocery': 1200, 'Electronics': 7000, 'Fuel': 1800}
df['amount'] = df['category'].map(lambda c: max(30, np.random.gamma(2.2, cat_mean[c] / 2.2)))
df['amount'] = df['amount'].round(2)

# approval status — baseline high approval
df['status'] = np.random.choice(['Approved', 'Declined'], N, p=[.91, .09])

# ---- BAKED-IN PROBLEM (the finding) ----
# Online transactions in the Travel category have a spiking decline rate
# driven by a mis-set fraud/risk rule, quietly killing high-value revenue.
mask = (df['channel'] == 'Online') & (df['category'] == 'Travel')
flip = np.random.rand(N) < 0.55  # 55% of these get forced to Declined
df.loc[mask & flip, 'status'] = 'Declined'

# a little messiness to clean (realism)
df.loc[df.sample(frac=0.02, random_state=1).index, 'region'] = np.nan
df.loc[df.sample(frac=0.015, random_state=2).index, 'category'] = df['category'].str.upper()  # inconsistent case
dupes = df.sample(300, random_state=3)
df = pd.concat([df, dupes], ignore_index=True)  # duplicate rows

df.to_csv('merchant_transactions.csv', index=False)
print(f"Wrote merchant_transactions.csv: {len(df)} rows")
