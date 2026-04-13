import streamlit as st
import pandas as pd
import os

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