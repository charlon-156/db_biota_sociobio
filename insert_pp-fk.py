import pandas as pd
import unicodedata
from utils.base import SQLGenerator
from utils.maps import map_typology

def normalize_key(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    s = unicodedata.normalize("NFKD", s)
    s = "".join([c for c in s if not unicodedata.combining(c)])
    s = " ".join(s.split()).lower()
    return s


def normalize_map(map_orig):
    new = {}
    for k, v in map_orig.items():
        nk = normalize_key(k)
        if nk:
            new[nk] = v
    return new




n_map_typology = normalize_map(map_typology)

file_path = "docs/public_policies.xlsx"


df = pd.read_excel(file_path)

db = SQLGenerator(df)
seen_inserts = set()


def process_multi(value):
    if pd.isna(value):
        return []
    parts = [p.strip() for p in str(value).split("//") if p.strip() != ""]
    return parts


# =========================
# LOOP PRINCIPAL
# =========================

for i, row in df.iterrows():

    # ID da política pública
    try:
        politica_id = int(row["resourceID"])
    except Exception:
        db.erros.append({
            "linha Excel": i + 2,
            "field": "resourceID",
            "value": row.get("resourceID")
        })
        continue

    parts = process_multi(row.get("Typology"))

    for part in parts:
        raw_value = part
        key = normalize_key(part)

        if key and key in n_map_typology:
            category_id = n_map_typology[key]

            sql = (
                "INSERT INTO pp_typology "
                "(resourceID, typologyID) "
                f"VALUES ({politica_id}, {category_id});"
            )

            if sql not in seen_inserts:
                db.inserts.append(sql)
                seen_inserts.add(sql)

        else:
            db.erros.append({
                "linha Excel": i + 2,
                "resourceID": politica_id,
                "field": "policyCategory",
                "value": raw_value
            })



db.save_sql("inserts_public_policies_fk.sql")

if db.erros:
    pd.DataFrame(db.erros).to_csv(
        "sql/erros_politicas_publicas_policyCategory.csv",
        index=False,
        encoding="utf-8"
    )

print("\n===== RELATÓRIO FINAL =====")
db.report()

if db.erros:
    print("Arquivo de erros salvo em: sql/erros_politicas_publicas_policyCategory.csv")
