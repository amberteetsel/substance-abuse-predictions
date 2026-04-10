import pandas as pd
import numpy as np
from sodapy import Socrata
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats
from scipy.stats import skew

# API Configuration
DATASET_ID = "xbxb-epbu"
DOMAIN = "data.cdc.gov"
APP_TOKEN = "CpwHhA1scJ9x7VNZ3PWM8MRG6"

# Initialize client
client = Socrata(DOMAIN, APP_TOKEN)

# Fetch the data
results = client.get(DATASET_ID, limit=5000)

# Convert to pandas DataFrame
nchs_df = pd.DataFrame.from_records(results)

# Save raw data to CSV
nchs_df.to_csv('../../data/NCHS_Mortality_Raw.csv', index=False)

# Drop range column
df = nchs_df.copy()
df.drop('state_crude_rate_in_range', axis=1, inplace=True)

# Combine crude and age-adjusted rates to one column for ease of future analysis
df['death_rate'] = np.where(df.age_group=='All Ages', df.age_adjusted_rate, df.crude_death_rate)
df['standard_error_death_rate'] = np.where(df.age_group=='All Ages', df.standard_error_for_age_adjusted_rate, df.standard_error_for_crude_rate)
df['lower_confidence_death_rate'] = np.where(df.age_group=='All Ages', df.lower_confidence_limit_for_age_adjusted_rate, df.lower_confidence_limit_for_crude_rate)
df['upper_confidence_death_rate'] = np.where(df.age_group=='All Ages', df.upper_confidence_limit_for_age_adjusted_rate, df.upper_confidence_limit_for_crude_rate)

# Fix data types
cols = ['year',
       'deaths', 'population', 'crude_death_rate',
       'standard_error_for_crude_rate',
       'lower_confidence_limit_for_crude_rate',
       'upper_confidence_limit_for_crude_rate', 'age_adjusted_rate',
       'standard_error_for_age_adjusted_rate',
       'lower_confidence_limit_for_age_adjusted_rate',
       'upper_confidence_limit_for_age_adjusted_rate', 'us_crude_rate',
       'us_age_adjusted_rate', 'death_rate',
       'standard_error_death_rate', 'lower_confidence_death_rate',
       'upper_confidence_death_rate']

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Log Transformation
df['death_rate_log'] = np.log10(df.death_rate + 1)

# Rename column
df.rename(columns={'race_and_hispanic_origin':'race'}, inplace=True)

# Mapping for Race & Hispanic Origin column
race_map = {'All Races-All Origins': 'All Races',
           'Hispanic': 'Hispanic',
           'Non-Hispanic Black':'Black',
           'Non-Hispanic White': 'White'}

df.race = df.race.map(race_map)

# Consolidate ages
age_map = {'All Ages': 'All Ages',
           '0–14':'0-14',
           '15–24':'15-24',
          '25–34':'25-44',
          '35–44':'25-44',
          '45–54':'45-64',
          '55–64':'45-64',
          '65–74':'65+',
          '75+':'65+'}
df['age_group1'] = df['age_group'].map(age_map)
df.rename(columns={'age_group':'age_group_detail',
                  'age_group1': 'age_group'}, inplace=True)

# keep relevant columns
cols_to_keep = ['state', 'year', 'sex', 'age_group', 'age_group_detail', 'race',
                'death_rate', 'death_rate_log',
                'us_crude_rate', 'us_age_adjusted_rate',
                'deaths', 'population']

df = df[cols_to_keep]

# Global cumulative level
df_cum = df.loc[(df.state=='United States')&\
                (df.sex=='Both Sexes')&\
                (df.race=='All Races')&\
                (df.age_group=='All Ages')].reset_index(drop=True)



scaler = StandardScaler()

df_cum['death_rate_z_score'] = scaler.fit_transform(df_cum[['death_rate']])

# State cumulative level
df_state = df.loc[(df.state!='United States')&\
                (df.sex=='Both Sexes')&\
                (df.race=='All Races')&\
                (df.age_group=='All Ages')].reset_index(drop=True)

# Initialize
scaler2 = StandardScaler()

df_state['death_rate_z_score'] = scaler2.fit_transform(df_state[['death_rate']])

# QQ Plot
plt.figure(figsize=(6,4))
stats.probplot(df_cum.death_rate, dist='norm', plot=plt)
plt.title('QQ Plot of Standardized Death Rates (Country-wide)')
# plt.show()

plt.savefig('../../resources/data_exploration_plots_NCHS/QQ_death_rate.jpeg')

# Export Clean Data
df.to_csv('../../data/NCHS_Mortality_Clean.csv', index=False)
df_state.to_csv('../../data/NCHS_Mortality_State.csv', index=False)
df_cum.to_csv('../../data/NCHS_Mortality_Cumulative.csv', index=False)

