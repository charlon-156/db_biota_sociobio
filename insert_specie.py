import pandas as pd
from utils.base import SQLGenerator

# Carregar planilha e aba específica
file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, sheet_name="espécies")

# Instanciar gerador SQL
db = SQLGenerator(df)

for i, row in df.iterrows():
    species = str(row["vernacularName"]).replace("'", "''") if pd.notna(row["vernacularName"]) else "NULL"
    family = str(row["family"]).replace("'", "''") if pd.notna(row["family"]) else "NULL"
    scientificName = str(row["scientificName"]).replace("'", "''") if pd.notna(row["scientificName"]) else "NULL"
    authorship = str(row["authorship"]).replace("'", "''") if pd.notna(row["authorship"]) else "NULL"
    threatenedIUCN = str(row["threatenedStatusIUCN"]).replace("'", "''") if pd.notna(row["threatenedStatusIUCN"]) else "NULL"
    threatenedCNCFLORA = str(row["threatenedStatusCNCFLORA"]).replace("'", "''") if pd.notna(row["threatenedStatusCNCFLORA"]) else "NULL"
    origin = str(row["origin"]).replace("'", "''") if pd.notna(row["origin"]) else "NULL"
    endemism = str(row["endemism"]).replace("'", "''") if pd.notna(row["endemism"]) else "NULL"

    if species != "NULL":
        sql = f"""INSERT INTO species (vernacularName, family, scientificName, authorship, threatenedStatusIUCN, threatenedStatusCNCFLORA, origin, endemism) VALUES ('{species}', '{family}', '{scientificName}', '{authorship}', '{threatenedIUCN}', '{threatenedCNCFLORA}', '{origin}', '{endemism}');"""
        db.inserts.append(sql)
    else:
        db.erros.append({
            "linha_excel": i+2,
            "species": row.get("vernacularName"),
            "scientificName": row.get("scientificName")
        })

# Salvar e relatar
db.save_sql("inserts_species.sql")
db.report()
