import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from itertools import combinations
import os
import kaleido

# Get cleaned and scaled data
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "death_rate.csv"))

# Find optimal features by Silhouette Score
# Define the pool based on your pre-scaled columns
candidate_pool = [
    'log_oxy', 'log_fent', 
    'log_unempl_rate',
    'log_min_wage', 
    'log_gsp', 'snap_rate', 'poverty_rate', 'log_death_rate'
]

# Test different k values
k_values = [3, 4]

def find_optimal_features_multi_k(df, pool, ks, min_features=3, max_features=6):
    results = []
    
    # Pre-filter dataframe to only include pool columns to save memory in loops
    df_calc = df[pool].copy()
    
    for k in ks:
        print(f"Testing combinations for k={k}...")
        for r in range(min_features, max_features + 1):
            for combo in combinations(pool, r):
                features = list(combo)
                
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=20, init="k-means++",
                                max_iter=300)
                clusters = kmeans.fit_predict(df_calc[features])
                
                score = silhouette_score(df_calc[features], clusters)
                
                results.append({
                    'k': k,
                    'feature_count': r,
                    'features': features,
                    'silhouette': score
                })
                
    return pd.DataFrame(results)

# Run the search
results_df = find_optimal_features_multi_k(df, candidate_pool, k_values)

# --- Display Top 10 for each k ---
for k in k_values:
    print(f"\n{'='*20} Top 10 Feature Sets for k={k} {'='*20}")
    top_k = results_df[results_df['k'] == k].sort_values(by='silhouette', ascending=False).head(10)
    print(top_k[['feature_count', 'silhouette', 'features']])

# Test effects of using 3 or 4 clusters
# Define features used for clustering to ensure consistency
cluster_features = ['log_oxy', 'log_fent', 'log_min_wage']
X = df[cluster_features]

# Create two candidate clusterings
km_3 = KMeans(n_clusters=3, random_state=42, init="k-means++").fit_predict(X)
km_4 = KMeans(n_clusters=4, random_state=42, init="k-means++").fit_predict(X)

df['cluster_k3'] = km_3
df['cluster_k4'] = km_4

# calculate DB index score (want to minimize)
db_k3 = davies_bouldin_score(X, km_3)
db_k4 = davies_bouldin_score(X, km_4)

# Compare how they split the death rates
grouping_cols = ['log_death_rate', 'log_oxy', 'log_fent', 'log_gsp', 'log_min_wage']

print(f"{'='*10} 3 Clusters {'='*10}")
print(f"Davies-Bouldin Index: {db_k3:.4f}")
print(df.groupby('cluster_k3')[grouping_cols].mean())

print(f"\n{'='*10} 4 Clusters {'='*10}")
print(f"Davies-Bouldin Index: {db_k4:.4f}")
print(df.groupby('cluster_k4')[grouping_cols].mean())

# Define text labels for clusters
clustering_map = {
    0: 'Moderate Risk (Economic Protections)', # Higher wage, moderate deaths
    1: 'High Risk (Prescription-Driven)',      # Extreme Oxy levels
    2: 'Low Risk',                              # Negative values across the board
    3: 'Acute High Risk (Fentanyl-Driven)'      # Extreme Fentanyl levels
}

# color palette for clusters
color_discrete_map = {
    'Low Risk': '#2ecc71',                    # Green
    'Moderate Risk': '#f1c40f',               # Yellow
    'High Risk (Prescription-Driven)': '#e67e22', # Orange
    'Acute High Risk (Fentanyl-Driven)': '#e74c3c' # Red
}

# Elbow/Silhouette Analysis
cluster_features = ['log_oxy', 'log_fent', 'log_min_wage']
X = df[cluster_features]

inertia = []
sil_scores = []
K_range = range(1, 11)

# calculate metrics
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X)
    inertia.append(km.inertia_)
    if k > 1:
        sil_scores.append(silhouette_score(X, labels))

# side by side plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Elbow Method
ax1.plot(K_range, inertia, 'bo-', markersize=8, linewidth=2)
ax1.set_xlabel('Number of Clusters (k)', fontsize=12)
ax1.set_ylabel('Inertia (Total Variance)', fontsize=12)
ax1.set_title('Elbow Method for Optimal k', fontsize=14, fontweight='bold')
ax1.set_xticks(K_range)
ax1.grid(True, alpha=0.3)

