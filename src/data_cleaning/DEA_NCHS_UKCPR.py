import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import math
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Load datasets
nchs = pd.read_csv(os.path.join(BASE_DIR, "data", "NCHS_Mortality_Clean.csv"))
dea = pd.read_csv(os.path.join(BASE_DIR, "data", "dea_full_interpolated.csv"))
ukcpr = pd.read_csv(os.path.join(BASE_DIR, "data", "UKCPR_cleaned.csv"))

# Add state abbrev to NCHS
state_map = {
    'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR', 'CALIFORNIA': 'CA',
    'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA',
    'HAWAII': 'HI', 'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
    'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS', 'MISSOURI': 'MO',
    'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', 'OHIO': 'OH',
    'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN', 'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT',
    'VIRGINIA': 'VA', 'WASHINGTON': 'WA', 'WEST VIRGINIA': 'WV', 'WISCONSIN': 'WI', 'WYOMING': 'WY',
    'DISTRICT OF COLUMBIA': 'DC'
}


# Remove national data and DC from NCHS since DEA data is state-level
nchs = nchs[(nchs['state'] != 'United States')].reset_index(drop=True)
# nchs = nchs[(nchs['state'] != 'DC')].reset_index(drop=True)# Strip spaces and force uppercase before filtering
nchs = nchs[nchs['state'].str.strip().str.upper() != 'DC'].reset_index(drop=True)

# Verify it worked
# print(f"Remaining states: {nchs['state'].unique()}")
# Map states
nchs['state'] = nchs['state'].str.upper().str.strip()
nchs['state'] = nchs['state'].map(state_map)

# Remove 1999 from NCHS since DEA data starts in 2000
nchs = nchs[nchs['year'] >= 2000].reset_index(drop=True)

# Get rid of DC
nchs = nchs.loc[nchs['state'] != "DC"].copy().reset_index(drop=True)
# Drop 1999 from UKCPR
ukcpr = ukcpr.loc[ukcpr.year >= 2000].reset_index(drop=True)

# Join NCHS and DEA on state and year
nchs_dea = pd.merge(
    nchs, 
    dea, 
    on=['year', 'state'], 
    how='left'
)

missing_count = nchs_dea['oxy_gms'].isna().sum()
if missing_count > 0:
    print(f"Warning: {missing_count} rows in NCHS did not find matching DEA data.")
else:
    print("Perfect match! No missing supply data in the final merge.")

# Convert hydro_gms, oxy_gms to be rate per 100k population
nchs_dea['hydro_gms'] = (nchs_dea['hydro_gms'] / nchs_dea['population']) * 100000 
nchs_dea['oxy_gms'] = (nchs_dea['oxy_gms'] / nchs_dea['population']) * 100000
nchs_dea['fent_gms'] = (nchs_dea['fent_gms'] / nchs_dea['population']) * 100000

# Merge with UKCPR on state and year
df_final = pd.merge(
    nchs_dea,
    ukcpr,
    left_on=['year', 'state'],
    right_on=['year', 'state_abbr'],
    how = 'left'
)

# Save Unscaled DataFrame for Before/After snapshots, schemas
df_final.to_csv(os.path.join(BASE_DIR, "data", "death_rate_unscaled.csv"), index=False)

# Distributions before scaling
continuous_vars = ['oxy_gms', 'hydro_gms', 'fent_gms', 
                   'gsp', 'unempl_rate', 'min_wage', 'snap_rate',
                   'poverty_rate', 'medicaid_rate',
                   'death_rate']

def plot_unscaled_hist(df, columns, cols_per_row=3):
    rows = math.ceil(len(columns) / cols_per_row)
    plt.figure(figsize=(5 * cols_per_row, 4 * rows))
    
    for i, col in enumerate(columns):
        plt.subplot(rows, cols_per_row, i + 1)
        sns.histplot(df[col].dropna(), kde=False, color='teal', bins=50) 
        plt.title(f'Unscaled Distribution: {col}')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
    
    plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "unscaled_histograms.png"), dpi=300) # Save high-res version
    # plt.show()

plot_unscaled_hist(df_final, continuous_vars)

# Feature Scaling

# log transform the skewed features
df_final['log_oxy'] = np.log1p(df_final['oxy_gms'])
df_final['log_hydro'] = np.log1p(df_final['hydro_gms'])
df_final['log_fent'] = np.log1p(df_final['fent_gms'])
df_final['log_gsp'] = np.log1p(df_final['gsp'])
df_final['log_death_rate'] = np.log1p(df_final['death_rate'])
df_final['log_min_wage'] = np.log1p(df_final['min_wage'])
df_final['log_unempl_rate'] = np.log1p(df_final['unempl_rate'])
df_final['log_medicaid_rate'] = np.log1p(df_final['medicaid_rate'])

# separate features
continuous_vars = ['log_oxy', 'log_hydro', 'log_fent',
                   'log_gsp', 'log_unempl_rate', 'log_min_wage', 'snap_rate',
                   'poverty_rate','log_medicaid_rate',
                   'log_death_rate']

