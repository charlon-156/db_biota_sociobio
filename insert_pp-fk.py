###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_pp-fk.py
# description: Generates SQL INSERT statements for the
#              pp_typology associative table.
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/public_policies.xlsx

2. Transformações realizadas:
   - Normalização Unicode (remoção de acentos)
   - Conversão para minúsculas
   - Separação de múltiplos valores ("//")

3. Estrutura SQL gerada:
   INSERT INTO pp_typology (...)

4. Tratamento de erros:
   - resourceID inválido
   - tipologia não encontrada no mapa
"""

import pandas as pd
import unicodedata
from utils.base import SQLGenerator
from utils.maps import map_typology

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

file_path = "docs/public_policies.xlsx"
df = pd.read_excel(file_path)

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
    # Processa células com múltiplos valores separados por "//"
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split("//") if v.strip() != ""]


# ============================================================
# 3. PREPARAÇÃO DOS MAPAS NORMALIZADOS
# ============================================================

n_map_typology = normalize_map(map_typology)

# Evita inserts duplicados
seen_inserts = set()

# ============================================================
# 4. LOOP PRINCIPAL
# ============================================================

for i, row in df.iterrows():

    # ---------- Validação de resourceID ----------
    try:
        resource_id = int(row["resourceID"])
    except Exception:
        db.erros.append({
            "linha Excel": i + 2,
            "field": "resourceID",
            "value": row.get("resourceID")
        })
        continue

    # ---------- Processamento de múltiplas tipologias ----------
    typologies = process_multi(row.get("Typology"))

    for typ in typologies:

        normalized_key = normalize_key(typ)

        if normalized_key and normalized_key in n_map_typology:

            typology_id = n_map_typology[normalized_key]

            sql = f"""INSERT INTO pp_typology (resourceID, typologyID) VALUES ({resource_id}, {typology_id});"""

            # Evita duplicidade
            if sql not in seen_inserts:
                db.inserts.append(sql)
                seen_inserts.add(sql)

        else:
            # Tipologia não encontrada no mapa
            db.erros.append({
                "linha Excel": i + 2,
                "resourceID": resource_id,
                "field": "Typology",
                "value": typ
            })


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_public_policies_fk.sql")

# Salva CSV detalhado de erros
if db.erros:
    pd.DataFrame(db.erros).to_csv(
        "sql/erros_politicas_publicas_typology.csv",
        index=False,
        encoding="utf-8"
    )

print("\n===== RELATÓRIO FINAL =====")
db.report()

if db.erros:
    print("Arquivo de erros salvo em: sql/erros_politicas_publicas_typology.csv")
