import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_tipo, map_instituicao, map_statusLaw
from utils.helpers import normalize_map, safe_map

# CONFIG
file_path = "docs/public_policies.xlsx"
output_sql = "inserts_public_policies.sql"

df = pd.read_excel(file_path)
db = SQLGenerator(df)

# normaliza maps
n_map_tipo = normalize_map(map_tipo)
n_map_instituicao = normalize_map(map_instituicao)
n_map_status = normalize_map(map_statusLaw)

# LOOP
for i, row in df.iterrows():

    title = db.text(row.get("title"))
    description = db.text(row.get("description"))
    fonte = db.text(row.get("bibliographicCitation"))
    site = db.text(row.get("referencesURL"))
    justification = db.text(row.get("Justification"))

    tipo = safe_map(row.get("type"), n_map_tipo)
    instituicao = safe_map(row.get("institution"), n_map_instituicao)
    status = safe_map(row.get("LegislativeStatus"), n_map_status)

    if tipo and instituicao and status:

        sql = f"""
        INSERT INTO public_policies 
        (title, description, bibliographicCitation, references_url, justification, typeID, institutionID, LegislativeStatusID)
        VALUES ({title}, {description}, {fonte}, {site}, {justification}, {tipo}, {instituicao}, {status});
        """

        db.add_insert(sql.strip())

    else:
        db.add_error({
            "linha_excel": i + 2,
            "title": row.get("title"),
            "type": row.get("type"),
            "institution": row.get("institution"),
            "status": row.get("LegislativeStatus")
        })

# OUTPUT
db.save_sql(output_sql)
db.report()