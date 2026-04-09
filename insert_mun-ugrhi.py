###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_mun-ugrhi.py
# description: Generates SQL INSERT statements for the
#              municipality_ugrhi associative table.
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/Dados abióticos.xlsx

2. Transformações realizadas:
   - Separação de múltiplos municípios (//)
   - Conversão de nomes para municipalityID via map_mun

3. Estrutura SQL gerada:
   INSERT INTO municipality_ugrhi (...)

4. Tratamento de erros:
   - Município não encontrado no map
   - ugrhiID inválido
"""

import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_mun

<<<<<<< HEAD
# CONFIG
=======
# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
file_path = "docs/Dados abióticos.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

# ============================================================
# 2. FUNÇÕES AUXILIARES
# ============================================================

def process_multi(value):
    # Processa células com múltiplos municípios separados por "//"
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split("//") if v.strip() != ""]


# ============================================================
# 3. LOOP PRINCIPAL
# ============================================================

for i, row in df.iterrows():

    # ---------- Validação de ugrhiID ----------
    try:
        ugrhi_id = int(row["ugrhiID"])
    except Exception:
        db.erros.append({
            "linha Excel": i + 2,
            "field": "ugrhiID",
            "value": row.get("ugrhiID")
        })
        continue

    # ---------- Processamento de múltiplos municípios ----------
    municipalities = process_multi(row.get("municipality"))

    # ========================================================
    # 4. GERAÇÃO DOS INSERTS (RELAÇÃO N:N)
    # ========================================================
    # Para cada município listado na célula:
    # - Converte o nome para municipalityID via map_mun
    # - Gera um INSERT na tabela associativa

    for m in municipalities:

        municipality_id = map_mun.get(m)

        if municipality_id:

<<<<<<< HEAD
# Output
=======
            sql = f"""INSERT INTO municipality_ugrhi (municipalityID, ugrhiID) VALUES ({municipality_id}, {ugrhi_id});"""

            db.inserts.append(sql)

        else:
            # Município não encontrado no mapa
            db.erros.append({
                "linha Excel": i + 2,
                "municipality": m,
                "ugrhiID": ugrhi_id
            })


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

>>>>>>> 33a7c0884b46783ebcae0ad18839b4c2fbb57b63
db.save_sql("inserts_mun_ugrhi.sql")
db.report()
