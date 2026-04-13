#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler
import requests
df = pd.read_csv("https://data.ct.gov/resource/rybz-nyjw.csv?$limit=20000")

df.columns = df.columns.str.strip()

#data information
df.describe(include="all")
df.isnull().sum()
df.duplicated().sum()

#removing duplicates
df = df.drop_duplicates()

#Converting date of death column to datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print(df['date'])


#Converting age to a numeric format
df['age'] = pd.to_numeric(df['age'], errors='coerce')
#Replacing missing values for the age column with the median age
df['age']=df['age'].fillna(df['age'].median())
#Removing extreme outliers in age column
df = df[df['age'] <= 100]
df = df[df['age'] >= 10]

#Standardizing the gender column by replacing 'M' with 'Male' and 'F' with 'Female'. Replacing missing values with 'Unknown'.
df['sex'] = df['sex'].replace({'M':'Male','F':'Female'})
df['sex']=df['sex'].fillna('Unknown')
#Standardizing the race column by replacing 'Black/African American' with 'Black'. Replacing missing values with 'Unknown'.
df['race'] = df['race'].replace({'Black/African American':'Black'})
df['race'] = df['race'].fillna('Unknown')
#Replacing missing values in 'Location' with 'Unknown'
df['location'] = df['location'].fillna('Unknown')

#Year column
df['year'] = df['date'].dt.year

#Month Column
df['month'] = df['date'].dt.month

#converting drug columns to binary integer format
drug_cols = [
'heroin','cocaine','fentanyl','fentanylanalogue','oxycodone',
'oxymorphone','ethanol','hydrocodone','benzodiazepine',
'methadone','meth_amphetamine','amphet','tramad',
'hydromorphone','morphine_notheroin','xylazine',
'gabapentin','opiatenos','heroin_morph_codeine',
'other_opioid','anyopioid']

df[drug_cols] = (
    df[drug_cols]
    .fillna('N')
    .applymap(lambda x: 1 if str(x).startswith('Y') else 0)
    .astype(int)
)
print(df[drug_cols].dtypes) #checking that all drug columns are integers

#Drug Count column
df['Drug Count'] = df[drug_cols].sum(axis=1)
df['Drug Count'].head()

print(df['datetype'].unique())
#['Date of death' 'Date reported']
print(df['location'].unique())
#[nan 'Decedent’s Home' 'Other (Specify)' 'Hospital - ER/Outpatient' 'Hospital - Inpatient' 'Hospital - Dead On Arrival' 'Hiospital''Nursing Home' 'Hospice Facility' 'Residence' 'Hospital' 'Other''Convalescent Home' 'Assisted Living' 'Shelter' 'Hospice',"Decedent's Home"]
locations = {
'Decedent’s Home': 'Home',
"Decedent's Home": 'Home',
'Residence': 'Home',
'Hospital': 'Hospital',
'Hiospital': 'Hospital',
'Hospital - ER/Outpatient': 'Hospital',
'Hospital - Inpatient': 'Hospital',
"Hospital - Dead On Arrival": "Hospital",
"Nursing Home": "Nursing Home",
"Convalescent Home": "Nursing Home",
"Assisted Living": "Assisted Living",
"Hospice Facility": "Hospice",
"Hospice": "Hospice",
"Shelter": "Shelter",
"Other": "Other",
"Other (Specify)": "Other"
}
df["location"] = df["location"].replace(locations)


print(df['mannerofdeath'].unique())
#['Accident' 'Acciddent' 'Pending' 'accident' nan 'ACCIDENT' 'Natural']
#formatting accident
df['mannerofdeath'] = df['mannerofdeath'].str.strip().str.lower()
df['mannerofdeath'] = df['mannerofdeath'].replace('acciddent', 'accident')
df['mannerofdeath'] = df['mannerofdeath'].str.capitalize()
print(df['mannerofdeath'].unique())

#Replacing unknown and X values as NaN.
print(df['sex'].unique())
#['Male' 'Female' nan 'Unknown' 'X']
df['sex'] = df['sex'].replace({'Unknown': np.nan, 'X': np.nan})


