# plot_utils.py
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score

def generate_era_3d_plots(df, periods, color_mapping):
    era_plots = {}
    risk_order = ['Low Risk', 'Moderate Risk', 'High Risk (Prescription-Driven)', 'Acute High Risk (Fentanyl-Driven)']
    features = ['log_oxy', 'log_fent', 'log_min_wage']

    for start, end, title in periods:
        df_era = df[(df['year'] >= start) & (df['year'] <= end)].copy()
        
        # basic metrics
        s_score = silhouette_score(df_era[features], df_era['cluster_lab'])
        db_index = davies_bouldin_score(df_era[features], df_era['cluster_lab'])
        
        stats_dict = {
            "Global Silhouette": round(s_score, 3),
            "Global DB Index": round(db_index, 3)
        }

        # variance
        cluster_groups = df_era.groupby('cluster_lab')[features]
        counts = cluster_groups.size()
        variances = cluster_groups.var().mean(axis=1) # Average variance across the 3 features

        for label in risk_order:
            if label in counts.index:
                n = counts[label]
                # Variance requires N > 1
                if n > 1:
                    stats_dict[f"{label} Variance"] = round(variances[label], 3)
                else:
                    stats_dict[f"{label} Variance"] = "N/A (N=1)"
            else:
                stats_dict[f"{label} Variance"] = "None"

        # 3D plot
        fig = px.scatter_3d(
            df_era, x='log_oxy', y='log_fent', z='log_min_wage',
            color='cluster_lab', title=f"3D Clusters: {title}",
            color_discrete_map=color_mapping,
            category_orders={'cluster_lab': risk_order},
            labels={'cluster_lab':'Cluster Label'},
            hover_name='state'
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=40),
            legend=dict(traceorder="normal", itemsizing="constant")
        )
        
        era_plots[title] = {
            "fig": fig,
            "stats": stats_dict
        }
        
    return era_plots