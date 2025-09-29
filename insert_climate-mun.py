import pandas as pd
from utils.maps import map_koppen
from utils.base import SQLGenerator

file_path = "docs/Dados abióticos.xlsx"
df = pd.read_excel(file_path, sheet_name="Koppen")

db = SQLGenerator(df)

temp_cols = [f"measurementOrFact_T_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]
rain_cols = [f"measurementOrFact_R_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]

for i, row in df.iterrows():
    municipality_id = int(row["municipalityID"])
    elevation = row["elevation"] if pd.notna(row["elevation"]) else "NULL"
    geometry = str(row["geometry"]).replace("'", "''") if pd.notna(row["geometry"]) else None
    
    # Climas (pode haver mais de um separado por //)
    climates = str(row["dynamicProperties"]).split("//") if pd.notna(row["dynamicProperties"]) else []
    
    for clima in climates:
        clima = clima.strip()
        clima_id = map_koppen.get(clima, None)
        
        if not clima_id:
            db.erros.append({"linha": i+2, "municipalityID": municipality_id, "clima": clima})
            continue
        
        # Médias de temperatura e chuva
        temps = [row[c] if pd.notna(row[c]) else "NULL" for c in temp_cols]
        rains = [row[c] if pd.notna(row[c]) else "NULL" for c in rain_cols]

        sql = f"""INSERT INTO climate_mun
        (municipalityID, koppenID, elevation, {", ".join(temp_cols)}, {", ".join(rain_cols)}, geometry)
        VALUES (
            {municipality_id},
            {clima_id},
            {elevation},
            {", ".join(map(str, temps))},
            {", ".join(map(str, rains))},
            '{geometry}'
        );"""
        
        db.inserts.append(sql)

# Salvar e relatar o arquivo SQL
db.save_sql("inserts_climate_mun.sql")
db.report()