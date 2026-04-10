import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv("data/tedsa_puf_2023_first_use.csv", low_memory=False)

# Select features and target
features = ['sex_label', 'race_label', 'educ_label', 'sub1_label', 'mental_health']
target = 'first_use_label'

# Create model dataframe
modeldf = df[features + [target]].dropna()

#snapshot
print("\n Snapshot: Before Transformation (Raw Categorical)")
print(modeldf[features].head(3))

#transformation encoding
x = pd.get_dummies(modeldf[features], drop_first=True)
y = modeldf[target] 

#snapshot
print("\n Snapshot: After Transformation (One-Hot Encoded)")
print(x.head(3))

#train and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

#scaling
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

#snapshot 
print("\n Snapshot: After Scaling")
print(pd.DataFrame(x_train_scaled, columns=x.columns).head(3))

#modeling
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
model.fit(x_train_scaled, y_train)

#predict
y_pred = model.predict(x_test_scaled)

#evaluate
print("\n Evaluation Metrics:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

#top predictors 
important = pd.DataFrame({'Feature': x.columns,'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)
print(important.head(5).to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 6))
ordered_labels = ['≤11', '12-14', '15-17', '18-20', '21-24', '25-29', '30+']
ConfusionMatrixDisplay.from_estimator(model, x_test_scaled, y_test, ax=ax, cmap="Purples", labels=ordered_labels)
plt.title("Confusion Matrix: Predicted vs. Actual Age")
plt.show()