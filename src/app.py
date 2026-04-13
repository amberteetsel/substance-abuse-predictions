import streamlit as st
import pandas as pd
from model_view import model_section
from data_view import data_source_section
import os
import plotly.express as px

# Set root directory for file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Page layout
st.set_page_config(page_title="Substance Abuse/Overdose Analysis", layout="wide")

# title
st.title("Substance Abuse & Overdose Death")
st.markdown("---")

# Initialize tabs
# tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs(["Introduction", "Research Questions", "Data Sources", "Team Bios", "References", "Data Exploration"])
tab1, tab2, tab4, tab5, tab6, tab7 = st.tabs(["Introduction",
                                              "Research Questions",
                                              "Team Bios",
                                              "References",
                                              "Data Exploration",
                                              "Models Implemented"])

# TAB 1: INTRODUCTION
with tab1:
    st.header("Project Introduction")

    # Research Topic & Significance 
    st.subheader("Problem Statement")
    st.write("""
	The topic of our research project is predicting which communities are at a higher risk of drug abuse and or drug overdose. By using socioeconomic, demographic, drug type, and past drug overdose data, we can help identify communities with high rates of substance abuse. Once these communities are identified, we will analyze the underlying factors that contribute to this elevated risk. Some of these factors could be housing insecurity, food insecurity, age, genetics, location, exposure to prescriptions drugs, or access to treatment. 
    
This research topic is important because substance abuse is alarmingly prevalent in the United States. Drug overdose is the leading cause of death for Americans under 50 years old (Substance Abuse and Mental Health Services Administration, 2025). In 2024, only 1 in 5 people who suffer from drug abuse received treatment (SAMHSA, 2025). Among people in 2024, 71.5% of adolescents aged 12 to 17 years used nicotine products in the past month (SAMHSA, 2025).

 If we could help predict which communities are at risk and why, it could help distinguish where substance abuse treatment resources need to go and identify which factors that lead to substance abuse. This research benefits treatment providers, schools and community organizations, and public health agencies.

    """)

    # Drug Death Visual
    st.image("resources/DrugDeathGraphic.png", width=1000)
    st.caption("U.S. Drug Deaths by Substance [CDC](https://www.cdc.gov/nchs/nvss/vsrr/prov-drug-involved-mortality.htm)")
    
    # Stakeholders
    st.subheader("Who is Affected?")
    st.write("""
Drug abuse has cascading effects across multiple industries. Real-world implications of substance abuse are intergenerational substance abuse, increased taxes and spending to keep up with this crisis, and entrenched poverty. This research could help healthcare and public health industries take a preventative approach to substance abuse rather than a reactive one. By using a data-supported stratification rather than miniscule intervention, the healthcare system can be more effective in their approach to fighting drug abuse. Predictive modeling is beneficial because it provides the most optimized approach to using limited and minimal resources. This ensures that the taxpayer dollar is utilized in an efficient approach towards prevention of drug addiction. This research could help lower the volume of non-violent offenders in jails and prisons. Schools and community organizations will improve if preventative measures can be taken because drop-out rates will decrease. Also, teachers and professors will have identifiers for students and or participants for risk of drug abuse. Not only can patterns be identified early, but schools can become a safe space for students to be vulnerable psychologically. This can allow them to focus on their academics rather than stressors from their environment outside of school. 

Marginalized populations could benefit from this research because resources and treatment can be focused on these groups if they are identified, setting up these communities to succeed. If these issues can be addressed throughout our research, the loop of generational poverty can be broken. The lack of education amongst marginalized groups can also be fixed as substance abuse decreases and more opportunities can arise. Breaking these trends can increase social equity. Plus, this research can provide the means necessary to inflict systemic changes in society. Legislation can be made to implement the results these types of studies produce in aiding those struggling. Bringing down the substance abuse crisis in the country can improve quality of life for individuals in major cities as well. Streets will be cleaner, the poverty rate will lower, unemployment rate will decrease, and these communities can produce contributing citizens. Identifying these trends can help prevent drug abuse and increase the professional integrity of those more likely to be at risk. 

    """)

    # Existing Solutions & Gaps
    st.subheader("Current Landscape")
    st.write("""
There are many imperfect solutions to combat drug overdose and help mitigate drug abuse. In specific there are opioid overdose reversal medications (OORM) that are life-saving and reverse the effects of opioid overdose (Substance Abuse and Mental Health Services Administration, 2023). These medications are widely available for the general public and do not require training, significantly reducing overdose fatality rates (SAMHSA, 2023). Another way to reduce the risk of overdose is using test strips to check for the presence of fentanyl (SAMHSA, 2023). In general effective treatment of substance use disorder can reduce the risk of overdose and help combat drug use, whether that be through out-patient therapy or in-patient stay at a facility. There are many challenges regarding drug use; one is the inappropriate and over-prescribing of opioids, leading to misuse (Cerdá, Krawczyk, Keyes, 2023). In addition, the criminalization of drug use has harmed those that are users and/or in possession of drugs resulting in incarceration rather than treatment (Cerdá, Krawczyk, Keyes, 2023). Many challenges occur because of a lack of resources, such as poor access to healthcare to address pain treatment (SAMHSA, 2023). To truly prevent overdose there needs to be steps taken before overdose can even occur to help mitigate the risk. This can be done by assessing personal risk and taking the steps that are specific to those factors because treatment needs to be individualized to truly be effective. 
    """)

    # Project Blueprint
    st.subheader("Roadmap")
    st.write("""
Before beginning with any data preparation, the team will read various scholarly sources on the topic of substance abuse and overdose to better understand the context of the data that will be analyzed. The team will start with data preparation to extract relevant information from a variety of datasets and integrate them. It is important that we use many datasets to ensure we have comprehensive data to analyze. Next, exploratory data analysis will help us understand the United States substance abuse and overdose landscape and identify interesting trends and patterns. For instance, we need to know the frequency of overdose for various drugs and communities with the highest rates of substance abuse. Then we will perform unsupervised learning (e.g. clustering) to determine risk profiles and dive deeper into identified patterns/trends. We plan to look into relationships between socioeconomic factors and substance abuse. Finally we plan to see if we can predict individual treatment outcomes or overdose, or general overdose death in the future. After the final models are completed, we will assess their performance to better understand how valid our findings are. Our findings will then be summarized to help inform public health strategies and also the general public.
    """)


# TAB 2: RESEARCH QUESTIONS
with tab2:
    st.header("Research Questions")
    st.write("We are applying data mining techniques to answer the following:")
    
    # container to hold questions
    with st.container():
        st.markdown("""
        1. What are the most common circumstances of death among substance users?
        2. How do drug profiles (mix of drugs in system) differ between overdose victims?
        3. How has the age of first use changed over time for different drugs?
        4. Does time of year affect overdose deaths? If so, how does the seasonality of overdose deaths differ between drugs?
        5. Which socioeconomic factors have the strongest correlation with overdose?
        6. How do mental health and substance abuse intersect? Does this differ by gender or race?
        7. How does forced vs. involuntary substance abuse treatment impact treatment completion rates?
        8. Can intake demographics allow us to predict whether substance abuse treatment will be completed or not?
        9. What demographic features are the best predictors of polysubstance mortality?
        9. Can we forecast the next X months of overdose death for specific drugs?
        """)

