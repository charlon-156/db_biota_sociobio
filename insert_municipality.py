###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_municipality.py
# description: Generates SQL INSERT statements for the
#              municipalities table based on municipality.xlsx
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/municipality.xlsx

2. Transformações realizadas:
   - Conversão segura de campos numéricos (db.num)
   - Escape de campos textuais
   - Mapeamento de RGI, RGINT e Region via dicionários

3. Validações:
   - municipalityID válido
   - rgiID e rgintID existentes no map
   - Apenas registros com integridade referencial geram INSERT

4. Estrutura SQL gerada:
   INSERT INTO municipalities (...)
"""

import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_rgi, map_rgint, map_region

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

file_path = "docs/municipality.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def escape_text(value):
    # Escapa aspas simples para evitar erro de sintaxe SQL
    if pd.isna(value):
        return None
    return str(value).replace("'", "''")


# ============================================================
# 3. LOOP PRINCIPAL
# ============================================================

for i, row in df.iterrows():

    # ---------- Conversão segura de ID ----------
    municipalityID = db.num(row.get("municipalityID"))

    # ---------- Campos textuais ----------
    municipality_raw = escape_text(row.get("municipality"))
    municipality = f"'{municipality_raw}'" if municipality_raw else "NULL"

    # ---------- Mapeamento de chaves estrangeiras ----------
    # Remove espaços extras antes do mapeamento
    rgi = map_rgi.get(str(row.get("rgi")).strip())
    rgint = map_rgint.get(str(row.get("rgint")).strip())
    region = map_region.get(str(row.get("locality")).strip())

    # ---------- Conversão numérica padronizada ----------
    area = db.num(row.get("areaKM2"))
    population = db.num(row.get("population"))
    man = db.num(row.get("man"))
    woman = db.num(row.get("woman"))
    genderRatio = db.num(row.get("genderRatio"))
    averageAge = db.num(row.get("averageAge"))
    populationDensity = db.num(row.get("populationDensity"))
    populationProtectedArea = db.num(row.get("populationProtectedArea"))
    indigenousPopulation = db.num(row.get("indigenousPopulation"))
    insideIndigenousLand = db.num(row.get("insideIndigenousLand"))
    outsideIndigenousLand = db.num(row.get("outsideIndigenousLand"))
    quilombolaPopulation = db.num(row.get("quilombolaPopulation"))
    insideQuilombolaLand = db.num(row.get("insideQuilombolaLand"))
    outsideQuilombolaLand = db.num(row.get("outsideQuilombolaLand"))
    populationByRaceAmarela = db.num(row.get("populationByRaceAmarela"))
    populationByRaceBranca = db.num(row.get("populationByRaceBranca"))
    populationByRaceIndigena = db.num(row.get("populationByRaceIndigena"))
    populationByRaceParda = db.num(row.get("populationByRaceParda"))
    populationByRacePreta = db.num(row.get("populationByRacePreta"))

    # ========================================================
    # 4. VALIDAÇÃO DE INTEGRIDADE REFERENCIAL
    # ========================================================
    # Só gera INSERT se:
    # - municipality não for NULL
    # - rgi e rgint existirem no mapa
    # Isso evita erro de foreign key no banco

    if municipality != "NULL" and rgi and rgint:

        sql = f"""INSERT INTO municipalities
        (municipalityID, municipality, rgiID, rgintID, regionID, areaKM2, population, man, woman, genderRatio, middleAge, populationDensity, populationProtectedArea, indigenousPopulation, insideIndigenousLand, outsideIndigenousLand, quilombolaPopulation, insideQuilombolaLand, outsideQuilombolaLand, populationByRaceAmarela, populationByRaceBranca, populationByRaceIndigena, populationByRaceParda, populationByRacePreta)
        VALUES ({municipalityID}, {municipality}, {rgi}, {rgint}, {region}, {area}, {population}, {man}, {woman}, {genderRatio}, {averageAge}, {populationDensity}, {populationProtectedArea}, {indigenousPopulation}, {insideIndigenousLand}, {outsideIndigenousLand}, {quilombolaPopulation}, {insideQuilombolaLand}, {outsideQuilombolaLand}, {populationByRaceAmarela}, {populationByRaceBranca}, {populationByRaceIndigena}, {populationByRaceParda}, {populationByRacePreta});"""


        db.inserts.append(sql.strip())

    else:
        # Registra erro para auditoria posterior
        db.erros.append({
            "linha Excel": i + 2,
            "municipalityID": municipalityID,
            "municipality": row.get("municipality"),
            "rgi": row.get("rgi"),
            "rgint": row.get("rgint")
        })

# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_municipalities.sql")
db.report()
