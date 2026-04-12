# plot_utils.py
import plotly.express as px
from sklearn.metrics import silhouette_score, davies_bouldin_score

def generate_era_3d_plots(df, periods, color_mapping):
    era_plots = {}
    risk_order = ['Low Risk', 'Moderate Risk', 'High Risk (Prescription-Driven)', 'Acute High Risk (Fentanyl-Driven)']
    features = ['log_oxy', 'log_fent', 'log_min_wage']

    for start, end, title in periods:
        df_era = df[(df['year'] >= start) & (df['year'] <= end)].copy()
        
        # Calculate Metrics
        s_score = silhouette_score(df_era[features], df_era['cluster_lab'])
        db_index = davies_bouldin_score(df_era[features], df_era['cluster_lab'])
        
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
        
        # Store both the figure and the metrics
        era_plots[title] = {
            "fig": fig,
            "stats": {
                "Silhouette Score": round(s_score, 4),
                "Davies-Bouldin Index": round(db_index, 4)
            }
        }
    return era_plots