# # TAB 3: DATA SOURCES
# with tab3:
#     st.header("Data Sources")
#     st.subheader("Potential Datasets for Analysis")

#     st.info("💡 [Accidental Drug Related Deaths 2012-2014](https://catalog.data.gov/dataset/accidental-drug-related-deaths-2012-2018)")
#     st.write("A listing of each accidental death associated with drug overdose in Connecticut from 2012 to 2024.")

#     st.info("💡 [SUDORS Dashboard: Fatal Drug Overdose Data](https://www.cdc.gov/overdose-prevention/data-research/facts-stats/sudors-dashboard-fatal-overdose-data-accessible.html)")
#     st.write("CDC data on unintentional and undetermined intent drug overdose deaths from death certificates, medical examiner or coroner reports, and postmortem toxicology results.")

#     st.info("💡 [Treatment Episode Data Set: Admissions/Discharges (TEDS-A/D)](https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles/teds-d-2020)")
#     st.write("When undergoing substance abuse treatment, individual people can be admitted and discharged from treatment multiple times. The Treatment Episode Data Set (TEDS) system comprises demographic and drug history information about these individuals.")

#     st.info("💡 [Provisional Drug Overdose Death Counts for Specific Drugs](https://catalog.data.gov/dataset/provisional-drug-overdose-death-counts-for-specific-drugs)")
#     st.write("The provisional data are based on a current flow of mortality data and include reported 12 month-ending provisional counts of drug overdose deaths by jurisdiction of occurrence and specified drug.")

#     st.info("💡 [CDC Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)")
#     st.write("Place-based index, database, and mapping application designed to identify and quantify communities experiencing social vulnerability.")

#     st.info("💡 [NCHS - Drug Poisoning Mortality by State: United States](https://data.cdc.gov/National-Center-for-Health-Statistics/NCHS-Drug-Poisoning-Mortality-by-State-United-Stat/xbxb-epbu/data_preview)")
#     st.write("This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning.")

#     st.info("💡 [National Survey on Drug Use and Health (NSDUH)](https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/datafiles?utm_source=chatgpt.com)")
#     st.write("NSDUH measures substance use, mental illness, and treatment in the civilian noninstitutionalized population 12 or older.")


# TAB 4: TEAM BIOS
with tab4:
    st.header("The Team")
    
    # Creating a grid for team members
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("resources/bio/AndreaCaceres_Headshot.jpg", width=150)
        st.write("**Andrea Caceres**")
        st.write("Role: Modeling & Visualization Lead")
        st.write("Andrea Caceres is a graduate student at the University of Colorado Boulder with a Bachelors in Statistics from the University of Georgia. She has experience in pension analysis from her prior position at WTW, but is focusing on expanding her data analytical knowledge. ")
        st.caption("[GitHub](https://github.com/andreaycaceres)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/andrea-caceres-609609256/)")

    with c2:
        st.image("resources/bio/IsraMarcu_Headshot.JPG", width=150)
        st.write("**Isra Marcu**")
        st.write("Role: Data & Analyzation Lead ")
        st.write("Isra Marcu is a graduate student at the University of Colorado Boulder pursuing a Masters in Data Science. She has a Bachelors in Psychology from the University of North Carolina at Chapel Hill. Isra has experience in ethically conducting research on participants and analyzing corresponding data.")
        st.caption("[GitHub](https://github.com/isram1223)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/isra-marcu-a220a1274/)")

    with c3:
        st.image("resources/bio/Teetsel_Headshot.jpeg", width=150)
        st.write("**Amber Teetsel**")
        st.write("Role: Web Developer & Data Scientist")
        st.write("Bio: Amber Teetsel is currently pursuiing a Master's in Data Science at the University of Colorado Boulder. She has Bachelor's degrees from Vanderbilt University in Mathematics, Finance, and Women's Studies. Amber began her career in financial services consulting, but her past 4 years of experience have been as data analyst for a multinational corporation.")
        st.caption("[GitHub](https://github.com/amberteetsel)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/amber-teetsel/)")


# TAB 5: CITATIONS/RESOURCES
with tab5:

    st.header("Works Cited")

    sources = {
        "Resource": ["Family, Individual, and Other Risk Factors Contributing to Risk of Substance Abuse in Young Adults: A Narrative Review",
                     "Drug Overdose Deaths in the United States, 2002–2022",
                     "SAMHSA Releases Annual National Survey on Drug Use and Health",
                     "SAMHSA Overdose Prevention and Response Toolkit",
                     "The Future of the United States Overdose Crisis: Challenges and Opportunities",
                     "Provisional Drug Overdose Death Counts for Specific Drugs"
        ],
        "Link": ["https://pmc.ncbi.nlm.nih.gov/articles/PMC9731175/",
                 "https://stacks.cdc.gov/view/cdc/135849",
                 "https://www.samhsa.gov/newsroom/press-announcements/20250728/samhsa-releases-annual-national-survey-on-drug-use-and-health",
                 "https://library.samhsa.gov/sites/default/files/overdose-prevention-response-kit-pep23-03-00-001.pdf",
                 "https://onlinelibrary.wiley.com/doi/10.1111/1468-0009.12602",
                 "https://www.cdc.gov/nchs/nvss/vsrr/prov-drug-involved-mortality.htm"
        ]
    }

    st.table(sources)


# TAB 6: DATA EXPLORATION

## Datasets to display
nchs_raw = pd.read_csv('data/NCHS_Mortality_Raw.csv')
nchs_clean = pd.read_csv('data/NCHS_Mortality_State.csv')
connecticut_raw = pd.read_csv("data/Connecticut_Accidental_Drug_Related_Deaths_Raw.csv")
connecticut_clean = pd.read_csv("data/Clean_Connecticut_Accidental_Drug_Related_Deaths.csv")
dea_clean = pd.read_csv('data/dea_full_interpolated.csv')
ukcpr_raw = pd.read_csv('data/ukcpr_raw.csv')
ukcpr_clean = pd.read_csv('data/UKCPR_cleaned.csv')

