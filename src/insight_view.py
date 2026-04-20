import streamlit as st
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Research Question Insight Template

def rq_section(
        title: str,
        research_question: str,
        approach: str,
        steps: dict,
        conclusion,
        recommendations = None
):
    with st.expander(title, expanded=False):
        st.markdown(f"### {research_question}")
        st.info(approach)

        st.divider()
        st.markdown("#### Analysis")
        
        # Iterate through the sub-sections (e.g., 'Incorporating the Influence...')
        for section_name, section_steps in steps.items():
            st.markdown(f"**{section_name}**")
            
            # Iterate through step1, step2, etc.
            for step_id, info in section_steps.items():
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if info['type'] == 'plot':
                        # Display Image
                        if os.path.exists(info['path']):
                            st.image(info['path'], use_container_width=True)
                        else:
                            st.warning(f"Plot not found at {info['path']}")
                            
                    elif info['type'] == 'table':
                        # Load and Display DataFrame
                        if os.path.exists(info['path']):
                            df_step = pd.read_csv(info['path'])
                            
                            # Clean up 'Unnamed' or index columns if they exist
                            if 'Unnamed: 0' in df_step.columns:
                                df_step = df_step.set_index('Unnamed: 0')
                                df_step.index.name = "Metric"
                            
                            st.dataframe(df_step, use_container_width=True)
                        else:
                            st.warning(f"Table not found at {info['path']}")

                with col2:
                    st.write(info['text'])
                
                st.write("") # Add some vertical padding between steps

        st.divider()
        st.markdown("### Conclusion")
        st.write(conclusion)

        if recommendations:
            st.markdown("#### Recommendations for Future Research")
            st.write(recommendations)

# To run it:
# rq_section(title, research_question_txt, approach_txt, steps_dict, conclusion_txt, recommendation_txt)
    

### Sample Inputs
title_econ_protect = "Economic Protection Hypothesis"
econ_research_question_txt = "Does higher minimum wage act as a buffer against high mortality rates, even when opioid availability is high?"
econ_approach_txt = """
    Our Economic Protection Hypothesis is that higher wages correlate with lower deaths, even when high drug supply is present.
    We will examine the full mortality dataset. In addition, we will compare the Moderate Risk cluster and the High Risk (Prescription-Driven) cluster.
    The Moderate Risk cluster is characterized by a high relative minimum wage, a below-average supply of opioids, and a slightly higher than average death rate.
    The High Risk cluster is characterized by a high relative minimum wage, an above-average supply of opioids, and the highest death rate of all clusters.
"""

wage_death_all_txt = """
    The regression plot visualizes the overall trend in our data: higher minimum wages are generally associated with higher death rates.
    This initial view appears to directly contradict our "Economic Protection" Hypothesis that high wages would be associated with lower death rates,
    and introduces a "Wage Paradox": why would stronger economic support correspond to higher drug deaths?
"""

cluster_comp_txt = """
    Compared to the Moderate Risk cluster, the High Risk cluster has a 14.5% higher average minimum wage, an 82.3% higher average death rate,
    and a higher than average drug supply across the board. Particularly of note is the massive oversupply of Fentanyl:
    +3.51 standard deviations higher than the Moderate Risk Cluster. \n
    We thus posit that in states with extreme opioid availability, the "Economic Protection" offered by higher wages is overwhelmed by the influence of drug supply.
"""

min_wage_cluster_txt = """
    The regression plot examines the correlation between minimum wage and death rate by the two clusters of interest (Moderate Risk and High Risk).
    The relative "flatness" of the regression lines emphasizes the low correlation of minimum wage with mortality in these clusters;
    some unknown factors are driving death rate (perhaps drug supply).
"""

lethality_gap_txt = """
    This plot splits the entire dataset by median minimum wage: states above the median are "High Wage" and states below it are "Low Wage". 
    We used the median rather than the mean becaues many states are stuck to the federal minimum wage of $7.25/hr. Using the median ensures a balanced split. \n
    This plot demonstrates that for most of the study period, states with higher minimum wages had higher drug supply *and* higher mortality rates than states with lower minimum wages. 
    This further confirms that "Economic Protections" matter less than the overall supply of Oxycodone and Fentanyl. 
    The gap between supply and mortality is also much more pronounced for high wage states in the early period (2000-2005). \n
    Interestingly, the drug supply for states with low minimum wages spiked higher than the supply for high minimum wage states in 2013/2014 (Fentanyl influx) 
    and stayed higher until the end of the study period (2016). 
    However, during this time the drug supply for high minimum wage states stayed consistent while mortality rates for these states continued to climb. 
    Mortality rates for low minimum wage states also climbed, but to a lesser degree and never exceeding mortality for high min. wage states. \n
    We proceed by building basic linear regression models to quantify the varying impacts of Minimum Wage and Drug Supply on Death Rate.
"""