#Standardizing the race column and fixing typos.
print(df['race'].unique())
df['race'] = df['race'].str.strip().str.title()
#['White' nan 'white' 'Black or African American' 'Asian Indian' 'Other Asian (Specify)' 'Other (Specify)' 'Asian' 'Asian/Indian' 'Unknown' 'Other' 'Other Asian' 'Other (Specify) Haitian' 'Black' 'Other (Specify) portugese, Cape Verdean' 'Other (Specify) Puerto Rican''Black or African American / American Indian Lenni Lenape''American Indian or Alaska Native' 'Asian, Other' 'Hawaiian''Native American, Other' 'Chinese' 'Korean' 'Japanese']
races = {
"White": "White",
"Black": "Black",
"Black Or African American": "Black",
"Black Or African American / American Indian Lenni Lenape": "Black",
"Asian": "Asian",
"Asian Indian": "Asian",
"Asian/Indian": "Asian",
"Chinese": "Asian",
"Korean": "Asian",
"Japanese": "Asian",
"Asian, Other": "Asian",
"Other Asian": "Asian",
"Other Asian (Specify)": "Asian",
"American Indian Or Alaska Native": "Native American",
"Native American, Other": "Native American",
"Hawaiian": "Pacific Islander",
"Other": "Other",
"Other (Specify)": "Other",
"Other (Specify) Haitian": "Other",
"Other (Specify) Puerto Rican": "Other",
"Other (Specify) Portugese, Cape Verdean": "Other",
"Unknown": np.nan
}
df['race'] = df['race'].replace(races)


print(df['ethnicity'].unique())
#['No, not Spanish/Hispanic/Latino' nan 'Yes, other Spanish/Hispanic/Latino' 'Unknown' 'Yes, Puerto Rican''Yes, Other Spanish/Hispanic/Latino (Specify)' 'Spanish/Hispanic/Latino' 'Mexican, Mexican American, Chicano' 'Puerto Rican' 'Cuban''Yes, Mexican, Mexican American, Chicano' 'Hispanic''Other Spanish/Hispanic/Latino' 'Not Spanish/Hispanic/Latino''Yes, Cuban' 'n'
df['race'] = df['race'].str.strip().str.lower()
races = {'white':'White', 'black':'Black', 'black or african american':'Black', 'black or african american / american indian lenni lenape': 'Black', 'asian':'Asian', 'asian/indian': 'Asian', 'asian indian':'Asian', 'asian, other': 'Asian', 'other asian': 'Asian', 'other asian (specify)':'Asian', 'korean':'Asian', 'japanese':'Asian', 'chinese':'Asian', 'hawaiian':'Pacific Islander','american indian or alaska native': 'Native American',
'native american, other': 'Native American', 'other':'Other','other (specify)':'Other','other (specify) haitian': 'Other', 'other (specify) portugese, cape verdean': 'Other', 'other (specify) puerto rican': 'Other', 'unknown':'Unknown'}
df['race'] = df['race'].map(races)
df.loc[df['race'].isna(), 'race'].unique()
print(df['race'].unique())

print(df['cod'].unique())
# possible pull 'combined' from column to analyze ods by combined drug use

print(df['heroin_dc'].unique())
#[nan 'Y'], going to drop this column because it does not contribute much for our analysis and there are no rows where heroin is 0 and heroin_dc is 1.

#only one row has Rhode Island as the death state, so I will remove death_state as a whole. The amount of nan's could be from assumption that the death state is Connecticut because this is only Connecticut data.
print(df['death_state'].unique())
#[nan 'CT' 'RI']

print(df['deathcounty'].unique())
#[nan 'NEW LONDON' 'HARTFORD' 'FAIRFIELD' 'NEW HAVEN' 'MIDDLESEX' 'TOLLAND']
df['deathcounty'] = df['deathcounty'].replace({"USA": np.nan})
#Replacing USA with NaN because it is not a valid county in Connecticut.

#Checking data quality after cleaning
df.isnull().sum() #Remove columns with 50% or more of the data missing: Location if Other, Other, Heroin_dc, Other Significant Conditions have very large missing values.
df.duplicated().sum()

columns_to_drop = [
'death_state',
'datetype',
'residencecity',
'injurycity',
'deathcity',
'descriptionofinjury',
'locationifother',
'injuryplace',
'residencecitygeo',
'injurycitygeo',
'deathcitygeo',
'othersignifican',
'heroin_dc', 'anyopioid', 'other_opioid'
]

df = df.drop(columns=columns_to_drop)
df.columns = (df.columns.str.strip().str.replace('_', ' ').str.title())
df = df.rename(columns={"Mannerofdeath": "Manner Of Death"})
df = df.rename(columns={'Morphine Notheroin': 'Morphine'})
df = df.rename(columns={'Meth Amphetamine': 'Methamphetamine'})
df=df.rename(columns={'Opiatenos': 'Opiate NOS'}) #nitrous oxide
df = df.rename(columns={'Tramad': 'Tramadol'})
df = df.rename(columns={'Fentanylanalogue': 'Fentanyl Analogue'})
df = df.rename(columns={'Amphet': 'Amphetamine'})