with tab6:
    st.header("Data Exploration & Preprocessing")

    # FUNCTION FOR DATA EXPLORATION LAYOUT
    def data_source_section(
        title,
        df_raw, df_clean,
        source_info,
        collection_method,
        description,
        cleaning_steps,
        limitations,
        visuals=None,
        outliers=None,
        sum_stats=None,
        corr=None,
        advanced=None,
        notes=None
    ):
        """
        Inputs will be displayed cleanly on the website
        title - title of dataset
        Ensure you load relevant versions of df_raw, df_clean earlier in this script (see TAB 6 comment above)
        source_info - where dataset came from
        collection_method - how you accessed the data (e.g. download, API, etc.)
        description - briefly describe dataset contents and why it's relevant to the project
        cleaning_steps - dictionary, {<step name> : <step description>}
        visuals - list of dictionaries, [{'title': <name of visual>,
                                        'desc': <description, insights, comments, etc.>,
                                        'path': <path to image>}]
        limitations - text describing any potential biases or limitations of data
        """
        with st.expander(f"📊 Dataset: {title}", expanded=False):
            st.subheader(title)
            
            # Overview
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.write(f"**Source:** {source_info}")
                st.write(f"**Collection Method:** {collection_method}")
            with col_meta2:
                st.markdown(f"**Description:** {description}")
            
            st.markdown("---")

            # Raw vs. Clean comparison
            st.subheader("Data Transformation Preview")
            col_pre1, col_pre2 = st.columns(2)
            
            with col_pre1:
                st.write("🔍 **Raw Snapshot**")

                # If using DataFrames
                if isinstance(df_raw, pd.DataFrame):
                    
                    st.dataframe(df_raw.head(5), use_container_width=True)
                    st.caption("Initial data types and values.")
                    with st.expander("View Raw Schema"):
                        st.code(df_raw.dtypes)

                # If using links/strings
                elif isinstance(df_raw, str):

                    st.image(df_raw, use_container_width=True)


            with col_pre2:
                st.write("✨ **Processed Snapshot**")

                if isinstance(df_clean, pd.DataFrame):
                    st.dataframe(df_clean.head(5), use_container_width=True)
                    st.caption("Post-cleaning, encoding, and scaling.")
                    with st.expander("View Processed Schema"):
                        st.code(df_clean.dtypes)
                elif isinstance(df_clean, str):
                    st.image(df_clean, use_container_width=True)

            st.markdown("---")

            # Summary Statistics
            if (isinstance(df_raw, pd.DataFrame)) and (isinstance(df_clean, pd.DataFrame)):
                st.subheader("Statistical Profile")
                st.write("Comparison of descriptive statistics before and after processing.")
                
                col_stat1, col_stat2 = st.columns(2)
                with col_stat1:
                    st.write("**Raw Summary**")
                    raw_stats = df_raw.select_dtypes(include=['number']).describe().T
                    if not raw_stats.empty:
                        st.table(raw_stats)
                    else:
                        st.warning("No numeric data found in Raw dataset.")
                
                with col_stat2:
                    st.write("**Processed Summary**")
                    clean_stats = df_clean.select_dtypes(include=['number']).describe().T
                    if not clean_stats.empty:
                        st.table(clean_stats)
                    else:
                        st.warning("No numeric data found in Processed dataset.")
    
                st.markdown("---")
            
            # Cleaning & Processing Steps
            st.subheader("Cleaning & Processing Logic")
            for step_title, step_desc in cleaning_steps.items():
                st.markdown(f"**{step_title}**")
                st.info(step_desc)

            st.markdown("---")

            # Visuals
            st.subheader("Visual Analysis")
            if visuals:
                for viz in visuals:
                    with st.container(border=True):
                        st.write(f"#### {viz['title']}")
                        st.write(viz['desc'])
                        st.image(viz['path'], use_container_width=True)
            else:
                st.info("Visualizations for this dataset are currently in progress.")

            # Additional Analysis Sections
            if outliers:
                st.subheader("Outlier Detection")
                with st.container(border=True):
                    st.image(outliers['image'], use_container_width=True)
                    st.write(f"**Interpretation:** {outliers['Interpretation']}")
                    st.write(f"**Action:** {outliers['Action']}")
                
            if sum_stats:
                st.subheader("Summary Statistics")
                with st.container(border=True):
                    st.write(f"**Summary:** {sum_stats['Interpretation']}")
                    st.write(f"**Interpretation:** {sum_stats['Interpretation']}")
                    
            if corr:
                st.subheader("Correlation Analysis")
                with st.container(border=True):
                    st.image(corr['image'], use_container_width=True)
                    st.write(f"**Interpretation:** {corr['Interpretation']}")
    
            if advanced:
                st.subheader("Advanced Analysis")
                with st.container(border=True):
                    st.image(advanced['image'], use_container_width=True)
                    st.write(f"**Interpretation:** {advanced['Interpretation']}")
                    
            if notes:
                st.subheader("Additional Notes")
                with st.container(border=True):
                    st.write(notes)

            # Bias/Limitations
            st.subheader("Limitations")
            if limitations:
                with st.container():
                    st.write(limitations)

    # --- SECTION: NCHS Drug Poisoning ---
    data_source_section(
        title="NCHS - Drug Poisoning Mortality by State",
        df_raw=nchs_raw,
        df_clean=nchs_clean,
        source_info="CDC / National Center for Health Statistics",
        collection_method="API (Socrata SODA)",
        description="The dataset provides solid historical information (1999-2016) on drug deaths in the United States broken down by State, Age Group, Race (White, Hispanic, Black), and Sex (Male, Female). It enables us to see trends (geographic, demographic, temporal) in drug mortality during the early 21st century and can be useful in building an eventual predictive model.",
        cleaning_steps={
            "Handling Missing Data": "Age-adjusted rate is NA for rows that specify an age group (vs. All Ages). To remedy, we combined crude rate and adjusted rate columns with the understanding that data will need to be filtered by age group for subsequent analysis.",
            "Outliers": "We identified many high outliers for death rate but decided to leave them in the data. Upon inspection, the numbers are consistent with the raw deaths/population numbers reported and tend to occur in states where we know the opioid and fentanyl crises had devastating effects (West Virginia, Ohio, etc.). Thus we feel the outliers are useful data points for understanding the true substance abuse landscape in the United States.",
            "Data Types": "The API returns all data as objects so we converted columns such as death rate, year, population, etc. to numeric. Relevant categorical columns include State, Race, Age Group, and Sex.",
            "Dimensionality Reduction": "Keep only year, categorical feature columns, and death rate calculations. Made age group less granular to simplify visualizations. Also simplified naming conventions for Race column.",
            "Handling Overlapping Totals": "Filter out 'United States' aggregate rows to isolate state-level data and prevent double-counting in statistical models.",
            "Standardization": "Applied Z-score standardization to the age-adjusted rates to identify statistical outliers. Added log transformation for death rate for use in potential future linear models."
        },
        visuals = [
            {
                'title': "Fig. 1: U.S. Drug Mortality Rate",
                'desc': "Demonstrates rise in U.S. drug mortality rates from 1999-2016, including a sharp jump between 2014 and 2016.",
                'path': "resources/data_exploration_plots_NCHS/mortality_1999_2016.jpeg"
            },
            {
                'title': 'Fig. 2: Drug Mortality Rate by Race',
                'desc': "The rise in drug mortality rates from 1999-2016 disproportionately impacted non-hispanic whites.",
                'path': "resources/data_exploration_plots_NCHS/mortality_race_1999_2016.jpeg"
            },
            {
                'title': 'Fig. 3: Drug Mortality Rate by Sex',
                'desc': "Men have consistently suffered higher drug death rates than women.",
                'path': "resources/data_exploration_plots_NCHS/mortality_sex_1999_2016.jpeg"
            },
            {
                'title': 'Fig. 4: Drug Mortality Rate by Age Group',
                'desc': "Drug mortality rates are highest among 25-44 year olds.",
                'path': "resources/data_exploration_plots_NCHS/mortality_age_boxplot.jpeg"
            },
            {
                'title': 'Fig. 5: Top 10 State Outliers for Drug Mortality',
                'desc': "These states had the top 10 most extreme death rates in 2016.",
                'path': "resources/data_exploration_plots_NCHS/state_outliers_2016.jpeg"
            }
        ],
        limitations="This dataset covers drug mortality rates from 1999-2016, so data is not available for the most recent years. Also, drug deaths can be underreported due to stigma and confounding factors.",
        advanced = {
            "image": "resources/data_exploration_plots_NCHS/QQ_death_rate.jpeg",
            'Interpretation':"Death rate is fairly normal, barring outliers at the extremes."

        }
    )

    # --- SECTION: TEDS-A ---
    data_source_section(
        title="TEDS-A 2023 Treatment Episode Data Set",
        df_raw="resources/teda_preview/raw_tedsa_preview.png",
        df_clean="resources/teda_preview/cleaned_tedsa_preview.png",
        source_info="[SAMHSA TEDS-A Dataset](https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles?data_collection=1011)",
        collection_method="Public-use dataset downloaded from SAMHSA website",
        description=(
            "TEDS-A is a national dataset of substance use treatment admissions, "
            "this dataset includes demographic information as well as treatment information. It captures all admissions "
            "to publicly funded treatment facilities in the U.S., helping to provide insight into substance"
            "use patterns and treatment trends. This is collected to monitor states substance use treatment systems."
        ),
        cleaning_steps={
            "Handling Missing Codes": "Converted SAMHSA missing codes (-9) to NaN. This was consistent across all questions.",
            "Column Retention": "Almost all original columns were kept, a select few that were redundant or added no value were dropped.",
            "Missing Column Values": "Columns missing atleast 50% of values were dropped, as they would not be helpful to computing results.",
            "Missing Row Values": "Rows with any missing values were dropped as the sample size was 1.5 million, it would still remain large after this.",
            "Renaming Columns": "Renamed columns to be more descriptive and human-readable by looking through the codebook provided on the website.",
            "Label Recoding": "Mapped numeric codes to human-readable labels for age, sex, race, substances, DSM diagnoses, and other categorical features.",  
            "Critical Value Filtering": "Dropped rows missing key variables such as AGE, SEX, SUB1, PSYPROB.",
            "Data Types" : "Ensured all object datatypes were changed to categorical. Those that were floats were not changed to integers as they had been changed when NaN was added in place of -9.",
            "Duplicates": "Ensured there were no duplicates.", 
            "Scaling & Log Transform": "Applied StandardScaler and log1p transform on numeric variables such as prior_tx and arrests_30days. Other transformation was not needed as the data is on a standardized small scale."
        },
        outliers={
            "image": "resources/data_exploration_tedsa/boxplot_tedsa.png",
            "Interpretation": "These outliers were not due to issues with the data but rather truthful outliers as the nature of the data does not allow for mistakes, using strict inputs.",
            "Action": "Nothing will be done for these at this moment but when experimenting with models this may change."
        },
        sum_stats={
            "Summary": "The mean, median, standard deviation, minimum, maximum, skewness, kurtosis, count, amount of missing values were computed for all relevant variables.",
            "Interpretation": "Age and educations are both roughly symmetric. Most of the variables are mildly skewed however there are some extremely skewed such as arrests_30days and self_help_30days."
        },
        corr={
            "image": "resources/data_exploration_tedsa/corr_tedsa.png",
            "Interpretation": "There are some strong correlations between variables such as route of administration and primary substance."
        },
        advanced={
            "image": "resources/data_exploration_tedsa/qq_tedsa_png.png",
            "Interpretation": "The data does not look normal on the Q-Q Plot however it is not continuous so this makes sense and is not a red flag."
        },
        visuals = [
            {'title': "Fig. 4",
            'desc': "Alaskian Native females seem to have the highest co-occurance of mental-health problems at admission.",
            'path': "resources/teds_visual/mh_race_tedsa.png"},
            {'title': 'Fig. 5',
            'desc':"Heatmap of age of first use with primary substance. Those whose first use was 30+ seem to gravitate to barbiturates.",
            'path':"resources/teds_visual/age_sub_tedsa.png"},
            {'title':'Fig. 6',
            'desc': "Those with less education while being unemployed seem to have been arrested more within the past 30 days of admission.",
            'path':"resources/teds_visual/employment_educ_tedsa.png"},
        ],
        notes=(
            "The dataset is quite large and complex, however the organization of the codebook helped tremendously with the process. It is important to note that there may be some missed biases or issues that need to be addressed with later modeling."
        ),
        limitations=(
            "This dataset represents treatment admissions rather than unique individuals, "
            "so repeat admissions by the same person are counted separately. "
            "Additionally because this dataset is so standardized there are missing values where answers were not applicable."
            "There was not much freedom with the data collection process, thus limiting the ability to capture the full complexity of individual experiences."
            "There are always potential biases due to systemic inequalities and prejudices."
        )
    )

    
    # --- SECTION: DATASET3 ---
    ## Datasets to display
