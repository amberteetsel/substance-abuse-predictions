import streamlit as st
import pandas as pd
import os

def model_section(
    title: str,
    model_type: str,
    description: str,
    justification: str,
    assumptions: dict,
    hyperparameters: dict, 
    hyperparameter_viz: dict=None,
    model_code = None,
    model_viz: dict=None,
    performance_summary: str=None,   
    performance_eval: str=None,
    performance_viz: dict=None,
    preprocessing_steps: dict=None,
    before_viz=None,
    after_viz=None,
    before_distr=None,
    after_distr=None,
    challenges: dict=None,
):
    def render_visual(obj, label=None, cont_width=True):
        if obj is None: return
        
        if isinstance(obj, pd.DataFrame):
            st.write(f"🔍 **{label} Snapshot**" if label else "")
            st.dataframe(obj.head(5), use_container_width=cont_width)
            st.caption("Snapshot of first 5 rows.")
            with st.expander(f"View {label if label else 'Data'} Schema"):
                st.code(obj.dtypes)
        
        elif hasattr(obj, 'data'): 
            st.plotly_chart(obj, use_container_width=cont_width)
            
        elif isinstance(obj, str):
            if obj.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                st.image(obj, use_container_width=cont_width)
            else:
                st.write(obj)

    def process_viz_dict(viz_dict):
        if not viz_dict: return
        for name, content in viz_dict.items():
            with st.container():
                st.markdown(f"**{name}**")
                
                # Check if we have stats to display side-by-side
                has_stats = isinstance(content, dict) and "stats" in content
                
                if has_stats:
                    col_plot, col_stats = st.columns([3, 1]) # 3:1 ratio
                    with col_plot:
                        render_visual(content.get("path") or content.get("fig"), cont_width=content.get("cont_width", True))
                    with col_stats:
                        st.markdown("##### Era Metrics")
                        for metric, val in content["stats"].items():
                            st.metric(label=metric, value=val)
                    st.markdown("----")
                else:
                    # Standard rendering for items without stats
                    if isinstance(content, dict):
                        render_visual(content.get("path"), cont_width=content.get("cont_width", True))
                        if content.get("description"):
                            st.caption(content.get("description"))
                    else:
                        render_visual(content)

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
        st.markdown("### 🛠️ Data Formatting & Preprocessing")
        if preprocessing_steps:
            for step, desc in preprocessing_steps.items():
                st.write(f"- **{step}:** {desc}")
        
        col_before, col_after = st.columns(2)
        with col_before:
            render_visual(before_viz, label="Before Transformation")
            render_visual(before_distr, label="Continuous Variable Distribution")
        with col_after:
            render_visual(after_viz, label="After Transformation")
            render_visual(after_distr, label="Continuous Variable Distribution")

        # --- NESTED TABS ---
        st.markdown("---")
        st.markdown("### 📊 Model Details & Evaluation")
        tab_specs, tab_perf, tab_challenges = st.tabs([
            "Technical Specs", "Assumptions & Performance", "Implementation Challenges"
        ])

        with tab_specs:
            if model_code:
                st.markdown("#### Final Model")
                st.code(model_code, language='python')
                st.markdown("---")

            st.markdown("#### Hyperparameters & Tuning")

            # turn input dict into DataFrame
            hp_df = pd.DataFrame([
                {"Parameter": param, "Value": info[0], "Tuning Process": info[1]}
                for param, info in hyperparameters.items()
            ])

            # configure columns
            st.dataframe(
                hp_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Parameter": st.column_config.TextColumn(
                        "Parameter",
                        help="The specific model hyperparameter",
                        width="medium",
                    ),
                    "Value": st.column_config.TextColumn(
                        "Value",
                        width="small",
                    ),
                    "Tuning Process": st.column_config.TextColumn(
                        "Tuning Process",
                        width="large", # Forces more space to prevent line breaks
                    )
                }
            )

            # Styling for centering (CSS Hack)
            st.markdown("""
                <style>
                    [data-testid="stDataFrame"] td {
                        text-align: center !important;
                    }
                    /* Keep Tuning Process left-aligned for readability if desired, 
                    otherwise the rule above centers everything */
                    [data-testid="stDataFrame"] td:nth-child(3) {
                        text-align: left !important;
                    }
                </style>
            """, unsafe_allow_html=True)

            # --- NEW: Hyperparameter Visualizations Section ---
            if hyperparameter_viz:
                process_viz_dict(hyperparameter_viz)
            

        with tab_perf:
            if performance_summary:
                st.markdown("### Overall Assessment")
                st.write(performance_summary)

            st.markdown("#### Performance Evaluation")
            st.write(performance_eval)
            if performance_viz:
                process_viz_dict(performance_viz)

            
            st.markdown("#### Model Assumptions")
            for key, details in assumptions.items():
                name = details.get("assumption", "N/A")
                assess = details.get("assessment", "N/A")
                st.markdown(f"**Assumption:** {name}")
                st.markdown(f"**Assessment:** {assess}")
                if details.get("viz"):
                    render_visual(details.get("viz"))
                st.markdown("---")
            
        with tab_challenges:
            if challenges:
                for key, details in challenges.items():
                    # Extract values from the sub-dictionary
                    name = details.get('name', 'N/A')
                    issue = details.get('issue', 'N/A')
                    sol = details.get('sol', 'N/A')
                    
                    # Display the formatted markdown
                    st.markdown(f"🔧 **{name}:** {issue}")
                    st.markdown(f"💡 **Solution:** {sol}")
                    st.markdown("---")

        # Model Visuals
        if model_viz:
            st.markdown("---")
            st.markdown("#### 📈 Model Visualizations")
            process_viz_dict(model_viz)