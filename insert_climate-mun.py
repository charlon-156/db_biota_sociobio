import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_koppen
from utils.helpers import process_multi, normalize_map, safe_map

# CONFIG
file_path = "docs/Dados abióticos.xlsx"
output_sql = "inserts_climate_mun.sql"

df = pd.read_excel(file_path, sheet_name="Koppen")
db = SQLGenerator(df)

n_map_koppen = normalize_map(map_koppen)

temp_cols = [f"measurementOrFact_T_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]
rain_cols = [f"measurementOrFact_R_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]

# LOOP
for i, row in df.iterrows():

    municipality_id = db.num(row.get("municipalityID"))
    elevation = db.num(row.get("elevation"))
    geometry = db.text(row.get("geometry"))

    climates = process_multi(row.get("dynamicProperties"))

    for clima in climates:

        clima_id = safe_map(clima, n_map_koppen)

        if not clima_id:
            db.add_error({
                "linha_excel": i + 2,
                "municipalityID": row.get("municipalityID"),
                "clima": clima
            })
            continue

        # TEMPERATURA E CHUVA

        temps = [db.num(row.get(c)) for c in temp_cols]
        rains = [db.num(row.get(c)) for c in rain_cols]

        sql = f"""
        INSERT INTO climate_mun
        (municipalityID, koppenID, elevation, {", ".join(temp_cols)}, {", ".join(rain_cols)}, geometry)
        VALUES (
            {municipality_id},
            {clima_id},
            {elevation},
            {", ".join(temps)},
            {", ".join(rains)},
            {geometry}
        );
        """

        db.add_insert(sql.strip())

# Output
db.save_sql(output_sql)
db.report()