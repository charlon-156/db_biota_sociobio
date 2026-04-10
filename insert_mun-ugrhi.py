import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_mun
from utils.helpers import normalize_map, process_multi, safe_map

# CONFIG
file_path = "docs/Dados abióticos.xlsx"
output_sql = "inserts_mun_ugrhi.sql"

df = pd.read_excel(file_path)
db = SQLGenerator(df)

n_map_mun = normalize_map(map_mun)
seen = set()

# LOOP
for i, row in df.iterrows():

    ugrhi_id = db.num(row.get("ugrhiID"))

    municipalities = process_multi(row.get("municipality"))

    if not municipalities:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "Nenhum município informado",
            "ugrhiID": row.get("ugrhiID")
        })
        continue

    for m in municipalities:

        municipality_id = safe_map(m, n_map_mun)

        if municipality_id:

            key = (municipality_id, ugrhi_id)

            if key not in seen:

                sql = f"""
                INSERT INTO municipality_ugrhi (municipalityID, ugrhiID) VALUES ({municipality_id}, {ugrhi_id});
                """

                db.add_insert(sql.strip())
                seen.add(key)

        else:
            db.add_error({
                "linha_excel": i + 2,
                "municipality": m,
                "ugrhiID": row.get("ugrhiID")
            })

# Output
db.save_sql(output_sql)
db.report()