# Silhouette Scores
ax2.plot(range(2, 11), sil_scores, 'ro-', markersize=8, linewidth=2)
ax2.set_xlabel('Number of Clusters (k)', fontsize=12)
ax2.set_ylabel('Silhouette Score', fontsize=12)
ax2.set_title('Silhouette Analysis for Optimal k', fontsize=14, fontweight='bold')
ax2.set_xticks(range(2, 11))
ax2.grid(True, alpha=0.3)

# Add a global title
plt.suptitle('K-Means Clustering Evaluation Metrics', fontsize=16, y=1.02)

plt.tight_layout()

# Save the combined plot
plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "kmeans_evaluation_metrics.png"), dpi=300, bbox_inches='tight')

# fit the final model and grab the labels 
kmeans_final = KMeans(n_clusters=4, random_state=42, max_iter=300, n_init=20)
df['cluster_num'] = kmeans_final.fit_predict(X) 

# add text labels
df['cluster_lab'] = df['cluster_num'].map(clustering_map)

# view cluster summary
cluster_summary = df.groupby('cluster_lab')[cluster_features].mean()
print(cluster_summary)

# Sort by mortality so they print in a logical order
ordered_clusters = ['Low Risk', 'Moderate Risk (Economic Protections)', 
                    'High Risk (Prescription-Driven)', 'Acute High Risk (Fentanyl-Driven)']

for cluster in ordered_clusters:
    if cluster in df['cluster_lab'].values:
        states = df[df['cluster_lab'] == cluster]['state'].unique()
        print(f"\nStates in {cluster}: {list(states)}")


# Predominant Risk Profile Map
state_identities = df.groupby('state')['cluster_lab'].agg(lambda x: x.mode()[0]).reset_index()

fig_mode = px.choropleth(
    state_identities,
    locations='state',
    locationmode="USA-states",
    color='cluster_lab',
    scope="usa",
    title="Predominant Risk Profile (2000-2016)",
    color_discrete_map=color_discrete_map,
    category_orders={"cluster_lab": ['Low Risk', 'Moderate Risk', 
                                    'High Risk (Prescription-Driven)', 
                                    'Acute High Risk (Fentanyl-Driven)']},
)
fig_mode.update_coloraxes(showscale=False)
fig_mode.update_traces(marker_line_color="white")
fig_mode.write_image(os.path.join(BASE_DIR, "resources", "death_rate_plots", "dominant_risk_profile_map_allyears.png"))

# Cluster Sizes by Era
periods_all = [
    (2000, 2016, "Full Time Span (2000-2016)"),
    (2000, 2005, "Early Era (2000-2005)"),
    (2006, 2010, "Prescription Era (2006-2010)"),
    (2011, 2016, "Synthetic/Fentanyl Era (2011-2016)")
]

# data prep
period_data = []
for start, end, label in periods_all:
    df_slice = df[(df['year'] >= start) & (df['year'] <= end)]
    # Calculate mode for each state in this period
    modes = df_slice.groupby('state')['cluster_lab'].agg(lambda x: x.mode()[0]).reset_index()
    modes['Era'] = label
    period_data.append(modes)

# Combine into one plotting dataframe
df_eras = pd.concat(period_data)

# 2. Plotting with Seaborn
sns.set_theme(style="white")
# Create a grid: 1 row, 3 columns (one for each era)
g = sns.FacetGrid(df_eras, col="Era", height=6, aspect=0.8)

# Use a categorical plot (stripplot or barplot) to show cluster distribution per era
g.map_dataframe(sns.countplot, y="cluster_lab", hue = "cluster_lab", palette=color_discrete_map, 
                order=['Low Risk', 'Moderate Risk', 
                       'High Risk (Prescription-Driven)', 
                       'Acute High Risk (Fentanyl-Driven)'])

g.set_axis_labels("Number of States", "")
g.set_titles("{col_name}")
plt.tight_layout()

# Save plot
plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "cluster_by_era_comp.png"), dpi=300)

# mapping labels
label_order = {
    'Low Risk': 0, 
    'Moderate Risk': 1, 
    'High Risk (Prescription-Driven)': 2, 
    'Acute High Risk (Fentanyl-Driven)': 3
}
df['risk_num'] = df['cluster_lab'].map(label_order)

# pivot
pivot_df = df.pivot(index="state", columns="year", values="risk_num")

# sort by risk
sort_cols = sorted(df['year'].unique(), reverse=True)
pivot_df_sorted = pivot_df.sort_values(by=sort_cols, ascending=False)


plt.figure(figsize=(14, 18)) # Height set to 18 to ensure 50 state labels are readable
sns.set_context("talk")
cmap = sns.color_palette([color_discrete_map[l] for l in label_order.keys()])

