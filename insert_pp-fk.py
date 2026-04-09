import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_typology
from utils.helpers import normalize_map, process_multi, safe_map

file_path = "docs/public_policies.xlsx"
output_sql = "inserts_public_policies_fk.sql"

df = pd.read_excel(file_path)
db = SQLGenerator(df)

n_map_typology = normalize_map(map_typology)

seen = set()

for i, row in df.iterrows():

    try:
        resource_id = int(row["resourceID"])
    except Exception:
        db.add_error({
            "linha_excel": i + 2,
            "field": "resourceID",
            "value": row.get("resourceID")
        })
        continue

    parts = process_multi(row.get("Typology"))

    for part in parts:

        typology_id = safe_map(part, n_map_typology)

        if typology_id:
            sql = f"INSERT INTO pp_typology (resourceID, typologyID) VALUES ({resource_id}, {typology_id});"

            if sql not in seen:
                db.add_insert(sql)
                seen.add(sql)

        else:
            db.add_error({
                "linha_excel": i + 2,
                "resourceID": resource_id,
                "field": "Typology",
                "value": part
            })

db.save_sql(output_sql)
db.report()