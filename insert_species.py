from contextlib import nullcontext
import pandas as pd
from utils.base import SQLGenerator

# Carregar planilha e aba específica
file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, sheet_name="Informações sobre as espécies ")

# Instanciar gerador SQL
db = SQLGenerator(df)

for i, row in df.iterrows():
    species = str(row["vernacularName"]).replace("'", "''") 
    family = str(row["family"]).replace("'", "''") 
    scientificName = str(row["scientificName"]).replace("'", "''")
    authorship = str(row["authorship"]).replace("'", "''") 
    threatenedIUCN = str(row["threatenedStatusIUCN"]).replace("'", "''")
    threatenedCNCFLORA = str(row["threatenedStatusCNCFLORA"]).replace("'", "''")
    origin = str(row["origin"]).replace("'", "''") 
    endemism = str(row["endemism"]).replace("'", "''")
    height = str(row["height"]).replace("'", "''") 
    successionalStage = str(row["successionalStage"]).replace("'", "''") 
    functionalGroup = str(row["functionalGroup"]).replace("'", "''") 
    dispersalSyndrome = str(row["dispersalSyndrome"]).replace("'", "''")
    lifeCycle = str(row["lifeCycle"]).replace("'", "''") 
    foliage = str(row["foliage"]).replace("'", "''")
    pollinationSyndrome = str(row["pollinationSyndrome"]).replace("'", "''") 
    flowerFenology = str(row["flowerFenology"]).replace("'", "''")
    fruitFenology = str(row["fruitFenology"]).replace("'", "''")
    quantitySeed = str(row["quantitySeed (kg)"]).replace("'", "''")

    if species != "NULL":
        sql = f"""INSERT INTO species (vernacularName, family, scientificName, authorship, threatenedStatusIUCN, threatenedStatusCNCFLORA, origin, endemism, height, successionalStage, functionalGroup, dispersalSyndrome, lifeCycle, foliage, pollinationSyndrome, flowerFenology, fruitFenology, quantitySeed) 
        VALUES ('{species}', '{family}', '{scientificName}', '{authorship}', '{threatenedIUCN}', '{threatenedCNCFLORA}', '{origin}', '{endemism}', '{height}', '{successionalStage}', '{functionalGroup}', '{dispersalSyndrome}', '{lifeCycle}', '{foliage}', '{pollinationSyndrome}', '{flowerFenology}', '{fruitFenology}', '{quantitySeed}');"""
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
