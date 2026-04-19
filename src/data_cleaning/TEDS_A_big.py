import pandas as pd 
import numpy as np
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))

TEDS_A = pd.read_csv(os.path.join(BASE_DIR, "data", "tedsa_puf_2006_2023.csv"))
#missing values are equal to -9, so replace
TEDS_A = TEDS_A.replace(-9,np.nan)
print(TEDS_A.columns.tolist())
# stratify sample because 32million will cause memory issues, year and stfips (based on codebook)

