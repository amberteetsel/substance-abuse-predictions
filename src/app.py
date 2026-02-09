import streamlit as st
import pandas as pd

# Page layout
st.set_page_config(page_title="Substance Abuse/Overdose Analysis", layout="wide")

# title
st.title("Substance Abuse & Overdose Death")
st.markdown("---")

# 3 tabs
tab1, tab2, tab3 = st.tabs(["Introduction", "Research Questions", "Team Bios"])

# TAB 1: INTRODUCTION
with tab1:
    st.header("Project Introduction")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Problem Statement")
        st.write("""
        The topic of our research project is predicting which communities are at a higher risk of drug abuse and or drug overdose.
        By using socioeconomic, demographic, drug type, and past drug overdose data, we can help identify communities with high risk with substance abuse and/or overdose.
        Once these communities are identified, we will analyze the underlying factors that contribute to this elevated risk.
        Some of these factors could be housing insecurity, food insecurity, age, genetics, location, exposure to prescriptions drugs, or access to treatment. 
        """)
        
        st.subheader("Potential Datasets")
        st.info("💡 [Accidental Drug Related Deaths 2012-2024](https://catalog.data.gov/dataset/accidental-drug-related-deaths-2012-2018)")
        st.write("Our dataset contains X observations and Y features, focusing on...")

    with col2:
        # Placeholder for a conceptual image or project logo
        st.image("https://via.placeholder.com/400x300.png?text=Project+Visual", 
                 caption="Project Overview Visual")

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
        9. Can we forecast the next XX months of overdose death for specific drugs?

        """)
        
    st.divider()
    st.subheader("Proposed Methodology")
    st.write("Methodology to follow")

# TAB 3: TEAM BIOS
with tab3:
    st.header("The Team")
    
    # Creating a grid for team members
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("bio/AndreaCaceres_Headshot.jpg", width=150)
        st.write("**Andrea Caceres**")
        st.write("Role: Modeling and Visualization Lead")
        st.caption("[LinkedIn](linkedin.com/in/andrea-caceres-609609256")
        st.write("Andrea Caceres is a graduate student at the University of Colorado Boulder with a Bachelors in Statistics from the University of Georgia. She has experience in pensions analysis from her prior position at WTW, but is focusing on expanding her data analytical knowledge. ")

    with c2:
        st.image("bio/IsraMarcu_Headshot.JPG", width=150)
        st.write("**Isra Marcu**")
        st.write("Role: Data & Analyzation Lead ")
        st.write("Bio: Isra Marcu is a graduate student at the University of Colorado Boulder pursuing a Master’s in Data Science. She has a Bachelors in Psychology from the University of North Carolina at Chapel Hill. Isra has experience in ethically conducting research on participants and analyzing corresponding data.")
        st.caption("[GitHub](https://github.com/isram1223)")
        st.caption("[LinkedIn](https://www.linkedin.com/in/isra-marcu-a220a1274/)")

    with c3:
        st.image("bio/Teetsel_Headshot.jpeg", width=150)
        st.write("**Amber Teetsel**")
        st.write("Role: Web Developer & Data Scientist")
        st.caption("[LinkedIn](https://www.linkedin.com/in/amber-teetsel/)")
        st.caption("[GitHub](https://github.com/amberteetsel)")



