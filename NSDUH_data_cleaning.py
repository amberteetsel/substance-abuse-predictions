import pandas as pd 
NSDUH = pd.read_csv("data/NSDUH_2024_Tab.txt", sep = "\t")
NSDUH.to_csv("data/NSDUH_2024_Tab.csv", index = False)