connecticut_raw = pd.read_csv("c:/Users/jenny/Downloads/Connecticut_Accidental_Drug_Related_Deaths_Raw.csv")
connecticut_clean = pd.read_csv("c:/Users/jenny/Downloads/DataMining/HW/Clean_Connecticut_Accidental_Drug_Related_Deaths.csv")

with tab6:
    

    # FUNCTION FOR DATA EXPLORATION LAYOUT
    def data_source_section(title, df_raw, df_clean, source_info, collection_method, description, cleaning_steps, visuals, limitations):
        """
        Inputs will be displayed cleanly on the website
        title - title of dataset
        Ensure you load relevant versions of df_raw, df_clean earlier in this script (see TAB 6 comment above)
        source_info - where dataset came from
        collection_method - how you accessed the data (e.g. download, API, etc.)
        description - briefly describe dataset contents and why it's relevant to the project
        cleaning_steps - dictionary, {<step name> : <step description>}
        visuals - list of dictionaries, [{'title': <name of visual>,
                                        'desc': <description, insights, comments, etc.>,
                                        'path': <path to image>}]
        limitations - text describing any potential biases or limitations of data
        """
        with st.expander(f"📊 Dataset: {title}", expanded=False):
            st.subheader(title)
            
            # Overview
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                st.write(f"**Source:** {source_info}")
                st.write(f"**Collection Method:** {collection_method}")
            with col_meta2:
                st.markdown(f"**Description:** {description}")
            
            st.markdown("---")

            # Raw vs. Clean comparison
            st.subheader("Data Transformation Preview")
            col_pre1, col_pre2 = st.columns(2)
            
            with col_pre1:
                st.write("🔍 **Raw Snapshot**")
                st.dataframe(df_raw.head(5), use_container_width=True)
                st.caption("Initial data types and values.")
                with st.expander("View Raw Schema"):
                    st.code(df_raw.dtypes)

            with col_pre2:
                st.write("✨ **Processed Snapshot**")
                st.dataframe(df_clean.head(5), use_container_width=True)
                st.caption("Post-cleaning, encoding, and scaling.")
                with st.expander("View Processed Schema"):
                    st.code(df_clean.dtypes)

            st.markdown("---")

            # Summary Statistics
            st.subheader("Statistical Profile")
            st.write("Comparison of descriptive statistics before and after processing.")
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.write("**Raw Summary**")
                raw_stats = df_raw.select_dtypes(include=['number']).describe().T
                if not raw_stats.empty:
                    st.table(raw_stats)
                else:
                    st.warning("No numeric data found in Raw dataset.")
            
            with col_stat2:
                st.write("**Processed Summary**")
                clean_stats = df_clean.select_dtypes(include=['number']).describe().T
                if not clean_stats.empty:
                    st.table(clean_stats)
                else:
                    st.warning("No numeric data found in Processed dataset.")

            st.markdown("---")
            
            # Cleaning & Processing Steps
            st.subheader("Cleaning & Processing Logic")
            for step_title, step_desc in cleaning_steps.items():
                st.markdown(f"**{step_title}**")
                st.info(step_desc)

            st.markdown("---")

            # Visuals
            st.subheader("Visual Analysis")
            if visuals:
                for viz in visuals:
                    with st.container(border=True):
                        st.write(f"#### {viz['title']}")
                        st.write(viz['desc'])
                        st.image(viz['path'], use_container_width=True)
            else:
                st.info("Visualizations for this dataset are currently in progress.")


            # Bias/Limitations
            st.subheader("Limitations")
            if limitations:
                with st.container(border=True):
                    st.write(limitations)

    # --- SECTION: Connecticut Accidental Drug Related Deaths ---
    data_source_section(
        title="Connecticut Accidental Drug Related Deaths",
        df_raw=connecticut_raw,
        df_clean=connecticut_clean,
        source_info="Connecticut Open Data Portal",
        collection_method="API (Socrata SODA)",
        description="This dataset contains accidental drug related deaths reported in Connecticut including demographic information, substances detected in toxicology reports, and circumstances surrounding overdose deaths. It allows analysis of poly-drug overdoses, demographic trends, and seasonal patterns.",
        cleaning_steps={
            "Duplicate Removal": "Duplicate records were identified and removed so each death is counted once.",
            "Handling Missing Values": "Age values were converted to numeric and missing ages were filled with the median age. Missing categorical values were standardized where possible.",
            "Outlier Handling": "Extreme age values outside the range of 10–100 were removed to eliminate likely data entry errors.",
            "Binary Encoding": "Drug indicator columns were converted to binary format where 1 indicates the drug was present in the toxicology report.",
            "Feature Engineering": "A Drug Count variable was created by summing drug indicator columns to measure the number of substances involved in each overdose case.",
            "Normalization": "Age was standardized using z-score normalization and Drug Count was log-transformed to reduce skewness."
        },
        visuals = [
        
        {'title': 'Fig. 7: Drug Correlation Heatmap',
         
        'desc': "The heatmap shows that there is a weak positive correlation between Xylazine and Fentanyl. There is a strong correlation between Heroin and Heroin Morphine Codeine, meaning that the combination of Heroin Morphine and Codeine combination is prevalent.",
        
        'path': "resources/data_exploration_plots_CT/heatmap.png"},
        
        {'title': 'Fig. 8: Drug Count Distribution',
        
        'desc':"This visual is to compare the transformation of Drug Count prior to the log transformation. From the shape, we can see that the distribution is right-skewed.",
        
        'path':"resources/data_exploration_plots_CT/Drug Count Distribution.png"},
        
        {'title': 'Fig. 9: Log Drug Count Distribution',
        
        'desc':"After the transformation, the distribution of data is more balanced and compressed, especially for cases with larger numbers of drugs involved. The majority of the cases center around the middle of the distribution which is approximately 2-4 substances.",
        
        'path':"resources/data_exploration_plots_CT/Log Transformed Data Count Distribution.png"},
        
        {'title':'Fig. 10: Total Deaths Involving Each Drug',
        
        'desc': "From this bar chart, we can see that the leading drug causing overdoses in Connecticut from 2012 to 2024 is Fentanyl, with Cocaine and Heroin being second and third leading drug.",
        
        'path':"resources/data_exploration_plots_CT/Total Deaths Involving Each Drug.png"},
        
        {'title':'Fig. 11: Seasonality of Overdose Deaths',
        
        'desc': "From this bar chart, we can see that the peak summer months, June and July, tend to have slightly higher overdose cases than the other months.",
        
        'path': "resources/data_exploration_plots_CT/Seasonality of Deaths.png"},
        
        {'title':'Fig. 12: Number of Drugs Present in Each Overdose Case',
        
        'desc': "The histogram shows that the most common number of drugs present in each overdose case is 3. A large amount of overdose cases involve 2 to 5 drugs present, indicating that many overdoses involve multiple substances. The shape of the histogram is skewed to the right, with a tail towards 7 to 8 drugs.",
        
        'path': "resources/data_exploration_plots_CT/Number of Drugs Present.png"},
        
        {'title':'Fig. 13: Q-Q Plot of Age Distribution',
        
        'desc': "From this Q-Q plot we can see that the red line depicts a normal distribution. The data points for Age seem to follow the line around the center of the data, but deviates in the lower and upper tails. This means that in younger and older ages occur less frequently than a normal dsitribution would expect.",
        
        'path': "resources/data_exploration_plots_CT/QQ Plot.png"}],
        
        
        limitations="There are many ethical considerations that apply to this dataset because it contains very sensitive public health information involving deaths caused by overdoses. Another limitation is that there might be reporting biases amongst races and ethnicities. Plus, there are columns with several missing responses which may affect analysis and conclusions."
        
        )
    

    # --- SECTION: DEA Retail Drug Sales ---
    try:
        data_source_section(
            title="ARCOS Retail Drug Summary Reports",
            df_raw="resources/dea_preview/arcos_raw_sample.png",
            df_clean=dea_clean,
            source_info="U.S. Drug Enforcement Administration (DEA) / ARCOS Retail Drug Summary Reports",
            collection_method="ARCOS Query Tool (2006-2016); Manual extraction from PDF reports (2000-2005)",
            description="Reported controlled substances transactions by state. Proxy for availability of opioids (Hydrocodone, Oxycodone, and Fentanyl).",
            cleaning_steps={
                "Data Extraction": "For 2006-2016, data was extracted using the DEA ARCOS Query Tool. For 2000, 2001, and 2005, data was manually extracted from PDF reports and digitized.",
                "Data Loading": "Due to large size of ARCOS extract (422,647,324 rows), data was loaded in chunks and aggregated to state-year level to create a more manageable dataset for analysis.",
                "Handling Missing Values": "Missing values for 2002-2003 were imputed using linear interpolation based on adjacent years.",
            },
            limitations="Dataset only covers transactions reported to the DEA, so it may not capture all sources of opioids (e.g. illicit market)."
            )
    except Exception as e:
        st.error(f"Error loading DEA dataset: {e}")


    # --- SECTION: UKCPR National Welfare Data ---
    try:
        data_source_section(
            title="UKCPR Dational Welfare Data, 1980-2024",
            df_raw=ukcpr_raw,
            df_clean=ukcpr_clean,
            source_info="University of Kentucky Center for Poverty Research (UKCPR)",
            collection_method="Excel download from source website",
            description="State-level panel data series covering population, employment, unemployment, welfare, poverty, and politics.",
            cleaning_steps={
                "Feature Selection": "Keep only relevant columns such as year, state, population, unemployment rate, welfare spending, poverty rate, and political control.",
                "Handling Missing Values": "N/A; dataset is complete with no missing values.",
                "Data Reduction": "Filtered to include only 1999-2016 to align with NCHS mortality data for potential future modeling."
            },
            limitations="Older data may have lower accuracy."
            )
    except Exception as e:
        st.error(f"Error loading UKCPR dataset: {e}")

