import streamlit as st
import pandas as pd

# Page layout
st.set_page_config(page_title="Substance Abuse/Overdose Analysis", layout="wide")

# title
st.title("Substance Abuse & Overdose Death")
st.markdown("---")

# 3 tabs
tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Research Questions", "Data", "Team Bios"])

# TAB 1: INTRODUCTION
with tab1:
    st.header("Project Introduction")

    # Research Topic & Significance 
    st.subheader("Problem Statement")
    st.write("""
The topic of our research project is predicting which communities are at a higher risk of drug abuse and/or drug overdose. By using socioeconomic, demographic, drug type, and past drug overdose data, we can help identify communities with high rates of substance abuse. Once these communities are identified, we will analyze the underlying factors that contribute to this elevated risk. Some of these factors could be housing insecurity, food insecurity, age, genetics, location, exposure to prescriptions drugs, or access to treatment. 
This research topic is important because substance abuse is prevalent in the United States. Drug overdose is the leading cause of death for Americans under 50 years old (Substance Abuse and Mental Health Services Administration, 2025). In 2024, only 1 in 5 people who suffer from drug abuse received treatment (SAMHSA, 2025).
If we could help predict which communities are at risk and why, it could help distinguish where substance abuse treatment resources need to go and identify which factors that lead to substance abuse. This research benefits treatment providers, schools and community organizations, and public health agencies.
    """)
    
    # Stakeholders
    st.subheader("Who is Affected?")
    st.write("""
Drug abuse has cascading effects across multiple industries. This research could help healthcare and public health industries take a preventative approach to substance abuse rather than a reactive one. Schools and community organizations will improve if preventative measures can be taken because drop-out rates will decrease and have identifiers for students and or participants for risk of drug abuse. Marginalized populations could benefit from this research because resources and treatment can be focused on these groups if they are identified, setting up these communities to succeed. Real-world implications of substance abuse are intergenerational substance abuse, increased taxes and spending to keep up with this crisis, and entrenched poverty.
    """)

    # Existing Solutions & Gaps
    st.subheader("Current Landscape")
    st.write("""
    There are many imperfect solutions to combat drug overdose and help mitigate drug abuse. In specific there are opioid overdose reversal medications (OORM) that are life-saving and reverse the effects of opioid overdose (Substance Abuse and Mental Health Services Administration, 2023). These medications are widely available for the general public and do not require training, significantly reducing overdose fatality rates (SAMHSA, 2023). Another way to reduce the risk of overdose is using test strips to check for the presence of fentanyl (toolkit). In general effective treatment of substance use disorder can reduce the risk of overdose and help combat drug use, whether that be through out-patient therapy or in-patient stay at a facility. There are many challenges regarding drug use; one is the inappropriate and over-prescribing of opioids, leading to misuse (Cerdá, Krawczyk, Keyes, 2023). In addition, the criminalization of drug use has harmed those that are users and/or in possession of drugs resulting in incarceration rather than treatment (Cerdá, Krawczyk, Keyes, 2023). 
    """)

    # Project Blueprint
    st.subheader("Roadmap")
    st.write("""
    The team will start with data preparation to extract relevant information from a variety of datasets and integrate them. Next, exploratory data analysis will help us understand the U.S. substance abuse and overdose landscape and identify interesting trends and patterns. For instance, we need to know the frequency of overdose for various drugs and communities with the highest rates of substance abuse. Then we will perform unsupervised learning (e.g. clustering) to determine risk profiles and dive deeper into identified patterns/trends. Finally we plan to see if we can predict individual treatment outcomes or overdose, or general overdose death in the future.
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

# TAB 3: DATA SOURCES
with tab3:
    st.header("Data Sources")
    st.subheader("Potential Sources for Analysis")

    st.info("💡 [Accidental Drug Related Deaths 2012-2014](https://catalog.data.gov/dataset/accidental-drug-related-deaths-2012-2018)")
    st.write("A listing of each accidental death associated with drug overdose in Connecticut from 2012 to 2024.")

    st.info("💡 [SUDORS Dashboard: Fatal Drug Overdose Data](https://www.cdc.gov/overdose-prevention/data-research/facts-stats/sudors-dashboard-fatal-overdose-data-accessible.html)")
    st.write("CDC data on unintentional and undetermined intent drug overdose deaths from death certificates, medical examiner or coroner reports, and postmortem toxicology results.")

    st.info("💡 [Treatment Episode Data Set: Admissions/Discharges (TEDS-A/D)](https://www.samhsa.gov/data/data-we-collect/teds-treatment-episode-data-set/datafiles/teds-d-2020)")
    st.write("When undergoing substance abuse treatment, individual people can be admitted and discharged from treatment multiple times. The Treatment Episode Data Set (TEDS) system comprises demographic and drug history information about these individuals.")

    st.info("💡 [Provisional Drug Overdose Death Counts for Specific Drugs](https://catalog.data.gov/dataset/provisional-drug-overdose-death-counts-for-specific-drugs)")
    st.write("The provisional data are based on a current flow of mortality data and include reported 12 month-ending provisional counts of drug overdose deaths by jurisdiction of occurrence and specified drug.")

    st.info("💡 [CDC Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)")
    st.write("Place-based index, database, and mapping application designed to identify and quantify communities experiencing social vulnerability.")

    st.info("💡 [NCHS - Drug Poisoning Mortality by State: United States](https://data.cdc.gov/National-Center-for-Health-Statistics/NCHS-Drug-Poisoning-Mortality-by-State-United-Stat/xbxb-epbu/data_preview)")
    st.write("This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning.")

    st.info("💡 [National Survey on Drug Use and Health (NSDUH)](https://www.samhsa.gov/data/data-we-collect/nsduh-national-survey-drug-use-and-health/datafiles?utm_source=chatgpt.com)")
    st.write("NSDUH measures substance use, mental illness, and treatment in the civilian noninstitutionalized population 12 or older.")


# TAB 4: TEAM BIOS
with tab4:
    st.header("The Team")
    
    # Creating a grid for team members
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("https://via.placeholder.com/150", width=150)
        st.write("**Andrea Caceres**")
        st.write("Role: TBD")
        st.caption("[GitHub](https://github.com/)") # add your personal link here
        st.caption("[LinkedIn](https://linkedin.com)") # add personal link here

    with c2:
        st.image("bio/IsraMarcu_Headshot.JPG", width=150)
        st.write("**Isra Marcu**")
        st.write("Role: Data & Analyzation Lead")
        st.write("Bio: Isra Marcu is a graduate student at the University of Colorado Boulder pursuing a Master’s in Data Science. She has a Bachelors in Psychology from the University of North Carolina at Chapel Hill. Isra has experience in ethically conducting research on participants and analyzing corresponding data.")
        st.caption("[GitHub](https://github.com/isram1223)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/isra-marcu-a220a1274/)")

    with c3:
        st.image("bio/Teetsel_Headshot.jpeg", width=150)
        st.write("**Amber Teetsel**")
        st.write("Role: Web Developer & Data Scientist")
        st.write("Bio: Amber Teetsel is currently pursuiing a Master's in Data Science at the University of Colorado Boulder. She has Bachelor's degrees from Vanderbilt University in Mathematics, Finance, and Women's Studies. Amber began her career in financial services consulting, but her past 4 years of experience have been as data analyst for a multinational corporation.")
        st.caption("[GitHub](https://github.com/amberteetsel)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/amber-teetsel/)")




