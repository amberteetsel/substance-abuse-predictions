#%%
import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.formula.api import ols
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv("../../data/Clean_Connecticut_Accidental_Drug_Related_Deaths.csv")
df.head()

#remove 'Heroin Morphine Codeine' column from list of drugs as it is redundant with the 'Heroin' column for Apriori analysis.
drugs = [
'Heroin','Cocaine','Fentanyl','Fentanyl Analogue','Oxycodone',
'Oxymorphone','Ethanol','Hydrocodone','Benzodiazepine',
'Methadone','Methamphetamine','Amphetamine','Tramadol',
'Hydromorphone','Morphine','Xylazine',
'Gabapentin','Opiate NOS']

basket = df[drugs].astype(bool)
frequent_itemsets = apriori(basket, min_support=0.1, use_colnames=True)
frequent_itemsets=frequent_itemsets.sort_values(by="support", ascending = False)
print(frequent_itemsets)

#67% of overdose cases from the data involve Fentanyl. Approximately 40% of overdose cases involve Cocaine. Approximately 30% of overdoses involve a combination of Fentanyl and Cocaine.

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
rules = rules.sort_values(by="confidence", ascending = False)

print("\n--- Top Association Rules - Deadliest Combinations  ---")
# Displaying just the most readable columns
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

#Regression Modeling for Drug OD Seasonality
monthlydeaths = df.groupby(['Year', 'Month']).size().reset_index(name='Deaths')
lm = ols('Deaths ~ C(Month) + Year', data=monthlydeaths).fit()
print(lm.summary())
#R^2 value of 0.64, inidicating that 64% of the variability in the data is explained by this model.


residuals = lm.resid
predicted = lm.fittedvalues
plt.figure(figsize=(10,6))
sns.scatterplot(x=predicted, y=residuals)
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()
#The plot shows a distinct parabolic pattern, indicating that the assumptions of linearity has been violated. Squaring the Year feature could help address this issue by allowing the model to capture the non-linear relationship between Year and Deaths. Additionally, the variance of the residuals appears to increase as the predicted values increase, suggesting heteroscedasticity. This could be addressed by applying a log transformation to the dependent variable (Deaths) to stabilize the variance.


#log transformation of deaths and squared the Year feature to address heteroscedasticity and non-linearity in the data. The residual plot shows a more random pattern, indicating that the assumptions of linear regression are better satisfied after the transformation.
monthlydeaths = df.groupby(['Year', 'Month']).size().reset_index(name='Deaths')
monthlydeaths['Log_Deaths'] = np.log(monthlydeaths['Deaths'])
log_lm = ols('Log_Deaths ~ C(Month) + Year + I(Year**2)', data=monthlydeaths).fit()
print(log_lm.summary())
#From the summary output we can see that the R^2 value is now 0.883, meaning that 88.3% of the variability is explained by the model. The coefficients for the month variables indicate the relative increase or decrease in log deaths compared to the reference month (January). The positive coefficient for Year suggests that log deaths tend to increase over time, while the negative coefficient for Year^2 indicates a decelerating effect of time on log deaths. None of the p-values for the month variables are statistically significant, this suggests that there are no statistically significant differences in log deaths across different months, indicating a lack of seasonality in drug overdose deaths. There is one marginally significant month variable, June, with a p-value of 0.062 and a positive coefficient of 0.1212. This suggests that there may be a slight increase in log deaths in June compared to January, but this result should be interpreted with caution due to the marginal significance level.

residuals = log_lm.resid
predicted = log_lm.fittedvalues

plt.figure(figsize=(10,6))
sns.scatterplot(x=predicted, y=residuals)
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

#MSE & RMSE
mse = log_lm.mse_resid
rmse = np.sqrt(mse)

print(f"\n--- Model Error Metrics ---")
print(f"MSE (Log Scale): {mse:.4f}")
print(f"RMSE (Log Scale): {rmse:.4f}")
#%%