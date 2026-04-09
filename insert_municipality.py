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
from utils.helpers import normalize_map, safe_map

<<<<<<< HEAD
# CONFIG
=======
# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
file_path = "docs/municipality.xlsx"
output_sql = "inserts_municipalities.sql"

df = pd.read_excel(file_path)
db = SQLGenerator(df)

<<<<<<< HEAD
# normaliza maps
n_map_rgi = normalize_map(map_rgi)
n_map_rgint = normalize_map(map_rgint)
n_map_region = normalize_map(map_region)

# LOOP
for i, row in df.iterrows():

    municipality_id = db.num(row.get("municipalityID"))
    municipality = db.text(row.get("municipality"))

    rgi = safe_map(row.get("rgi"), n_map_rgi)
    rgint = safe_map(row.get("rgint"), n_map_rgint)
    region = safe_map(row.get("locality"), n_map_region)

    # NUMÉRICOS
=======
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
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
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

<<<<<<< HEAD
    # VALIDAÇÃO

    if rgi and rgint:

        sql = f"""
        INSERT INTO municipalities
        (municipalityID, municipality, rgiID, rgintID, regionID, areaKM2, population, man, woman, genderRatio, middleAge, populationDensity, populationProtectedArea, indigenousPopulation, insideIndigenousLand, outsideIndigenousLand, quilombolaPopulation, insideQuilombolaLand, outsideQuilombolaLand, populationByRaceAmarela, populationByRaceBranca, populationByRaceIndigena, populationByRaceParda, populationByRacePreta)
        VALUES ({municipality_id}, {municipality}, {rgi}, {rgint}, {region}, {area}, {population}, {man}, {woman}, {genderRatio}, {averageAge}, {populationDensity}, {populationProtectedArea}, {indigenousPopulation}, {insideIndigenousLand}, {outsideIndigenousLand}, {quilombolaPopulation}, {insideQuilombolaLand}, {outsideQuilombolaLand}, {populationByRaceAmarela}, {populationByRaceBranca}, {populationByRaceIndigena}, {populationByRaceParda}, {populationByRacePreta});
        """

        db.add_insert(sql.strip())

    else:
        db.add_error({
            "linha_excel": i + 2,
            "municipalityID": row.get("municipalityID"),
=======
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
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
            "municipality": row.get("municipality"),
            "rgi": row.get("rgi"),
            "rgint": row.get("rgint")
        })

<<<<<<< HEAD
# Output
db.save_sql(output_sql)
db.report()
=======
# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_municipalities.sql")
db.report()
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
