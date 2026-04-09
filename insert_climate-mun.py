###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_climate-mun.py
# description: Generates SQL INSERT statements for the
#              climate_mun table based on abiotic Excel data.
# Last update: 2026-02-09
###############################################################

"""
1. Origem dos dados:
   - Planilha: docs/Dados abióticos.xlsx
   - Aba: Koppen

2. Transformações realizadas:
   - Geração dinâmica das colunas mensais de temperatura e chuva
   - Separação de múltiplos climas (//)
   - Conversão segura de valores numéricos
   - Escape de campos textuais

3. Estrutura SQL gerada:
   INSERT INTO climate_mun VALUES (...)

4. Tratamento de erros:
   - Climas não encontrados no map_koppen
   - municipalityID inválido
"""

import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_koppen
from utils.helpers import process_multi, normalize_map, safe_map

<<<<<<< HEAD
# CONFIG
=======
# ============================================================
# 1. CARREGAMENTO DOS DADOS 
# ============================================================

>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
file_path = "docs/Dados abióticos.xlsx"
output_sql = "inserts_climate_mun.sql"

df = pd.read_excel(file_path, sheet_name="Koppen")
db = SQLGenerator(df)

<<<<<<< HEAD
n_map_koppen = normalize_map(map_koppen)

temp_cols = [f"measurementOrFact_T_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]
rain_cols = [f"measurementOrFact_R_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]
=======
# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def process_multi(value):
    
    # Processa células com múltiplos valores separados por "//".
    # Retorna lista limpa de valores.
   
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split("//") if v.strip() != ""]


def escape_text(value):
    
    #Escapa aspas simples para evitar erro de sintaxe SQL.
    
    if pd.isna(value):
        return None
    return str(value).replace("'", "''")


# ============================================================
# 3. GERAÇÃO DINÂMICA DAS COLUNAS MENSAIS
# ============================================================

months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

temp_cols = [f"measurementOrFact_T_{m}" for m in months]
rain_cols = [f"measurementOrFact_R_{m}" for m in months]

# ============================================================
# 4. LOOP PRINCIPAL
# ============================================================
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63

# LOOP
for i, row in df.iterrows():

<<<<<<< HEAD
    municipality_id = db.num(row.get("municipalityID"))
    elevation = db.num(row.get("elevation"))
    geometry = db.text(row.get("geometry"))

=======
    # ---------- ID do município ----------
    try:
        municipality_id = int(row["municipalityID"])
    except Exception:
        db.erros.append({
            "linha Excel": i + 2,
            "field": "municipalityID",
            "value": row.get("municipalityID")
        })
        continue

    # ---------- Campos opcionais ----------
    elevation = db.num(row.get("elevation"))

    geometry_raw = escape_text(row.get("geometry"))
    geometry = f"'{geometry_raw}'" if geometry_raw else "NULL"

    # ---------- Processamento de múltiplos climas ----------
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
    climates = process_multi(row.get("dynamicProperties"))

    for clima in climates:

<<<<<<< HEAD
        clima_id = safe_map(clima, n_map_koppen)

        if not clima_id:
            db.add_error({
                "linha_excel": i + 2,
                "municipalityID": row.get("municipalityID"),
=======
        koppen_id = map_koppen.get(clima)

        if not koppen_id:
            db.erros.append({
                "linha Excel": i + 2,
                "municipalityID": municipality_id,
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
                "clima": clima
            })
            continue

<<<<<<< HEAD
        # TEMPERATURA E CHUVA

        temps = [db.num(row.get(c)) for c in temp_cols]
        rains = [db.num(row.get(c)) for c in rain_cols]

        sql = f"""
        INSERT INTO climate_mun
        (municipalityID, koppenID, elevation, {", ".join(temp_cols)}, {", ".join(rain_cols)}, geometry)
=======
        # ---------- Médias mensais ----------
        temps = [db.num(row.get(c)) for c in temp_cols]
        rains = [db.num(row.get(c)) for c in rain_cols]

        # ---------- Montagem do SQL ----------
        sql = f"""
        INSERT INTO climate_mun
        (municipalityID, koppenID, elevation,
         {", ".join(temp_cols)},
         {", ".join(rain_cols)},
         geometry)
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
        VALUES (
            {municipality_id},
            {koppen_id},
            {elevation},
            {", ".join(temps)},
            {", ".join(rains)},
            {geometry}
        );
        """
<<<<<<< HEAD

        db.add_insert(sql.strip())

# Output
db.save_sql(output_sql)
db.report()
=======

        db.inserts.append(sql.strip())

# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_climate_mun.sql")
db.report()
>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
