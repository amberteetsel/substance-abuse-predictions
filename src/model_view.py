import streamlit as st
import pandas as pd
import os

def model_section(
    title: str,
    model_type: str,
    description: str,
    justification: str,
    assumptions: dict,
    hyperparameters: dict, # New format: {name: [value, tuning_desc]}
    model_viz: dict=None,   # New format: {name: {"path": obj, "description": text}}
    performance_eval: str=None,
    performance_viz: dict=None,
    preprocessing_steps: dict=None,
    before_viz=None,
    after_viz=None,
    challenges: dict=None
):
    def render_visual(obj):
        if obj is None: return
        if hasattr(obj, 'data'): st.plotly_chart(obj, use_container_width=True)
        elif isinstance(obj, pd.DataFrame): st.dataframe(obj, use_container_width=True)
        elif isinstance(obj, str):
            # Basic check to see if string is a path or just text
            if obj.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                st.image(obj, use_container_width=True)
            else:
                st.write(obj)

    with st.expander(f"📌 {title}"):
        st.caption(f"Category: {model_type}")
        
        # --- OVERVIEW ---
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("### Description")
            st.write(description)
        with col2:
            st.markdown("### Selection Justification")
            st.write(justification)

        # --- DATA TRANSFORMATION ---
        st.markdown("---")
        st.markdown("### 🛠 Data Formatting & Preprocessing")
        if preprocessing_steps:
            for step, desc in preprocessing_steps.items():
                st.write(f"- **{step}:** {desc}")
        
        col_before, col_after = st.columns(2)
        with col_before:
            st.write("**Before Transformation**")
            render_visual(before_viz)
        with col_after:
            st.write("**After Transformation**")
            render_visual(after_viz)

        # --- NESTED TABS ---
        st.markdown("---")
        st.markdown("### 🔍 Model Details & Evaluation")
        tab_specs, tab_perf, tab_challenges = st.tabs([
            "Technical Specs", "Performance Evaluation", "Implementation Challenges"
        ])

        with tab_specs:
            # Layout for Hyperparameters with tuning descriptions
            st.markdown("#### Hyperparameters & Tuning")
            # Create a dataframe for a clean table view of hyperparameters
            hp_data = []
            for param, info in hyperparameters.items():
                # info[0] is value, info[1] is tuning description
                hp_data.append({"Parameter": param, "Value": info[0], "Tuning Process": info[1]})
            st.table(hp_data)

            st.markdown("#### Model Assumptions")
            for k, v in assumptions.items():
                st.write(f"- **{k}:** {v}")
            
            if model_viz:
                st.markdown("#### Model Visualizations")
                for name, content in model_viz.items():
                    with st.container():
                        st.markdown(f"**{name}**")
                        # Handle the nested dict format
                        if isinstance(content, dict):
                            render_visual(content.get("path"))
                            st.caption(content.get("description", ""))
                        else:
                            render_visual(content)

        with tab_perf:
            st.write(performance_eval)
            if performance_viz:
                for name, viz in performance_viz.items():
                    st.write(f"**{name}**")
                    render_visual(viz)

        with tab_challenges:
            if challenges:
                for issue, sol in challenges.items():
                    st.markdown(f"🚩 **Challenge:** {issue}\n\n💡 **Solution:** {sol}")
    """
    Inputs will be displayed cleanly on the website
    title: Descriptive Name of Model and Relevant Dataset (e.g. "Random Forest on Customer Churn Data")
    model_type: e.g. "Random Forest Classifier", "Linear Regression", etc.
    description: Brief overview of the model's purpose and how it fits into the project.
    justification: Why this model was chosen for the task (e.g. handles non-linearity).
    assumptions: Dictionary of key assumptions made when implementing the model.
    hyperparameters: Dictionary of the hyperparameters used, their values, and explanation of tuning process.
    model_viz: (Optional) Dictionary containing paths to visualizations related to the model.
    performance_eval: Text describing how the model's performance was evaluated.
    performance_viz: (Optional) Dictionary containing paths to visualizations of performance metrics.
    preprocessing_steps: Dictionary of preprocessing steps taken before modeling
    before_viz: (Optional) Visualization showing data before preprocessing
    after_viz: (Optional) Visualization showing data after preprocessing
    challenges: Dictionary describing any challenges faced during model implementation and how they were addressed.
    """