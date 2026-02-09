###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_species-fk.py
# description: Generates SQL INSERT statements for all
#              species associative (N:N) tables.
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/dados_biologicos.xlsx
   - Aba: Informações sobre as espécies

2. Transformações realizadas:
   - Normalização Unicode
   - Separação de múltiplos valores ("//")
   - Conversão via mapas normalizados

3. Estrutura SQL gerada:
   INSERT INTO species_<relation> (...)

4. Tratamento de erros:
   - speciesID inválido
   - Valor não encontrado no mapa correspondente
"""

import pandas as pd
import unicodedata
from utils.base import SQLGenerator
from utils.maps import (
    map_lifeForm,
    map_substrate,
    map_biomes,
    map_states,
    map_typesOfUses,
    map_vegetation,
    map_luminosity
)

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, sheet_name="Informações sobre as espécies ")

db = SQLGenerator(df)

# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def normalize_key(value):
    # Remove acentos, espaços extras e converte para minúsculo
    if pd.isna(value) or value is None:
        return None
    value = str(value).strip()
    if value == "":
        return None
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = " ".join(value.split()).lower()
    return value


def normalize_map(original_map):
    # Cria versão normalizada do dicionário
    normalized = {}
    for k, v in original_map.items():
        nk = normalize_key(k)
        if nk:
            normalized[nk] = v
    return normalized


def process_multi(value):
    # Processa múltiplos valores separados por "//"
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split("//") if v.strip() != ""]


# ============================================================
# 3. PREPARAÇÃO DOS MAPAS NORMALIZADOS
# ============================================================

n_map_life = normalize_map(map_lifeForm)
n_map_sub = normalize_map(map_substrate)
n_map_biomes = normalize_map(map_biomes)
n_map_states = normalize_map(map_states)
n_map_types = normalize_map(map_typesOfUses)
n_map_veg = normalize_map(map_vegetation)
n_map_lum = normalize_map(map_luminosity)

# Evita duplicidade de inserts
seen_inserts = set()

# ============================================================
# 4. LOOP PRINCIPAL
# ============================================================

for i, row in df.iterrows():

    # ---------- Validação de speciesID ----------
    try:
        species_id = int(row["speciesID"])
    except Exception:
        db.erros.append({
            "linha Excel": i + 2,
            "field": "speciesID",
            "value": row.get("speciesID")
        })
        continue

    # ========================================================
    # ARQUITETURA GENÉRICA DE RELACIONAMENTOS N:N
    # ========================================================
    # Cada item define:
    # (nome_coluna_excel, mapa_normalizado, tabela_destino, nome_coluna_fk)

    tasks = [
        ("lifeForm", n_map_life, "species_lifeForms", "lifeFormID"),
        ("substrate", n_map_sub, "species_substrates", "substrateID"),
        ("biome", n_map_biomes, "species_biomes", "biomeID"),
        ("vegetationType", n_map_veg, "species_vegetation", "vegetationTypeID"),
        ("locality", n_map_states, "species_localityStates", "localityStatesID"),
        ("typesOfUses", n_map_types, "species_typesOfUses", "typeOfUseID"),
        ("luminosity", n_map_lum, "species_luminosity", "luminosityID"),
    ]

    for column_name, normalized_map, table_name, target_column in tasks:

        values = process_multi(row.get(column_name))

        for raw_value in values:

            normalized_key = normalize_key(raw_value)

            if normalized_key and normalized_key in normalized_map:

                target_id = normalized_map[normalized_key]

                sql = f"""INSERT INTO {table_name}
        ({column_name == "locality" and "speciesID, " + target_column or "speciesID, " + target_column})
        VALUES ({species_id}, {target_id});"""

                # Evita duplicidade
                if sql not in seen_inserts:
                    db.inserts.append(sql)
                    seen_inserts.add(sql)

            else:
                db.erros.append({
                    "linha Excel": i + 2,
                    "speciesID": species_id,
                    "field": column_name,
                    "value": raw_value
                })


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_species_fk.sql")

if db.erros:
    pd.DataFrame(db.erros).to_csv(
        "sql/erros_species_fk.csv",
        index=False,
        encoding="utf-8"
    )

print("\n===== RELATÓRIO FINAL =====")
db.report()

if db.erros:
    print("Arquivo de erros salvo em: sql/erros_species_fk.csv")
