import streamlit as st
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Function to display results in app
def conclusion_section(
    title: str,
    summary: str,
    insights: dict,
    impact: str,
    limitations: dict,
    future: dict,
    improvements: dict=None,
):
    with st.expander(title, expanded=False):
        st.subheader("📝 Summary of Findings")
        st.write(summary)
        
        st.divider()

        # Insights Section
        st.markdown("### 🔍 Key Insights")
        for key, value in insights.items():
            st.markdown(f"**{key}:** {value}")

        st.divider()

        # Impact and Limitations in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌎 Real-World Impact")
            st.info(impact)
            
            st.markdown("### 🚀 Future Work")
            for idea, desc in future.items():
                st.markdown(f"- **{idea}**: {desc}")

        with col2:
            st.markdown("### ⚠️ Study Limitations")
            for lim, desc in limitations.items():
                # Using a warning box for the supply limitation specifically
                if "Supply" in lim:
                    st.warning(f"**{lim}**: {desc}")
                else:
                    st.write(f"• **{lim}**: {desc}")
            if improvements:
                st.markdown("### 🔧 Possible Improvements")
                for imp, desc in improvements.items():
                    st.markdown(f"- **{imp}**: {desc}")


# ------------- MORTALITY/CLUSTERING INPUTS ------------- #
title_mort = "Drug Mortality (2000 - 2016)"

sum_mort = """
    Our analysis tracked the progression of the opioid epidemic across the United States, 
    identifying distinct geographical shifts and the evolving relationship between 
    state-level policy and mortality rates.
"""

insights_mort = {
    'Mortality Trends': "Mortality rates from drug overdose have consistently climbed in the U.S. from 2000-2016, with higher rates among whites, men, and people aged 25-44.",
    'Clustering': "We were able to group states by their drug death risk profiles, providing a view into how the opioid crisis has evolved geographically over time.",
    'Economic Impact on Drug Death': "We disproved the concept that strong economic protections like high minimum wage reduce drug mortality."
}

impact_mort = """
    We found that minimum wages and overall drug supply cannot explain drug death rates.
    Policymakers should realize that economic 'safety nets' alone are insufficient to combat 
    the overdose crisis if the illicit supply remains unchecked.
"""

limitations_mort = {
    'Study Period': 'These insights only apply to drug death rates from 2000-2016, so we cannot comment on more recent trends',
    'Legitimate vs. Illicit Supply': "Our only data on drug supply comes from official transactions reported to the DEA, so we cannot incorporate the actual total drug supply per state.",
    'Lack of Data Granularity': "For privacy reasons, most data available on the opioid crisis is aggregated. This meant we could not access granular demographic information."
}

improvements_mort = {
    'Additional Data': "Incorporate additional factors that may affect drug death rates, such as demographic information.",
    'Linear Modeling': 'Expand and refine linear models used to investigate the Economic Protection Hypothesis',
}

future_mort = {
    'Cost of Living': "Looking into actual customer purchasing power may help explain the mortality paradox. The increased cost of living in states with high minimum wages may actually exacerbate economic pains.",
    'Population Density': 'Incorporate population density data. Higher-wage states often have denser urban areas which may facilitate more effecieint drug distribution networks, thus a faster spread of highly dangerous synthetic opioids like Fentanyl.',
    'Public Safety Net': 'Incorporate data on public spending to combat the opioid crisis. It is possible that the mortality gap is widened by states where higher minimum wages do not correspond with increased investment in Substance Use Disorder treatment or harm-reduction infrastructure.',
    'Realistic Wages of Overdose Victims': "Right now, we don't know whether overdose victims are actually earning the minimum wage, or if wage levels act as a proxy for broader economic trends. If overdose deaths are concentrated among unhoused or undocumented communities, minimum wage would have little to no bearing on drug mortality."
}
# ------------- END MORTALITY/CLUSTERING INPUTS ------------- #

# ------------- START ISRA INPUTS ------------- #
title_isra = "Substance Abuse Treatment"

sum_isra = """
    The goal of this research was to change how we look and approach substance abuse into a more proactive, predictive model of care. Analyzing about 1.6 million admission records for 2023, helped us develop a system that can identify a patient's specific risks. 
    One of the most significant findings is that the biggest red flag in regards to having a mental health issue is if you have been in treatment before. This means that those that are new to the system are at a higher risk for having a mental health disorder and need more rigorous testing.  Additionally the most significant predictor for age of first use is not a demographic but rather the type of drug used, in specific ‘Other Opiates’ and ‘Synthetics’ were the top two predictors. 
    This insight is valuable and can help treatment centers take the necessary steps to identify patients with extra risks and thus have more rigorous treatment plans and testing. It is important that we begin preventative models rather than simply caring for issues once they become prevelant. 
"""

insights_isra = {
    'Treatment Gap': "We discovered a treatment gap in the current healthcare intake system. The most common single predictor for co-occurring mental health diagnoses was 'No Prior Treatment', this accounted for 46 percent of the model's decision making weight. Additionally the logistic regression AUC of 0.64, suggests that patterns for co-occurring disorders are relatively linear, meaning both demographics and substance choice give a consistent foundation for early screening.",
    'Specific Drug Interactions': "Methamphetamine and Speed were identified as the highest risk substances to predict co-occurring mental health diagnoses, they contributed to 6 percent of the diagnostic splits.",
    'Demographics': "'Alaskan Native females' have the highest co-occurrence of mental health problems at the time of admission. This highlights the need for culturally specific resources.",
    'Age of First Use': "We found that substance type is the primary predictor for early use, specifically the use of 'Other Opiates' and 'Synthetics'. Additionally the random forest model showed that it has clinical value by identifying the extreme age brackets."
}

impact_isra = """
    The TEDS-A results provide a framework for new preventative approaches. 
    Specifically, using data-supported stratification to prioritize specific patients for more rigorous diagnostic testing, 
    would help to catch co-occurring mental health diagnoses, particularly for those in high-risk drug types. 
    Using the results from the model can help optimize the use of resources in areas of higher risk. 
    Additionally, this can further be used in legislative rulings to address the loops of generational poverty via identification and treatment. 
"""

limitations_isra = {
    'Data Structure': "The TEDS-A dataset provides latent data rather than longitudinal tracking, therefore making it impossible to analyze long-term treatment outcomes.",
    'Inherent Bias': "This data requires self-reporting which can lead to biases that can be influenced by social stigma in relation to substance use and mental health. ",
    'Data Integration': "The scope of our analysis was limited by the lack of clinical assessments."
}

future_isra = {
    'Additional Resources': "Inclusion of the WISC-V or other diagnostic tools can help with the accuracy of the diagnoses.",
    'Holistic View': "Incorporation of more data concerning more factors, along with application of predictive model across this field of research, can lead to a more holistic view of SUD and how to treat it."
}
# ------------- END ISRA INPUTS ------------- #