# put everything in common range
scaler = StandardScaler()
df_final[continuous_vars] = scaler.fit_transform(df_final[continuous_vars])

def plot_scaled_hist(df, columns, cols_per_row=3):
    rows = math.ceil(len(columns) / cols_per_row)
    plt.figure(figsize=(5 * cols_per_row, 4 * rows))
    
    for i, col in enumerate(columns):
        plt.subplot(rows, cols_per_row, i + 1)
        sns.histplot(df[col].dropna(), kde=False, color='teal', bins=50) 
        plt.title(f'Scaled Distribution: {col}')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
    
    plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "scaled_histograms.png"), dpi=300) # Save high-res version
    # plt.show()

plot_scaled_hist(df_final, continuous_vars)


# Plotting drugs against death rate, before and after scaling
# UNSCALED

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

sns.regplot(data=df_final, x='oxy_gms', y='death_rate', ax=ax1, scatter_kws={'alpha':0.5})
ax1.set_title('Oxycodone per 100k vs Death Rate')

sns.regplot(data=df_final, x='hydro_gms', y='death_rate', ax=ax2, scatter_kws={'alpha':0.5}, color='orange')
ax2.set_title('Hydrocodone per 100k vs Death Rate')

sns.regplot(data=df_final, x='fent_gms', y='death_rate', ax=ax3, scatter_kws={'alpha':0.5}, color='green')
ax3.set_title('Fentanyl per 100k vs Death Rate')

plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "unscaled_drugs_vs_death.png"), dpi=300) # Save high-res version

# SCALED
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

sns.regplot(data=df_final, x='log_oxy', y='log_death_rate', ax=ax1, scatter_kws={'alpha':0.5})
ax1.set_title('Oxycodone per 100k vs Death Rate')

sns.regplot(data=df_final, x='log_hydro', y='log_death_rate', ax=ax2, scatter_kws={'alpha':0.5}, color='orange')
ax2.set_title('Hydrocodone per 100k vs Death Rate')

sns.regplot(data=df_final, x='log_fent', y='log_death_rate', ax=ax3, scatter_kws={'alpha':0.5}, color='green')
ax3.set_title('Fentanyl per 100k vs Death Rate')

plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "scaled_drugs_vs_death.png"), dpi=300) # Save high-res version

# FINAL DATAFRAME FOR MODELING

cols_to_keep = ['year', 'state',
                'hydro_gms', 'oxy_gms', 'fent_gms',
                'log_oxy', 'log_hydro', 'log_fent',
                'gsp', 'unempl_rate', 'min_wage', 'medicaid_rate', 
                'log_gsp', 'log_unempl_rate', 'log_min_wage', 'log_medicaid_rate',
                'snap_rate', 'poverty_rate',
                'gov_dem', 'death_rate', 'log_death_rate']

df_final = df_final[cols_to_keep]

# Export final dataset, scaled (use for "after" snapshots, schemas)
df_final.to_csv(os.path.join(BASE_DIR, 'data', 'death_rate.csv'), index=False)

# Correlation Plots, Unscaled and Scaled
# Unscaled
cols_to_corr = ['death_rate', 'oxy_gms', 'hydro_gms', 'fent_gms', 'gsp', 'snap_rate',
                'poverty_rate', 'unempl_rate', 'min_wage', 'medicaid_rate']

plt.figure(figsize=(10, 8))
sns.heatmap(df_final[cols_to_corr].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix (Unscaled): Supply & Economics vs. Mortality")
plt.savefig(os.path.join(BASE_DIR, 'resources', 'death_rate_plots', "unscaled_corrplot.png"))

# Scaled
cols_to_corr = ['log_death_rate', 'log_oxy', 'log_hydro', 'log_fent', 'log_gsp', 'snap_rate',
                'poverty_rate', 'log_unempl_rate', 'log_min_wage', 'log_medicaid_rate']

plt.figure(figsize=(10, 8))
sns.heatmap(df_final[cols_to_corr].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix (Scaled): Supply & Economics vs. Mortality")
plt.savefig(os.path.join(BASE_DIR, 'resources', 'death_rate_plots', "scaled_corrplot.png"))


# Drug Supply by Year
df_melted = df_final.melt(id_vars='year', 
                    value_vars=['log_oxy', 'log_hydro', 'log_fent'],
                    var_name='Drug Type', 
                    value_name='Grams')

plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Create the lineplot
sns.lineplot(data=df_melted, x='year', y='Grams', hue='Drug Type', marker='o')

plt.title('National Supply Trends: Oxycodone, Hydrocodone, and Fentanyl', fontsize=15)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Grams per 100k Population, scaled', fontsize=12)
plt.legend(title='Drug Type')
plt.xticks(df_final['year'].unique(), rotation=45) # Ensure every year is shown

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "drug_supply_by_year.png"), dpi=300)