# ---------------------- TAB 7: MODELS IMPLEMENTED ----------------------

# Get the directory that app.py is in, then go up one level to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# CLUSTER MODEL REFERENCES
map_path = os.path.join(BASE_DIR, "resources", "death_rate_plots", "dominant_risk_profile_map_allyears.png")
map_shift = os.path.join(BASE_DIR, "resources", "death_rate_plots", "state_risk_map_eras.png")
schema_pre = pd.read_csv(os.path.join(BASE_DIR, "data", "death_rate_unscaled.csv"))
schema_post = pd.read_csv(os.path.join(BASE_DIR, "data", "death_rate.csv"))
distr_pre = os.path.join(BASE_DIR, "resources", "death_rate_plots", "unscaled_histograms.png")
distr_post = os.path.join(BASE_DIR, "resources", "death_rate_plots", "scaled_histograms.png")
clust_descriptions = """
    To determine the optimal number of clusters, we evaluated the model using three metrics. The Elbow Method suggested a clear transition at k=3 or k=4, and the Davies=Bouldin Index confirmed k=3 as most compact clustering. \n
    However, we ultimately selected k=4. Despite slightly increasing the DB Index, using 4 clusters enabled us to see the difference between high Oxycodone states and high Fentanyl states. \n
    We deemed the trade-off between minor loss in cluster quality and gain of qualitative nuance necessary to accurately study the shifting nature of the opioid crisis.
"""
performance_str = """
    We evaluate cluster performance using Silhouette Score and the Davies-Bouldin (DB) Index. \n
    The overall model's Silhouette Score (0.4675) is relatively low, but it was the best score possible with a reasonable amount of clusters.
    It's DB Index (0.9318) is poor, indicating clusters are not well separated as seen in the 3D visual below. \n
    In 2000-2005, both metrics improve. The Silhouette Score (0.5129) indicates better separation of clusters, as does the significantly reduced DB Index (0.5343). \n
    2006-2010 is the worst performaing era. Silhouette Score (0.3745) is low and DB Index (0.9647) is high, indicating poor separation of clusters. The visual below demonstrates how spread out some clusters are and the low degree of separation between many data points. \n
    2011-2016 improves slightly on the previous era with a higher Silhouette Score (0.4261) and lower DB Index (0.8814). The plot below visualizes the spread of clusters, where we can see that the Low and Moderate Risk clusters are pretty well-defined and separated.
    However, the High and Acute risk clusters are very spread out.
"""
challenge_dict = {
    "Ch1":{
        'name': "Data Accessability",
        'issue': 'Drug availability data from 2000-2005 was trapped in pdf reports from the DEA.',
        'sol': "Manually extracted and digitized data for 2000 and 2005, then use linear interpolation to fill in 2001-2004"
    },
    "Ch2":{
        "name": "Data Volume",
        "issue": "The DEA ARCOS data from 2006-2016 contained over 6 million rows, so loading and cleaning the data took over 30 minutes and often crashed the kernel.",
        "sol": "Processing and cleaning the data in chunks of 1 million rows each"
    },
    "Ch3": {
        "name": "Data Availability",
        "issue": "Initially the goal was to incorporate demographic data (age, sex, race) into the model. However, the NCHS data only provides this information at the national level.",
        "sol": "Drop age, sex, and race data from analysis"
    },
    "Ch4": {
        "name": "Multicollinearity",
        "issue": "Oxycodone and Hydrocodone supply were highly correlated (r = 0.73), as were SNAP rate and Poverty Rate (r = 0.71)",
        "sol": "Dropped Hydrocodone supply and Poverty rate from feature considerations since Oxycodone supply and SNAP rate were more highly correlated with death rate than their counterparts."
    }
}
assumption_dict = {
    "A1": {
        "assumption": "Clusters are spherical and isotropic",
        "assessment": "In general, clusters generated by our model are not spherical or isotropic. The exception is the Moderate Risk group which is approximately spherical in most models (see Performance Evaluation visuals above).\n The Silhouette Score for each models generally ranges between 0.4 to 0.5, indicating the assumption has not been violated too severely."
    },
    "A2": {
        "assumption": "Equal Variance of Clusters",
        "assessment": "Variance between clusters differs significantly. The Low Risk and Moderate Risk clusters generally have very low variance, between approx. 0.01 and 0.3. The Acute Risk cluster variance is higher, generally hovering around 0.5 - 0.6. The High Risk cluster's variance is extremely high (approx. 0.95)."
    },
    "A3": {
        "assumption": "Cluster Size Similarity",
        "assessment": "Cluster sizes are not evenly balanced, particularly in the Early Era",
        "viz": os.path.join(BASE_DIR,"resources","death_rate_plots","cluster_by_era_comp.png")
    }
}
death_rate_df = pd.read_csv(os.path.join(BASE_DIR,"data","death_rate_kmeans.csv"))
# define time periods
periods = [
    (2000, 2016, "Full Time Span (2000-2016)"),
    (2000, 2005, "Early Era (2000-2005)"),
    (2006, 2010, "Prescription Era (2006-2010)"),
    (2011, 2016, "Synthetic/Fentanyl Era (2011-2016)")
]

