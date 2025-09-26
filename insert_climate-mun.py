import pandas as pd


file_path = "planilhas/Dados abióticos.xlsx"
df = pd.read_excel(file_path, sheet_name="Koppen")

map_koppen = {
    "Cfb": 1,
    "Cfa": 2, 
    "Cwb": 3, 
    "Cwa": 4, 
    "Af": 5, 
    "Am": 6, 
    "As": 7, 
    "BSw": 8,
    "BSh": 9
}


temp_cols = [f"measurementOrFact_T_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]
rain_cols = [f"measurementOrFact_R_{m}" for m in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]]

inserts = []
erros = []

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
            erros.append({"linha": i+2, "municipalityID": municipality_id, "clima": clima})
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
        
        inserts.append(sql)

# Salvar em arquivo
with open("sql/inserts_climate_mun.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(inserts))

# Verificação de erros
if not erros:
    print("Tudo certo, patrão ✅")
    print("Quantidade de Inserts gerados: ", len(inserts))
else:
    erros_df = pd.DataFrame(erros)
    print("⚠️ Climas não encontrados no mapa:")
    print(erros_df)
    erros_df.to_csv("sql/erros_climate_mun.csv", index=False, encoding="utf-8")