# VISUALIZATIONS
# YoY Change in US Age-Adjusted Death Rate
tmp = df.loc[(df.sex=='Both Sexes')&(df.age_group=='All Ages')&(df.race=='All Races')&\
    (df.state=='United States')].reset_index(drop=True)
tmp = pd.DataFrame(tmp.groupby(['year']).agg({'us_age_adjusted_rate':'mean',
                                                'deaths':'sum'})).reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=tmp,
             x='year',
             y='us_age_adjusted_rate',
            marker='o',
            markersize=6)

for i in range(tmp.shape[0]):
    plt.text(tmp.year[i],
             tmp.us_age_adjusted_rate[i] + 0.5,
             f'{tmp.us_age_adjusted_rate[i]:.1f}',
             ha='center', va='bottom',
             fontsize='10')

# sns.barplot(data=tmp,
#             x='year',
#             y='deaths')

plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.ylim(0,22)
plt.title("US Drug Death Mortality Rate, 1999-2016", fontsize=14, pad=10)
plt.xlabel('Year')
plt.ylabel('Age-Adjusted Death Rate per 100,000 Population')

plt.savefig('../../resources/data_exploration_plots_NCHS/mortality_1999_2016.jpeg')

# YoY Change by Race
tmp = df.loc[(df.sex=='Both Sexes')&(df.age_group=='All Ages')&(df.race!='All Races')].reset_index(drop=True)
tmp = pd.DataFrame(tmp.groupby(['year', 'race'])['death_rate'].mean()).reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=tmp,
             x='year',
             y='death_rate',
             hue = 'race',
             palette='colorblind',
            marker='o',
            markersize=6)

plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.legend(title='Race')
plt.title("US Drug Death Mortality Rate by Race, 1999-2016", fontsize=14, pad=10)
plt.xlabel('Year')
plt.ylabel('Age-Adjusted Death Rate per 100,000 Population')

plt.savefig('../../resources/data_exploration_plots_NCHS/mortality_race_1999_2016.jpeg')

# YoY Change by Sex
tmp = df.loc[(df.sex!='Both Sexes')&(df.age_group=='All Ages')&(df.race=='All Races')].reset_index(drop=True)
tmp = pd.DataFrame(tmp.groupby(['year', 'sex'])['death_rate'].mean()).reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=tmp,
             x='year',
             y='death_rate',
             hue = 'sex',
             palette='colorblind',
            marker='o',
            markersize=6)

plt.grid(linestyle='--', alpha=0.7, zorder=0)
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.legend(title='Sex')
plt.title("US Drug Death Mortality Rate by Sex, 1999-2016", fontsize=14, pad=10)
plt.xlabel('Year')
plt.ylabel('Age-Adjusted Death Rate per 100,000 Population')
plt.savefig('../../resources/data_exploration_plots_NCHS/mortality_sex_1999_2016.jpeg')

# Boxplots - Death Rate by Age Group
tmp = df.loc[(df.sex=='Both Sexes')&(df.age_group!='All Ages')&(df.race=='All Races')\
    &(df.age_group!='0-14')].reset_index(drop=True)

plt.figure(figsize=(10,6))
sns.boxplot(data=tmp,
            x='age_group',
            y='death_rate',
            hue='age_group',
           palette='crest')

plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
plt.title("US Drug Death Mortality Rate by Age", fontsize=14, pad=10)
plt.xlabel('Age Group')
plt.ylabel('Death Rate per 100,000 Population')
plt.savefig('../../resources/data_exploration_plots_NCHS/mortality_age_boxplot.jpeg')

# State Outliers, 2016
tmp = df_state.loc[df_state.year==2016].reset_index(drop=True)

top10 = tmp.sort_values(by='death_rate_z_score', ascending=False).head(10)

plt.figure(figsize=(10,6))
ax = sns.barplot(data = top10,
            x = 'death_rate_z_score',
            hue = 'state',
            palette='colorblind',
           edgecolor='black',
                legend=False)

# gridlines
plt.grid(axis='x', linestyle='--', alpha=0.7, zorder=0)
ax.set_axisbelow(True)

# labels
for i, p in enumerate(ax.patches[:10]):
    state_name = top10.iloc[i]['state']
    z_val = top10.iloc[i]['death_rate_z_score']
    
    y_coord = p.get_y() + p.get_height() / 2
    
    plt.text(
        0.1, 
        y_coord, 
        f'{state_name} ({z_val:.2f})', 
        color='black',
        va='center',
        fontweight='bold',
        fontsize=10
    )

plt.title('Top 10 State Outliers for Drug Mortality (2016)')
plt.xlabel('Z-Score')
plt.ylabel('State')
plt.savefig('../../resources/data_exploration_plots_NCHS/state_outliers_2016.jpeg')