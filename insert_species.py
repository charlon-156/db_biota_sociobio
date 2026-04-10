import pandas as pd
from utils.base import SQLGenerator

# 1. CARREGAMENTO DOS DADOS
file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, sheet_name="Informações sobre as espécies ")

db = SQLGenerator(df)

def escape_text(value):
    # Escapa aspas simples e retorna None se valor for vazio ou NaN
    if pd.isna(value) or value is None:
        return None
    value = str(value).strip()
    if value == "":
        return None
    return value.replace("'", "''")

# 3. LOOP PRINCIPAL
for i, row in df.iterrows():

    vernacular_raw = escape_text(row.get("vernacularName"))

    if not vernacular_raw:
        db.erros.append({
            "linha Excel": i + 2,
            "vernacularName": row.get("vernacularName"),
            "scientificName": row.get("scientificName")
        })
        continue

    vernacular = f"'{vernacular_raw}'"

    #Campos textuais 
    family_raw = escape_text(row.get("family"))
    scientific_raw = escape_text(row.get("scientificName"))
    authorship_raw = escape_text(row.get("authorship"))
    threatenedIUCN_raw = escape_text(row.get("threatenedStatusIUCN"))
    threatenedCNCFLORA_raw = escape_text(row.get("threatenedStatusCNCFLORA"))
    origin_raw = escape_text(row.get("origin"))
    endemism_raw = escape_text(row.get("endemism"))
    height_raw = escape_text(row.get("height"))
    successional_raw = escape_text(row.get("successionalStage"))
    functional_raw = escape_text(row.get("functionalGroup"))
    dispersal_raw = escape_text(row.get("dispersalSyndrome"))
    lifeCycle_raw = escape_text(row.get("lifeCycle"))
    foliage_raw = escape_text(row.get("foliage"))
    pollination_raw = escape_text(row.get("pollinationSyndrome"))
    flower_raw = escape_text(row.get("flowerFenology"))
    fruit_raw = escape_text(row.get("fruitFenology"))
    quantity_raw = escape_text(row.get("quantitySeed (kg)"))

    # Converte None → NULL
    family = f"'{family_raw}'" if family_raw else "NULL"
    scientific = f"'{scientific_raw}'" if scientific_raw else "NULL"
    authorship = f"'{authorship_raw}'" if authorship_raw else "NULL"
    threatenedIUCN = f"'{threatenedIUCN_raw}'" if threatenedIUCN_raw else "NULL"
    threatenedCNCFLORA = f"'{threatenedCNCFLORA_raw}'" if threatenedCNCFLORA_raw else "NULL"
    origin = f"'{origin_raw}'" if origin_raw else "NULL"
    endemism = f"'{endemism_raw}'" if endemism_raw else "NULL"
    height = f"'{height_raw}'" if height_raw else "NULL"
    successionalStage = f"'{successional_raw}'" if successional_raw else "NULL"
    functionalGroup = f"'{functional_raw}'" if functional_raw else "NULL"
    dispersalSyndrome = f"'{dispersal_raw}'" if dispersal_raw else "NULL"
    lifeCycle = f"'{lifeCycle_raw}'" if lifeCycle_raw else "NULL"
    foliage = f"'{foliage_raw}'" if foliage_raw else "NULL"
    pollinationSyndrome = f"'{pollination_raw}'" if pollination_raw else "NULL"
    flowerFenology = f"'{flower_raw}'" if flower_raw else "NULL"
    fruitFenology = f"'{fruit_raw}'" if fruit_raw else "NULL"
    quantitySeed = f"'{quantity_raw}'" if quantity_raw else "NULL"


    sql = f"""INSERT INTO species (vernacularName, family, scientificName, authorship, threatenedStatusIUCN, threatenedStatusCNCFLORA, origin, endemism, height, successionalStage, functionalGroup, dispersalSyndrome, lifeCycle, foliage, pollinationSyndrome, flowerFenology, fruitFenology, quantitySeed)
        VALUES ({vernacular}, {family}, {scientific}, {authorship}, {threatenedIUCN}, {threatenedCNCFLORA}, {origin}, {endemism}, {height}, {successionalStage}, {functionalGroup}, {dispersalSyndrome}, {lifeCycle}, {foliage}, {pollinationSyndrome}, {flowerFenology}, {fruitFenology}, {quantitySeed});"""

    db.inserts.append(sql)


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_species.sql")
db.report()