modeling_txt = """
    **Naive Model:** Direct link between minimum wage and death rate. \n

    This model suggests that Minimum Wage alone explains about $23\%$ of the variance in death rates. 
    Ignoring all other variables, the wage coefficient $(0.4803)$ indicates that as wages go up, drug deaths increase significantly. 
    This overly simplistic model appears to confirms the contradiction we've been investigating; namely that higher wages lead to higher death rates.

    **Controlled Model:** Also accounts for Oxycodone and Fentanyl Supply.

    The 'Controlled' Model has a better R-Squared value than the Naive Model, implying that adding drug supply to the equation gives the model more predictive power. 
    The wage coefficient drops from $0.4803$ to $0.3192$ and Oxycodone supply seems to have equivalent predictive power over death rate with a coefficient of $0.3182$. 
    Its coefficient is nearly equal to that of wages suggesting that the economic environment is just as influential as the physical presence of opioids.

    **Interactive Model:** Examines the interaction effect between drug supply and minimum wage.

    The 'Interactive' Model fails to reveal a statistically significant interaction effect between minimum wage and overall drug supply. 
    It has the best R-Squared value of all models, accounting for approx. $33\%$ of the variability in death rate. 
    This was achieved by slightly shifting predictive emphasis from minimum wage (coefficient = $0.3081$) to the supply of Oxycodone (coefficient = $0.325$).

    **Interpretation:** Even accounting for drug supply and the interaction between supply and wages, higher minimum wages consistently predict higher death rates. 
    This suggests the paradox we've been investigating is a persistent structural feature of our data.

    **Limitations**
    - The models assume linear relationships between features and response that may not exist in the underlying data.
    - Log-transformations were utilized to normalize skewed drug supply and mortality data, meaning coefficients represent relative shifts rather than raw unit changes.
    - Drug supply here only refers to legitimate transactions reported to the DEA. We do not have solid data on the illicit marker supply, which could completely change the results of our analysis.
    - The models relied only on the predictive features our K-Means Clustering analysis chose as the optimal features for clustering (Minimum Wage, Oxycodone and Fentanyl supply). 
    Introducing a wider range of predictors could improve these models and lead to different conclusions.
"""

lethality_efficiency_txt = """
    While both wage groups had relatively stable lethality ratios across the study period (excluding high wage states in 2011), the High Wage states show a more consistent pattern.
    We conclude that drugs are not more deadly in High Wage states than Low Wage states.
    Instead, something about the environmental conditions of High Wage states is driving mortality in those areas.
"""

econ_steps_dict = {
    'Examining the Relationship Between Minimum Wage and Death Rate':{
        'step1': {'type': 'plot',
                  'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_plots", "death_v_minwage.png"),
                  'text': wage_death_all_txt
                  },
        'step2': {'type': 'table',
                  'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_tables", "high-mod-wage-death-supply-comp.csv"),
                  'text': cluster_comp_txt
                  },
        'step3': {'type': 'plot',
                  'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_plots", "minwage_death_by_cluster.png"),
                  'text': min_wage_cluster_txt
                  }                 
    },
    'Incorporating the Influence of Drug Supply':{
        'step1': {'type': 'plot',
                  'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_plots", "lethality_gap.png"),
                  'text': lethality_gap_txt
                  },
        'step2': {'type': 'table',
                  'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_tables", "lmod_comp.csv"),
                  'text': modeling_txt
                  },
        'step_3': {'type': 'plot',
                   'path': os.path.join(BASE_DIR.parent, "resources", "death_rate_plots", "lethality_ratio.png"),
                   'text': lethality_efficiency_txt}
    }
}

econ_conclusion_txt = """
    Our findings confirm a significant and persistent correlation between state-level minimum wages and opioid-related mortality. 
    Initial observations suggested a "Lethality Gap" wherein higher-wage states appeared to experience an outsized increase in mortality due to increasing supplies. 
    However, regression analysis on the full dataset indicates that the relationship is more structural.

    Through three stages of modeling, the positive correlation between minimum wage and death rate remained statistically significant even when controlling 
    for drug supply and potential interactive effects. 
    This suggests the "Wage Paradox" may be driven by specific environmental factors in high-wage states rather than the byproduct of higher-wage states having higher drug supply.

    Ultimately, drug supply remains the driver of the opioid crisis and the "Economic Protection" hypothesis is rejected. 
    Over 2000 - 2016, higher nominal wages correlate with increased mortality; 
    this phenomenom contradicts [traditional assumptions](https://odphp.health.gov/healthypeople/priority-areas/social-determinants-health) 
    about economic prosperity and public health outcomes.
"""

econ_recommendation_txt = """
    Though this study found a persistent correlation between higher minimum wages and overdose mortality, the underlying mechanisms (the "why?") require further investigation. 
    We recommend future research prioritize the following: \n

    1. **Cost of Living:** Looking into actual customer purchasing power may help explain the mortality paradox. 
    The increased cost of living in states with high minimum wages may actually exacerbate economic pains.

    2. **Population Density:** Higher-wage states often have denser urban areas which may facilitate more effecieint drug distribution networks, 
    thus a faster spread of highly dangerous synthetic opioids like Fentanyl.

    3. **Public Safety Net:** It's possible that the mortality gap is widened by states where higher minimum wages do not correspond with increased investment in Substance Use Disorder
    treatment or harm-reduction infrastructure.

    4. **Realistic Wages of Overdose Victims:** Right now, we don't know whether overdose victims are actually earning the minimum wage, 
    or if wage levels act as a proxy for broader economic trends. 
    If overdose deaths are concentrated among unhoused or undocumented communities, minimum wage would have little to no bearing on drug mortality.
"""