# Define specific color scale
color_mapping = {
    'Low Risk': '#2ecc71',
    'Moderate Risk': '#f1c40f',
    'High Risk (Prescription-Driven)': '#e67e22',
    'Acute High Risk (Fentanyl-Driven)': '#e74c3c'
}

from plot_utils import generate_era_3d_plots, generate_dominant_risk_map, generate_eras_map
from plot_utils import generate_interactive_heatmap
era_3d_plots = generate_era_3d_plots(death_rate_df,periods, color_mapping)
map_mode = generate_dominant_risk_map(death_rate_df, color_mapping)
eras_map = generate_eras_map(death_rate_df, periods, color_mapping)
heatmap_red_wall = generate_interactive_heatmap(death_rate_df)

with tab7:
    st.header("Models Implemented")
    st.info("Modeling is currently in progress and will be added to the website soon. Stay tuned!")

    # ------------------ CLUSTERING MODEL ------------------ #
    model_section(
        title = "Clustering of U.S. States Based on Drug Mortality Trends",
        model_type = "K-Means Clustering",
        description = "We applied K-Means clustering to group U.S. states based on their drug supply and minimum wages from 2000-2016. The goal was to identify clusters of states with similar characteristics and evaluate trends in their respective death rates.",
        justification = "K-Means is a simple and effective clustering algorithm that can help us uncover underlying patterns in the data. By clustering states and assessing each cluster's drug mortality rates, we can identify groups of states that may share common risk factors or policy environments.",
        assumptions = assumption_dict,
        hyperparameters = {
            "k": [4, "See images below"],
            "random_state": [42, "Set for reproduceability"],
            "max_iter": [300, "Left at default value; changes had no meaningful impact on Silhouette score"],
            "n_init": [20, "Adjusted from default 10 to improve Silhouette score"]
        },
        hyperparameter_viz={
            "Features & K Selection": {
                "path": os.path.join(BASE_DIR, "resources", "death_rate_plots", "cluster_feature_sets.png"),
                "description": "Optimal model features were initially selected based on Silhouette score. We wanted to include both Oxycodone and Fentanyl supply to determine if one or the other was a larger driver of death rate.",
                "cont_width": False
            },
            "K Validation": {
                "path": os.path.join(BASE_DIR, "resources", "death_rate_plots", "kmeans_evaluation_metrics.png"),
                "description": "Elbow Method and Silhouette Score \n ",
                "cont_width": True
            },
            "Davies-Bouldin Index & Cluster Identification": {
                "path": os.path.join(BASE_DIR,"resources","death_rate_plots","cluster_db_index.png"),
                "description": "While DB scores indicate k=3 as optimal cluster number, k=4 provides better insight to specific drivers of death rate.",
                "cont_width":False
            },
            "Cluster Descriptions": {
                "path":os.path.join(BASE_DIR,"resources", "death_rate_plots", "cluster_descriptions.png"),
                "description": clust_descriptions,
                "cont_width": False
            }

        },
        model_code="kmeans_final = KMeans(n_clusters=4, random_state=42, max_iter=300, n_init=20)",
        model_viz={
            "U.S. States by Predominant Cluster": {
                "path": map_mode,
                "description": "This map visualizes the clusters of states based on their drug mortality trends. Each color represents a different cluster, allowing us to see geographic patterns in drug mortality.",
                "cont_width": True
            },
            "State Cluster Shift": {
                "path": eras_map,
                "description": "Predominant cluster for each state during each era. Illustrates developing severity of risk of death from drug overdose over time.",
                "cont_width":True
            },
            "Drug Death Risk Heatmap": {
                "path": heatmap_red_wall,
                "description": "Sorted by risk level in 2016, this heatmap demonstrates the shift in drug death risk over time. Note the 'red wall' appearing in 2006 and taking over from then until 2016.",
                "cont_width": True
            }
        },
        performance_summary="Our data violates model assumptions, leading to relatively poor performance.",
        performance_eval=performance_str,
        performance_viz={
            "Comprehensive Analysis":{
                "fig": era_3d_plots[periods[0][2]]["fig"],
                "stats": era_3d_plots[periods[0][2]]["stats"],
                "cont_width":True
            },
            "Early Era Analysis": {
                "fig": era_3d_plots[periods[1][2]]["fig"],
                "stats": era_3d_plots[periods[1][2]]["stats"],
                "cont_width": True
            },
            "Mid Era Analysis": {
                "fig": era_3d_plots[periods[2][2]]["fig"],
                "stats": era_3d_plots[periods[2][2]]["stats"],
                "cont_width": True
            },
            "Late Era Analysis": {
                "fig": era_3d_plots[periods[3][2]]["fig"],
                "stats": era_3d_plots[periods[3][2]]["stats"],
                "cont_width": True
            }
        },
        preprocessing_steps={
            "Step 1": "Log transformation for drug quantities and other skewed continuous variables.",
            "Step 2" : "Z-Score Standardization of features",
            "Step 3": "Feature selection"
        },
        before_viz = schema_pre,
        after_viz = schema_post,
        before_distr = distr_pre,
        after_distr = distr_post,
        challenges=challenge_dict

    )
    # ------------------ END OF CLUSTERING MODEL ------------------ #
