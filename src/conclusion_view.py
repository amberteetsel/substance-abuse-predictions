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
    improvements: dict,
    future: dict,
):
    with st.expander(title, expanded=True):
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

            st.markdown("### 🔧 Possible Improvements")
            for imp, desc in improvements.items():
                st.markdown(f"- **{imp}**: {desc}")


# ------------- MORTALITY/CLUSTERING INPUTS ------------- #
title_mort = "Drug Mortality (2000 - 2016)"

sum_mort = """
    Explain findings in simple terms
"""

insights_mort = {
    'Mortality Trends': "description of insight",
    'Economic Impact on Drug Death': "We disproved the concept that strong economic protections like high minimum wage reduce drug mortality."
}

impact_mort = """
    Real world implications of results...
"""

limitations_mort = {
    'Study Period': 'These insights only apply to drug death rates from 2000-2016',
    'Legitimate vs. Illicit Supply': "Our only data on drug supply comes from official transactions reported to the DEA, so we cannot incorporate the actual total drug supply per state.",
    'Another Limitation': "description..."
}

improvements_mort = {
    'idea1': 'description',
    'idea2': 'description2',
}

future_mort = {
    'idea1': "description",
    'idea2': 'description'
}
# ------------- END MORTALITY/CLUSTERING INPUTS ------------- #