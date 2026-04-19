import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))

NSDUH = pd.read_csv(os.path.join(BASE_DIR, "data", "NSDUH_2024_Tab.txt"), sep = "\t")
NSDUH.to_csv(os.path.join(BASE_DIR, "data", "NSDUH_2024_Tab.csv"), index = False)

