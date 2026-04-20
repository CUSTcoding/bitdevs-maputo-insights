import pandas as pd
import os

url = "https://docs.google.com/spreadsheets/d/1FX0YZa9hIbAut_vCN66OQroYDeuH_zlFOJAfHQCYs1M/export?format=csv&gid=1797247439"

df = pd.read_csv(url)

os.chdir("data/")

df.to_csv("bitdevsinquete.csv", index=False)

print("Ficheiro salvo com sucesso!")