#Standardizing the age column by creating a new column with standardized age values using z-score normalization.
scaler = StandardScaler()
df["Age Standardized"] = scaler.fit_transform(df[["Age"]])

#Log Transformation of Drug Count
df["Drug Count Log"] = np.log1p(df["Drug Count"])

#Visualization between Log Drug Count and Drug Count
sns.histplot(df["Drug Count"], bins=8, kde=True)
plt.title("Drug Count Distribution")
plt.show()
#versus
sns.histplot(df["Drug Count Log"], bins=8, kde=True)
plt.title("Log Transformed Drug Count Distribution")
plt.xlabel("Log(Drug Count + 1)")
plt.ylabel("Frequency")

plt.savefig("../../resources/data_exploration_plots_CT/Log_Transformed_Data_Count_Distribution.png")
plt.show()



#Summary Statistics
print(df.describe())

#Q-Q Plots
#Age Distribution
sns.set_theme(style="whitegrid")
plt.figure(figsize=(7,6))
stats.probplot(df["Age"], dist="norm", plot=plt)
plt.title("Q-Q Plot of Age Distribution")

plt.savefig("../../resources/data_exploration_plots_CT/QQ_Plot.png")
plt.show()

#Total Deaths Involving Each Drug
drugs = [
'Heroin','Cocaine','Fentanyl','Fentanyl Analogue','Oxycodone',
'Oxymorphone','Ethanol','Hydrocodone','Benzodiazepine',
'Methadone','Methamphetamine','Amphetamine','Tramadol',
'Hydromorphone','Morphine','Xylazine',
'Gabapentin','Opiate NOS','Heroin Morph Codeine']

#Heatmap of Correlation Between Drugs in Overdose Cases
drug_variation = df[drugs].loc[:, df[drugs].nunique() > 1] #selecting only drug columns that have more than one unique value to avoid errors in correlation calculation
drug_corr = drug_variation.corr()
plt.figure(figsize=(14,10))
sns.heatmap(drug_corr, cmap="coolwarm", center=0, annot = True, fmt=".2f", square=True)
plt.title("Correlation Between Drugs in Overdose Cases")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig("../../resources/data_exploration_plots_CT/heatmap.png")
plt.show()



#How common is it for multiple drugs to be present in overdose cases?
drug_count_dist = df['Drug Count'].value_counts().sort_index()
plt.figure(figsize=(8,6))
sns.barplot(
    x=drug_count_dist.index,
    y=drug_count_dist.values,
    palette="viridis"
)
plt.title("Number of Drugs Present in Each Case")
plt.xlabel("Number of Drugs")
plt.ylabel("Number of Cases")
plt.savefig("../../resources/data_exploration_plots_CT/Drug_Count_Distribution.png")
plt.show()


#Total Deaths Involving Each Drug
drug_sums = df[drugs].sum().sort_values(ascending=False)
plt.figure(figsize=(12,6))
sns.barplot(x=drug_sums.index, y=drug_sums.values, palette="viridis")
plt.title('Total Deaths Involving Each Drug')
plt.ylabel('Number of Deaths')
plt.xlabel('Drug')
plt.xticks(rotation=45)
plt.savefig("../../resources/data_exploration_plots_CT/Total_Deaths_Involving_Each_Drug.png")
plt.show()


#How Many Drugs are Present in Each Case
sns.countplot(data=df, x='Drug Count', palette="viridis")
plt.title('Number of Drugs Present in Each Case')
plt.ylabel('Number of Cases')
plt.xlabel('Number of Drugs')
plt.savefig("../../resources/data_exploration_plots_CT/Number_of_Drugs_Present.png")
plt.show()


#Seasonality of Deaths
month_labels = [
"January","February","March","April","May","June",
"July","August","September","October","November","December"
]
sns.countplot(data=df, x="Month", palette="viridis")
plt.xticks(
    ticks=range(12),
    labels=month_labels,
    rotation=45
)
plt.title("Seasonality of Deaths")
plt.xlabel("Month")
plt.ylabel("Number of Deaths")
plt.savefig("../../resources/data_exploration_plots_CT/Seasonality_of_Deaths.png")
plt.show()


# %%
