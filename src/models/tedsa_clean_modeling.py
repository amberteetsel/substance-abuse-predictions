import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


df = pd.read_csv("data/tedsa_puf_2023_cleaned.csv", low_memory=False)

#select variables 
features = ['age_label', 'sex_label', 'race_label', 'employment_label', 'sub1_label', 'prior_tx_label']
target = 'mental_health'

#df for the model 
modeldf = df[features + [target]].dropna()
print(modeldf.head().to_string()) 

#text labels to binary
x = pd.get_dummies(modeldf[features], drop_first=True)
y = modeldf[target]

#snapshot
print("\n"+ "Preprocessing Snapshot: Before Transformation")
print(modeldf[features].head(3)) 

print("\n" + "Preprocessing Snapshot: After Encoding")
print(x.head(3)) 

#train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42, stratify=y)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train) 
x_test_scaled = scaler.transform(x_test) 

print("\nPreprocessing Snapshot 3: After Scaling (First 3 rows)")
print(pd.DataFrame(x_train_scaled, columns=x.columns).head(3))

print("\n" + "Model 1: Decision Tree")
dt = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')
dt.fit(x_train, y_train)
dt_pred = dt.predict(x_test)
print(classification_report(y_test, dt_pred))
print("ROC AUC:", roc_auc_score(y_test, dt.predict_proba(x_test)[:, 1]))

print("\n" + "Model 2: Logistic Regression")
lrmodel = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lrmodel.fit(x_train_scaled, y_train)
lr_pred = lrmodel.predict(x_test_scaled)
print(classification_report(y_test, lr_pred))
print("ROC AUC:", roc_auc_score(y_test, lrmodel.predict_proba(x_test_scaled)[:, 1]))

#top predictor
important = pd.DataFrame({'Feature': x.columns,'Importance': dt.feature_importances_}).sort_values(by='Importance', ascending=False)
print(important.head(5).to_string(index=False))

# ROC Curve
RocCurveDisplay.from_estimator(dt, x_test, y_test, curve_kwargs={"color": "pink"})
plt.title("ROC Curve - Decision Tree")
plt.show()

RocCurveDisplay.from_estimator(lrmodel, x_test_scaled, y_test, curve_kwargs={"color": "lightblue"})
plt.title("ROC Curve - Logistic Regression")
plt.show()