import pandas as pd
from utils.base import SQLGenerator
from utils.maps import (map_lifeForm, map_substrate, map_biomes, map_states, map_typesOfUses, map_vegetation, map_luminosity)
from utils.helpers import normalize_map, process_multi, safe_map

file_path = "docs/dados_biologicos.xlsx"
output_sql = "inserts_species_fk.sql"

df = pd.read_excel(file_path, "Informações sobre as espécies ")
db = SQLGenerator(df)

# normaliza maps
n_map_life = normalize_map(map_lifeForm)
n_map_sub = normalize_map(map_substrate)
n_map_biomes = normalize_map(map_biomes)
n_map_states = normalize_map(map_states)
n_map_types = normalize_map(map_typesOfUses)
n_map_veg = normalize_map(map_vegetation)
n_map_lum = normalize_map(map_luminosity)

seen = set()

for i, row in df.iterrows():

    try:
        species_id = int(row["speciesID"])
    except Exception:
        db.add_error({
            "linha_excel": i + 2,
            "field": "speciesID",
            "value": row.get("speciesID")
        })
        continue

    tasks = [
        ("lifeForm", process_multi(row.get("lifeForm")), n_map_life, "species_lifeForms", "lifeFormID"),
        ("substrate", process_multi(row.get("substrate")), n_map_sub, "species_substrates", "substrateID"),
        ("biome", process_multi(row.get("biome")), n_map_biomes, "species_biomes", "biomeID"),
        ("vegetationType", process_multi(row.get("vegetationType")), n_map_veg, "species_vegetation", "vegetationTypeID"),
        ("locality", process_multi(row.get("locality")), n_map_states, "species_localityStates", "localityStatesID"),
        ("typesOfUses", process_multi(row.get("typesOfUses")), n_map_types, "species_typesOfUses", "typesOfUsesID"),
        ("luminosity", process_multi(row.get("luminosity")), n_map_lum, "species_luminosity", "luminosityID"),
    ]

    for col, parts, nmap, table, target_col in tasks:

        for part in parts:

            target_id = safe_map(part, nmap)

            if target_id:
                sql = f"INSERT INTO {table} (speciesID, {target_col}) VALUES ({species_id}, {target_id});"

                if sql not in seen:
                    db.add_insert(sql)
                    seen.add(sql)

            else:
                db.add_error({
                    "linha_excel": i + 2,
                    "speciesID": species_id,
                    "field": col,
                    "value": part
                })

db.save_sql(output_sql)
db.report()