# --- Model 1 Image Paths (Mental Health) ---
    dt_feat_path = os.path.join(BASE_DIR, "resources", "model_viz", "dt_importance_tedsa.png")
    dt_model_path = os.path.join(BASE_DIR, "resources", "model_viz", "dt_model.png")
    roc_dt_path = os.path.join(BASE_DIR, "resources", "model_viz", "roc_dt.png")
    lr_model_path = os.path.join(BASE_DIR, "resources", "model_viz", "lr_model.png")
    roc_lr_path = os.path.join(BASE_DIR, "resources", "model_viz", "roc_lr.png")
    mh_before_path = os.path.join(BASE_DIR, "resources", "model_viz", "mh_before.png")
    mh_after_path = os.path.join(BASE_DIR, "resources", "model_viz", "mh_after_scale.png")

    # --- Model 2 Image Paths (Age of First Use) ---
    rf_feat_path = os.path.join(BASE_DIR, "resources", "model_viz", "rf_feat_importance.png")
    rf_eval_path = os.path.join(BASE_DIR, "resources", "model_viz", "rf_eval.png")
    rf_matrix_path = os.path.join(BASE_DIR, "resources", "model_viz", "rf_matrix.png")
    age_before_path = os.path.join(BASE_DIR, "resources", "model_viz", "age_before.png")
    age_after_path = os.path.join(BASE_DIR, "resources", "model_viz", "age_after_scale.png")


    # --- Isra's Model 1: Co-occurring Mental Health ---
# --- Isra's Model 1: Co-occurring Mental Health ---
# --- Isra's Model 1: Co-occurring Mental Health ---
    model_section(
        title="Predicting Co-occurring Mental Health Diagnoses",
        model_type="Decision Tree & Logistic Regression",
        description="Predicts the likelihood of a patient requiring dual-diagnosis treatment based on demographics and substance use risk factors.",
        justification="Decision trees handle highly categorical data without assuming linearity and provide clear feature importance. Logistic Regression serves as an industry-standard, highly interpretable baseline for overall probability.",
        
        # FIXED for Line 172: Nested Dictionary
        assumptions={
            "A1": {
                "assumption": "Decision Tree non-parametric",
                "assessment": "Assumes features have predictive power to create meaningful data splits."
            },
            "A2": {
                "assumption": "Logistic Regression Linearity",
                "assessment": "Assumes a linear relationship between the logits of the mental health diagnosis and the independent variables."
            }
        },
        
        # FIXED for Line 116: Dict with a 2-item List
        hyperparameters={
            "class_weight": ["'balanced'", "Ensures equal weighting of classes so the models aren't biased toward common outcomes during the 70/30 train-test split."]
        },
        
        model_viz={
            "Decision Tree Feature Importance": {
                "path": dt_feat_path, 
                "description": "Visualizing the strongest underlying risk factors driving the decision tree splits."
            }
        },
        preprocessing_steps={
            "Handling Missing Data": "Used dropna() on targets and primary predictors to ensure training on complete observations.",
            "One-Hot Encoding": "Expanded text categories into binary columns using pd.get_dummies.",
            "Scaling": "Transformed features into z-scores using StandardScaler so larger numerical ranges didn't disproportionately influence the logistic regression."
        },
        before_viz=mh_before_path, 
        after_viz=mh_after_path,   
        performance_eval=(
            "Both models achieved 60% accuracy, outperforming a random guess on the balanced test set. "
            "Logistic Regression generated a smooth ROC curve with an AUC of 0.64 (Decision tree: 0.63), indicating reliable, relatively linear relationships. "
            "Recall was nearly perfectly balanced (0.60 for class 0, 0.61 for class 1). "
            "Key Decision Tree insights showed 'No Prior Treatment' held 46% of the decision weight, followed by Race: Other (16%), Male (15%), and Methamphetamine/Speed use (6%)."
        ),
        performance_viz={
            "Decision Tree Evaluation": { "path": dt_model_path },
            "Decision Tree ROC Curve": { "path": roc_dt_path },
            "Logistic Regression Evaluation": { "path": lr_model_path },
            "Logistic Regression ROC Curve": { "path": roc_lr_path }
        },
        challenges={
            "C1": {
                "name": "Feature Scaling",
                "issue": "Logistic regression can be disproportionately influenced by variables with larger ranges.",
                "sol": "Applied StandardScaler across the features."
            }
        }
    )
    # --- Isra's Model 2: Age of First Use ---