# heatmap
ax = sns.heatmap(
    pivot_df_sorted, 
    cmap=cmap, 
    linewidths=.5, 
    yticklabels=True, # Forces every state label to appear
    cbar_kws={'shrink': 0.5}
)

# customize legend
colorbar = ax.collections[0].colorbar
colorbar.set_ticks([0.375, 1.125, 1.875, 2.625]) # Centers labels on the colors
colorbar.set_ticklabels(list(label_order.keys()))

plt.title("The 'Red Wall': Opioid Risk Evolution (2000-2016)", fontsize=22, pad=20)
plt.xlabel("Year", fontsize=16)
plt.ylabel("State (Sorted by 2016 Risk)", fontsize=16)

# save fig
plt.savefig(os.path.join(BASE_DIR, "resources", "death_rate_plots", "risk_progression_heatmap_sorted.png"), dpi=300, bbox_inches='tight')


# Side by Side Predominant Risk Profiles by Era

# define time periods
periods = [
    (2000, 2005, "Early Era (2000-2005)"),
    (2006, 2010, "Prescription Era (2006-2010)"),
    (2011, 2016, "Synthetic/Fentanyl Era (2011-2016)")
]

# Define specific color scale
custom_colorscale = [
    [0.0, '#2ecc71'],  # Low Risk
    [0.33, '#f1c40f'], # Moderate Risk
    [0.66, '#e67e22'], # High Risk
    [1.0, '#e74c3c']   # Acute Risk
]

# three side-by-side subplots
fig = make_subplots(
    rows=1, cols=3, 
    subplot_titles=[p[2] for p in periods],
    specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}, {'type': 'choropleth'}]]
)

for i, (start, end, title) in enumerate(periods):
    df_slice = df[(df['year'] >= start) & (df['year'] <= end)]
    era_modes = df_slice.groupby('state')['cluster_lab'].agg(lambda x: x.mode()[0]).reset_index()
    
    # Add the map trace
    fig.add_trace(
        go.Choropleth(
            locations=era_modes['state'],
            z=era_modes['cluster_lab'].map(label_order), 
            locationmode='USA-states',
            colorscale=custom_colorscale,
            zmin=0,  # forces 0 to always be Green
            zmax=3,  # forces 3 to always be Red
            showscale=False,
            marker_line_color='white', # Sharpens the state borders
            marker_line_width=0.5
        ),
        row=1, col=i+1
    )

# USA only
fig.update_geos(scope="usa", projection_type='albers usa')

# layout
fig.update_layout(
    title_text="Geographic Evolution of Risk Profiles",
    title_x=0.5,
    width=1800,
    height=600,
    margin={"r":10,"t":100,"l":10,"b":10}
)

# save fig
fig.write_image(os.path.join(BASE_DIR, "resources", "death_rate_plots", "state_risk_map_eras.png"))

# 3D Interactive Cluster Plots by Era

periods_full = [
    (2000, 2016, "Full Time Span (2000-2016)"),
    (2000, 2005, "Early Era (2000-2005)"),
    (2006, 2010, "Prescription Era (2006-2010)"),
    (2011, 2016, "Synthetic/Fentanyl Era (2011-2016)")
]

# Dictionary to store figures for the app
era_3d_plots = {}

for start, end, title in periods_full:
    # Filter data for the era
    df_era = df[(df['year'] >= start) & (df['year'] <= end)]
    
    fig_3d = px.scatter_3d(
        df_era, 
        x='log_oxy', 
        y='log_fent', 
        z='log_min_wage',
        color='cluster_lab',
        symbol='cluster_lab',
        hover_name='state',
        hover_data=['year', 'death_rate'],
        title=f"3D Cluster Distribution: {title}",
        color_discrete_map=color_discrete_map,
        category_orders={"cluster_lab": ['Low Risk', 'Moderate Risk', 
                                        'High Risk (Prescription-Driven)', 
                                        'Acute High Risk (Fentanyl-Driven)']}
    )
    
    # Improve the look for Streamlit
    fig_3d.update_layout(
        margin=dict(l=0, r=0, b=0, t=50),
        scene=dict(
            xaxis_title='Log Oxycodone',
            yaxis_title='Log Fentanyl',
            zaxis_title='Log Min Wage'
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Store the object (not the path!) to keep it interactive
    era_3d_plots[title] = fig_3d

# Save clustered dataframe
df.to_csv(os.path.join(BASE_DIR, "data", "death_rate_kmeans.csv"))
