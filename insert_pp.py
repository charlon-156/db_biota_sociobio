###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: insert_pp.py
# description: Generates SQL INSERT statements for the
#              public_policies table based on public_policies.xlsx
# Last update: 2026-02-09
###############################################################

"""
Descrição detalhada:

1. Origem dos dados:
   - Planilha: docs/public_policies.xlsx

2. Transformações realizadas:
   - Escape de campos textuais longos
   - Mapeamento de tipo, instituição e status legislativo

3. Validações:
   - typeID existente no map
   - institutionID existente no map
   - LegislativeStatusID existente no map

4. Estrutura SQL gerada:
   INSERT INTO public_policies (...)

5. Tratamento de erros:
   - Foreign keys não encontradas nos mapas
"""

import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_tipo, map_instituicao, map_statusLaw

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

file_path = "docs/public_policies.xlsx"
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

    # ---------- Campos textuais ----------
    title_raw = escape_text(row.get("title"))
    description_raw = escape_text(row.get("description"))
    fonte_raw = escape_text(row.get(" bibliographicCitation"))
    site_raw = escape_text(row.get("referencesURL"))
    just_raw = escape_text(row.get("Justification"))

    title = f"'{title_raw}'" if title_raw else "NULL"
    description = f"'{description_raw}'" if description_raw else "NULL"
    fonte = f"'{fonte_raw}'" if fonte_raw else "NULL"
    site = f"'{site_raw}'" if site_raw else "NULL"
    just = f"'{just_raw}'" if just_raw else "NULL"

    # ---------- Mapeamento de foreign keys ----------
    tipo = map_tipo.get(str(row.get("type")).strip())
    instituicao = map_instituicao.get(str(row.get("institution")).strip())
    status = map_statusLaw.get(str(row.get("LegislativeStatus")).strip())

    # ========================================================
    # 4. VALIDAÇÃO DE INTEGRIDADE REFERENCIAL
    # ========================================================
    # Só gera INSERT se todas as foreign keys existirem.
    # Isso evita erro de FK no banco.

    if tipo and instituicao and status:

        sql = f"""INSERT INTO public_policies
        (title, description, bibliographicCitation, references_url, justification, typeID, institutionID, LegislativeStatusID)
        VALUES ({title}, {description}, {fonte}, {site}, {just}, {tipo}, {instituicao}, {status});"""

        db.inserts.append(sql)

    else:
        # Registra erro para auditoria
        db.erros.append({
            "linha Excel": i + 2,
            "title": row.get("title"),
            "type": row.get("type"),
            "institution": row.get("institution"),
            "LegislativeStatus": row.get("LegislativeStatus")
        })


# ============================================================
# 5. SAÍDA E RELATÓRIO
# ============================================================

db.save_sql("inserts_public_policies.sql")
db.report()
