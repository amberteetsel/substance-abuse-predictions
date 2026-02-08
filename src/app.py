import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Substance Abuse/Overdose Analysis", layout="wide")

# Title of the main application
st.title("🔍 Data Mining Project: Substance Abuse & Overdose Death")
st.markdown("---")

# Create the three tabs as requested
tab1, tab2, tab3 = st.tabs(["Introduction", "Research Questions", "Team Bios"])

# --- TAB 1: INTRODUCTION ---
with tab1:
    st.header("Project Introduction")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Problem Statement")
        st.write("""
        Phe topic of our research project is predicting which communities are at a higher risk of drug abuse and or drug overdose.
        By using socioeconomic, demographic, drug type, and past drug overdose data, we can help identify communities to have a higher correlation with substance abuse.
        Once these communities are identified, we will analyze the underlying factors that contribute to this elevated risk.
        Some of these factors could be housing insecurity, food insecurity, age, genetics, location, exposure to prescriptions drugs, or access to treatment. 
        """)
        
        st.subheader("The Dataset")
        st.info("💡 **Source:** [Link to Kaggle/UCI/Source]")
        st.write("Our dataset contains X observations and Y features, focusing on...")

    with col2:
        # Placeholder for a conceptual image or project logo
        st.image("https://via.placeholder.com/400x300.png?text=Project+Visual", 
                 caption="Project Overview Visual")

# --- TAB 2: RESEARCH QUESTIONS ---
with tab2:
    st.header("Research Questions")
    st.write("We are applying data mining techniques to answer the following:")
    
    # Using a container for better organization
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

# --- TAB 3: TEAM BIOS ---
with tab3:
    st.header("The Team")
    
    # Creating a grid for team members
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.image("https://via.placeholder.com/150", width=150)
        st.bold("Andrea Cacares")
        st.write("Role: TBD")
        st.caption("[LinkedIn](https://linkedin.com)")

    with c2:
        st.image("https://via.placeholder.com/150", width=150)
        st.bold("Isra Marcu")
        st.write("Role: TBD")
        st.caption("[GitHub](https://github.com)")

    with c3:
        st.image("https://via.placeholder.com/150", width=150)
        st.bold("Amber Teetsel")
        st.write("Role: TBD")
        st.caption("[LinkedIn](https://www.linkedin.com/in/amber-teetsel/)")

