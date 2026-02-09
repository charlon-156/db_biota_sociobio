###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_pp-species.py
# description: Generates SQL INSERT statements for the
#              public_policies_species associative table.
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/dados_biologicos.xlsx
   - Aba: Conexão com Políticas Públicas
   - Planilha: docs/public_policies.xlsx

2. Transformações realizadas:
   - Normalização de texto para comparação
   - Match dinâmico baseado na coluna indicada
   - Regra especial "all" (aplica a todas as espécies)

3. Estrutura SQL gerada:
   INSERT INTO public_policies_species (...)

4. Tratamento de erros:
   - Título de política não encontrado
   - Coluna inexistente
   - Nenhuma espécie correspondente
"""

import pandas as pd
import unicodedata
from utils.base import SQLGenerator

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

file_bio = "docs/dados_biologicos.xlsx"
file_pp = "docs/public_policies.xlsx"

sheet_conn = "Conexão com Políticas Públicas"
sheet_species = "Informações sobre as espécies "

df_conn = pd.read_excel(file_bio, sheet_name=sheet_conn)
df_pp = pd.read_excel(file_pp)
df_sp = pd.read_excel(file_bio, sheet_name=sheet_species)

db = SQLGenerator(df_conn)

# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def normalize(value):
    # Remove acentos, espaços extras e converte para minúsculo
    if pd.isna(value) or value is None:
        return None
    value = str(value).strip()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return value.lower()


# ============================================================
# 3. PREPARAÇÃO DO MAPA DE POLÍTICAS
# ============================================================

map_pp = {
    normalize(r["title"]): int(r["resourceID"])
    for _, r in df_pp.iterrows()
    if pd.notna(r["title"]) and pd.notna(r["resourceID"])
}

# ============================================================
# 4. LOOP PRINCIPAL
# ============================================================

for i, row in df_conn.iterrows():

    title_norm = normalize(row.get("title"))
    species_column = row.get("speciesInformationColumn")
    link_value = row.get("biologicalLink")

    # ---------- Validação do título ----------
    if title_norm not in map_pp:
        db.erros.append({
            "linha Excel": i + 2,
            "erro": "Título não encontrado",
            "title": row.get("title")
        })
        continue

    resource_id = map_pp[title_norm]

    # ========================================================
    # REGRA ESPECIAL: "all"
    # ========================================================
    # Se speciesInformationColumn == "all",
    # associa a política a TODAS as espécies

    if str(species_column).strip().lower() == "all":

        all_species = df_sp["speciesID"].dropna().astype(int).tolist()

        for species_id in all_species:

            sql = f"""INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resource_id}, {species_id});"""

            db.inserts.append(sql)

        continue

    # ---------- Validação da coluna ----------
    if species_column not in df_sp.columns:
        db.erros.append({
            "linha Excel": i + 2,
            "erro": "Coluna inexistente",
            "column": species_column
        })
        continue

    # ---------- Busca de correspondências ----------
    target_norm = normalize(link_value)
    matches = []

    for _, sp_row in df_sp.iterrows():

        cell = sp_row[species_column]

        if pd.isna(cell):
            continue

        options = [normalize(x) for x in str(cell).split("//")]

        if target_norm in options:
            matches.append(int(sp_row["speciesID"]))

    # ---------- Nenhuma correspondência ----------
    if not matches:
        db.erros.append({
            "linha Excel": i + 2,
            "erro": "Nenhuma espécie correspondeu",
            "column": species_column,
            "value": link_value
        })
        continue

    # ---------- Geração dos INSERTs ----------
    for species_id in matches:

        sql = f"""INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resource_id}, {species_id});"""

        db.inserts.append(sql)


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_public_policies_species.sql")
db.report()
