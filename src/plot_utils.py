# plot_utils.py
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score, davies_bouldin_score
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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

# Interactive Map
def generate_dominant_risk_map(df, color_map):
    # Calculate mode
    state_identities = df.groupby('state')['cluster_lab'].agg(lambda x: x.mode()[0]).reset_index()

    fig = px.choropleth(
        state_identities,
        locations='state',
        locationmode="USA-states",
        color='cluster_lab',
        scope="usa",
        title="Predominant Risk Profile (2000-2016)",
        color_discrete_map=color_map,
        category_orders={"cluster_lab": ['Low Risk', 'Moderate Risk', 
                                        'High Risk (Prescription-Driven)', 
                                        'Acute High Risk (Fentanyl-Driven)']},
        # Rename the label for the legend/hover
        labels={'cluster_lab': 'Risk Profile'}
    )
    
    fig.update_layout(
        margin={"r":0,"t":50,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    fig.update_traces(marker_line_color="white")
    fig.update_traces(
        hovertemplate="<b>%{location}</b><br>Profile: %{customdata[0]}<extra></extra>",
        customdata=state_identities[['cluster_lab']]
    )
    
    return fig

def generate_eras_map(df, periods, color_dict):
    active_periods = periods[1:4]
    custom_colorscale = [
        [0.0, color_dict['Low Risk']],
        [0.25, color_dict['Low Risk']],
        [0.25, color_dict['Moderate Risk']],
        [0.5, color_dict['Moderate Risk']],
        [0.5, color_dict['High Risk (Prescription-Driven)']],
        [0.75, color_dict['High Risk (Prescription-Driven)']],
        [0.75, color_dict['Acute High Risk (Fentanyl-Driven)']],
        [1.0, color_dict['Acute High Risk (Fentanyl-Driven)']]
    ]
    label_order = {'Low Risk':0, 'Moderate Risk':1,
                   'High Risk (Prescription-Driven)':2, 'Acute High Risk (Fentanyl-Driven)':3}
    fig = make_subplots(
        rows=1, cols=3, 
        subplot_titles=[p[2] for p in active_periods],
        specs=[[{'type': 'choropleth'}]*3]
    )

    for i, (start, end, title) in enumerate(active_periods):
        df_slice = df[(df['year'] >= start) & (df['year'] <= end)]
        era_modes = df_slice.groupby('state')['cluster_lab'].agg(lambda x: x.mode()[0]).reset_index()
        era_modes['z_value'] = era_modes['cluster_lab'].map(label_order)
        
        # Add the map trace
        fig.add_trace(
            go.Choropleth(
                locations=era_modes['state'],
                z=era_modes['cluster_lab'].map(label_order), 
                locationmode='USA-states',
                colorscale=custom_colorscale,
                zmin=0, 
                zmax=3,
                showscale=False,
                marker_line_color='white',
                marker_line_width=0.5,
                customdata=np.expand_dims(era_modes['cluster_lab'].values, axis=-1),
                hovertemplate="<b>%{location}</b><br>Profile: %{customdata[0]}<extra></extra>"
            ),
            row=1, col=i+1
        )

    # USA only
    fig.update_geos(scope="usa", projection_type='albers usa')

    # layout specs
    fig.update_layout(
        title_text="Geographic Evolution of Risk Profiles",
        title_x=0.39,
        width=1800,
        height=600,
        margin={"r":10,"t":100,"l":10,"b":10}
    )

    return fig


def generate_interactive_heatmap(df):

    label_order = {
        'Low Risk': 0, 
        'Moderate Risk': 1, 
        'High Risk (Prescription-Driven)': 2, 
        'Acute High Risk (Fentanyl-Driven)': 3
    }

    # sorting logic
    sort_cols = sorted(df['year'].unique(), reverse=True)
    pivot_df = df.pivot(index="state", columns="year", values="risk_num")
    pivot_df_sorted = pivot_df.sort_values(by=sort_cols, ascending=False)

    colors = ['#27ae60', '#f1c40f', '#e67e22', '#e74c3c']

    fig = px.imshow(
        pivot_df_sorted,
        labels=dict(x="Year", y="State", color="Risk Level"),
        color_continuous_scale=colors,
        zmin=0, zmax=3,
        aspect="auto"
    )

    fig.update_traces(
        xgap=0.5,
        ygap=0.5,
        selector=dict(type='heatmap')
    )

    # legend
    for label, val in label_order.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker = dict(size=10, color=colors[val], symbol='square'),
            showlegend=True,
            name=label
        ))

    # custom data for hover
    death_rates = df.pivot(index="state", columns="year", values="death_rate").reindex(pivot_df_sorted.index).values
    
    fig.update_traces(
        customdata=death_rates,
        hovertemplate=(
            "<b>State:</b> %{y}<br>" +
            "<b>Year:</b> %{x}<br>" +
            "<b>Death Rate:</b> %{customdata:.2f}<extra></extra>"
        ),
        selector=dict(type='heatmap')
    )
    # fig.update_traces(marker_line_color="white")
    fig.update_layout(
        title="Opioid Risk Evolution (2000-2016)",
        height=1200,
        # title_font_size=22,
        coloraxis_showscale=False,
        legend=dict(
            title="Risk Categories",
            orientation="v",
            yanchor="bottom",
            y=.91,
            xanchor="right",
            x=1.3
        ),
        yaxis=dict(tickmode='linear'), # Ensures every state name is printed
        margin=dict(l=150)
    )
    
    return fig