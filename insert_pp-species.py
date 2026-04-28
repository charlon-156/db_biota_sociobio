import pandas as pd
from utils.base import SQLGenerator
from utils.helpers import normalize_key

file_bio = "docs/dados_biologicos.xlsx"
file_pp = "docs/public_policies.xlsx"
sheet_conn = "Conexão com Políticas Públicas"
sheet_species = "Informações sobre as espécies "
output_sql = "inserts_public_policies_species.sql"

df_conn = pd.read_excel(file_bio, sheet_name=sheet_conn)
df_pp = pd.read_excel(file_pp)
df_sp = pd.read_excel(file_bio, sheet_name=sheet_species)

db = SQLGenerator(df_conn)

# mapa políticas
map_pp = {
    normalize_key(r["title"]): int(r["resourceID"])
    for _, r in df_pp.iterrows()
    if pd.notna(r["title"]) and pd.notna(r["resourceID"])
}

seen = set()

for i, row in df_conn.iterrows():
    title = normalize_key(row["title"])
    species_col = row["speciesInformationColumn"]
    link_value = row["biologicalLink"]

    if title not in map_pp:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "Título não encontrado",
            "title": row["title"]
        })
        continue

    resource_id = map_pp[title]

    # caso ALL
    if str(species_col).strip().lower() == "all":

        all_species = df_sp["speciesID"].dropna().astype(int)

        for sid in all_species:
            key = (resource_id, sid)

            if key not in seen:
                db.add_insert(
                    f"INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resource_id}, {sid});"
                )
                seen.add(key)

        continue

    if str(species_col).strip() == "threatenedStatusIUCN":

        IUCN_TARGET = {"ew", "cr", "en", "vu"}

        matches = []

        for _, sp_row in df_sp.iterrows():

            cell = sp_row["threatenedStatusIUCN"]

            if pd.isna(cell):
                continue

            values = [normalize_key(v) for v in str(cell).split("//")]

            # se QUALQUER categoria bater
            if any(v in IUCN_TARGET for v in values):
                matches.append(int(sp_row["speciesID"]))

        if not matches:
            db.add_error({
                "linha_excel": i + 2,
                "erro": "Nenhuma espécie ameaçada encontrada",
                "column": "threatenedStatusIUCN"
            })
            continue

        for sid in matches:
            key = (resource_id, sid)

            if key not in seen:
                db.add_insert(
                    f"INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resource_id}, {sid});"
                )
                seen.add(key)

        continue

    # valida coluna
    if species_col not in df_sp.columns:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "Coluna inexistente",
            "column": species_col
        })
        continue

    target = normalize_key(link_value)

    matches = []

    for _, sp_row in df_sp.iterrows():

        cell = sp_row[species_col]

        if pd.isna(cell):
            continue

        values = [normalize_key(v) for v in str(cell).split("//")]

        if target in values:
            matches.append(int(sp_row["speciesID"]))

    if not matches:
        db.add_error({
            "linha_excel": i + 2,
            "erro": "Nenhuma espécie correspondeu",
            "column": species_col,
            "value": link_value
        })
        continue

    for sid in matches:
        key = (resource_id, sid)

        if key not in seen:
            db.add_insert(
                f"INSERT INTO public_policies_species (resourceID, speciesID) VALUES ({resource_id}, {sid});"
            )
            seen.add(key)

# Output
db.save_sql(output_sql)
db.report()