# --- Isra's Model 2: Age of First Use ---
    model_section(
        title="Predicting Age of First Use",
        model_type="Random Forest Classifier",
        description="Predicts the discrete age bracket of a patient's first substance use based on primary substance choice and demographic background.",
        justification="Because age was recorded in discrete brackets rather than continuously, regression was not ideal. A Random Forest was chosen to mitigate overfitting and provide stability when dealing with complex data and many categorical features.",
        # FIXED: Nested Dictionary for Line 173
        assumptions={
            "A1": {
                "assumption": "Non-parametric",
                "assessment": "The model does not assume anything about the distribution of the data."
            },
            "A2": {
                "assumption": "Predictive Power",
                "assessment": "Assumes features have the predictive power necessary to make meaningful splits."
            }
        },
        # FIXED: Dictionary with 2-item list for Line 116
        hyperparameters={
            "n_estimators": [100, "Utilized 100 independent trees to ensure accurate split points and mitigate overfitting."],
            "max_depth": ["Tuned", "Ensured the model identified underlying patterns without getting lost in the noise."],
            "class_weight": ["'balanced'", "Critically important to prevent the model from defaulting to the most common age group."]
        },
        model_viz={
            "Random Forest Feature Importance": {
                "path": rf_feat_path,
                "description": "The strongest predictors for age of first use were specific substances."
            }
        },
        preprocessing_steps={
            "Handling Missing Data": "Used dropna() on the 'first_use' target and predictors.",
            "One-Hot Encoding": "Applied pd.get_dummies to process text categories independently.",
            "Scaling": "Applied StandardScaler to normalize features."
        },
        before_viz=age_before_path, 
        after_viz=age_after_path,   
        performance_eval=(
            "Evaluated via multi-class classification report and a chronological confusion matrix. "
            "The model achieved 20.2% accuracy across 7 categories (beating the random guess baseline of 14.2%). "
            "Its primary strength was identifying extreme age brackets, achieving a recall of 0.60 for the '< 11' group and 0.54 for the '30+' group. "
            "The top predictors were specific substances, namely Other Opiates (26.3%) and Synthetics/Heroin (20.9%)."
        ),
        performance_viz={
            "Evaluation Metrics": { "path": rf_eval_path },
            "Chronological Confusion Matrix": { "path": rf_matrix_path }
        },
        challenges={
            "C1": {
                "name": "Continuous vs. Discrete Target",
                "issue": "Initially, Linear Regression was considered but target was discrete brackets.",
                "sol": "Reframed the problem as a classification task using a Random Forest."
            }
        }
    )
# --- Model 1 Image Paths (Apriori / Association Rules) ---
apriori_before_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_apriori_before_transformation.png")
apriori_after_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_apriori_after_transformation.png")

# --- Model 2 Image Paths (Regression & Seasonality) ---
resid_before_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_residplot_before_transformation.png")
resid_after_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_residplot_after_transformation.png")
regress_before_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_regression_summary_before.png")
regress_after_path = os.path.join(BASE_DIR, "resources", "model_viz", "connecticut_regression_summary_after.png")
apriori_table_path = os.path.join(BASE_DIR, "resources", "model_viz", "apriori_algorithm_table.png")





# --- Andrea's Model 1: Deadliest Drug Combinations ---
model_section(
    title="Identifying Deadliest Drug Combinations",
    model_type="Apriori Algorithm & Association Rules",
    description=" This will help provide insight into the circumstances surrounding these deaths and determine which drugs are frequently used together. The apriori algorithm is the best model for this because in this case our 'market basket' will be the death’s related toxicology report to help uncover the deadliest drug pairings.",
    justification="The apriori algorithm is efficient for mining boolean data to find frequent itemsets through interpretable association rules based on support and confidence metrics.",
    
    assumptions={
        "A1": {
            "assumption": "Transaction Independence",
            "assessment": "Assumes each overdose case is an independent event."
        },
        "A2": {
            "assumption": "Minimum Frequency",
            "assessment": "Assumes drug combinations occurring in < 10% of cases are not primary patterns."
        }
    },
    
    hyperparameters={
        "min_support": ["0.1", "Requires combination to appear in at least 10% of cases."],
        "min_threshold": ["0.7", "70% confidence baseline for drug pairings."]
    },
    model_viz={
    "Frequent Itemsets": {
        "path": apriori_table_path,
        "description": "Visualizing the baseline frequencies..."
    }
},
    preprocessing_steps={
        "Feature Selection": "Isolated 18 specific substance columns from the dataset.",
        "Boolean Conversion": " I converted the selected drug columns to boolean types using .astype(bool) to create a correct market basket for the algorithm."
    },
    before_viz=apriori_before_path,
    after_viz=apriori_after_path,  
    performance_eval=(
        "The algorithm successfully identified primary substance threats. 67% of overdose cases involved Fentanyl, "
        "and approximately 40% involved Cocaine."
    ),
    challenges={
        "C1": {
            "name": "Threshold Tuning & Removing Drug",
            "issue": "An issue that occured was finding the right balance between support and confidence. Another issue was removing the 'Heroin Morphine Codeine' drug from the analysis because it was a combination of Heroin, Morphine, and Codeine, which made it difficult to interpret the results since we already have 'Heroin'.",
            "sol": "Iterative testing to find meaningful rules and comparing results from apriori with 'Heroin Morphine Codeine' versus without."
        }
    }
)

# --- Andrea's Model 2: Drug Overdose Seasonality & Trends ---
model_section(
    title="Predicting Drug Overdose Deaths: Seasonality & Trends",
    model_type="Ordinary Least Squares (OLS) Regression",
    description="Analyzes monthly overdose deaths to identify long-term yearly trends and test for statistically significant seasonal fluctuations.",
    justification="OLS Regression provides highly interpretable coefficients for time and month variables.",

    assumptions={
        "A1": {
            "assumption": "Linearity",
            "assessment": "Corrected by introducing a polynomial squared Year feature."
        },
        "A2": {
            "assumption": "Homoscedasticity",
            "assessment": "Corrected by applying a log transformation to the response variable, 'Deaths'."
        }
    },
    
    hyperparameters={
        "Formula": ["Log_Deaths ~ C(Month) + Year + I(Year**2)", "Forces categorical months and quadratic time trend."]
    },
    model_viz={
        "Regression Summary": {
            "path": regress_before_path,
            "description": "Summary output detailing R-squared, coefficients, and p-values before transformation."
        },
        "Regression Summary (Transformed)": {
            "path": regress_after_path,
            "description": "Summary output detailing R-squared, coefficients, and p-values after transformation."
        }

    },
    preprocessing_steps={
        "Aggregation": "Grouped data by 'Year' and 'Month'.",
        "Log Transformation": "Applied np.log() to the 'Deaths' column.",
        "Polynomial Features": "Squared the Year feature within the OLS formula."
    },
    before_viz=resid_before_path,
    after_viz=resid_after_path,  
    performance_eval="The final model achieved an R-squared of 0.883, explaining 88.3% of the variance.",
    performance_viz={
        "Initial Residual Plot": {"path": resid_before_path},
        "Transformed Residual Plot": {"path": resid_after_path}
    },
    challenges={
        "C1": {
            "name": "Violated Assumptions",
            "issue": "The initial residual plot showed a distinct parabolic pattern.",
            "sol": "Solved by squaring the Year feature & log transforming the response variable."
        }
    }
)
    # ------------------ END OF CLUSTERING MODEL ------------------ #
