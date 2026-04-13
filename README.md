# Substance Abuse and Overdose Death

## Project Overview
The topic of our research project is identifying/predicting which communities are at risk of drug abuse and or drug overdose. Once these communities are identified, we will identify which factors cause these communities to have a higher risk of substance abuse. This research topic is important because substance abuse is prevalent in the United States. Drug overdose is the leading cause of death for Americans under 50 years old (Substance Abuse and Mental Health Services Administration, 2025). In 2024, only 1 in 5 people who suffer from drug abuse received treatment (SAMHSA, 2025). If we could help predict which communities are at risk and why, it could help distinguish where substance abuse treatment resources need to go and identify which factors that lead to substance abuse. This research benefits treatment providers, schools and community organizations, and public health agencies.

## Website

[Link to webpage holding project results](https://substance-abuse-predictions.streamlit.app/)

## Team

**Andrea Caceres:** Modeling & Visualization Lead

**Isra Marcu:** Data & Analyzation Lead

**Amber Teetsel:** Web Developer & Data Scientist

## Development Environment
1. Run `conda env create -f environment.yml` in terminal.
2. `conda activate substance_abuse ` to activate the environment.
3. `python -m streamlit run src/app.py` to run the streamlit app.
4. `python <file_path>` to run any other .py files

## Data Cleaning
To run TEDS_Acleaning.py
1. Download tedsa_puf_2023.csv from the google drive: https://drive.google.com/drive/folders/1tE90rBjR8Rhdg5j_9aLIlxras2XQ7W-J?usp=sharing
2. Create a folder called data and place tedsa_puf_2023.csv in the folder
3. Run the file (be patient, it is a large data set)
4. Cleaned csv for this set will be found in the google drive

To run Connecticut_Data_Caceres_Andrea.py
1. Download the cleaning file
2. Run the file
3. Cleaned csv for these datasets will be found in the data folder

To run DEA_cleaning.py, NCHS_cleaning.py, UKCPR_cleaning.py, DEA_NCHS_UKCPR.py:
1. Clone the repository
2. `python src/data_cleaning/<file_name>`
3. Cleaned .csv files to be found in [Data Folder](data)
4. Relevant plots to be found at [Data Exploration Plots](resources/data_exploration_plots_NCHS) and [Death Rate Plots](resources/death_rate_plots)

## Data Modeling 
To run tedsa_clean_modeling.py
1. Download tedsa_puf_2023_cleaned.csv from the google drive: https://drive.google.com/drive/folders/1tE90rBjR8Rhdg5j_9aLIlxras2XQ7W-J?usp=sharing
2. Create a folder called data and place tedsa_puf_2023_cleaned.csv in the folder
3. Run the file (be patient, it is a large data set)
4. Cleaned csv for this set will be found in the google drive

To run tedsa_first_use_modeling.py
1. Download tedsa_puf_2023_first_use.csv from the google drive: https://drive.google.com/drive/folders/1tE90rBjR8Rhdg5j_9aLIlxras2XQ7W-J?usp=sharing
2. Create a folder called data and place tedsa_puf_2023_first_use.csv in the folder
3. Run the file (be patient, it is a large data set)
4. Cleaned csv for this set will be found in the google drive

To run death_rate_model.py (K-Means Clustering):
1. Clone the repository
2. `python src/models/death_rate_model.py`
3. Data with clustering results: [Death Rate Clusters](data/death_rate_kmeans.csv)
4. Associated visuals: [Death Rate Cluster Plots](resources/death_rate_plots)
   

## Milestones

1. Project Framing & Website Launch (9 Feb 2026)
2. Data Preparation/Collection & Cleaning (6 Mar 2026)
3. Model Implementation (13 Apr 2026)
4. Conclusion, Results, & Project Report (20 Apr 2026)
