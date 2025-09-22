import pandas as pd

# Carregar a planilha
file_path = "planilhas/municipality.xlsx"
df = pd.read_excel(file_path)

map_rgi = {
    "São Paulo": 350001,
    "Santos": 350002,
    "Sorocaba": 350003,
    "Itapeva": 350004,
    "Registro": 350005,
    "Bragança Paulista": 350041,
    "São José dos Campos": 350049,
    "Taubaté - Pindamonhangaba": 350050,
    "Caraguatatuba - Ubatuba - São Sebastião": 350051,
    "Guaratinguetá": 350052,
    "Cruzeiro": 350053,
}

map_rgint = {
    "São Paulo": 3501,
    "Soborocaba": 3502,
    "Campinas": 3510,
    "São José dos Campos": 3511,
}

inserts = []
erros = []

for i, row in df.iterrows():
   
    def num(val):
        if pd.isna(val):
            return "NULL"
        if isinstance(val, (int, float)):
            return str(int(val)) if float(val).is_integer() else str(val)
        return str(val)

    municipalityID = num(row.get("municipalityID"))
    municipality = str(row["municipality"]).replace("'", "''") if pd.notna(row["municipality"]) else None
    rgi = map_rgi.get(str(row["rgi"]).strip(), None)
    rgint = map_rgint.get(str(row["rgint"]).strip(), None)  

    area = num(row.get("areaKM2"))
    population = num(row.get("population"))
    man = num(row.get("man"))
    woman = num(row.get("woman"))
    reasonSex = num(row.get("reasonSex"))
    middleAge = num(row.get("middleAge"))

    if municipality and rgi and rgint:
        sql = f"""INSERT INTO municipalities
        (municipalityID, municipality, rgiID, rgintID, areaKM2, population, man, woman, reasonSex, middleAge)
        VALUES ({municipalityID}, '{municipality}', {rgi}, {rgint}, {area}, {population}, {man}, {woman}, {reasonSex}, {middleAge});"""
        inserts.append(sql)
    else:
        erros.append({
            "linha_excel": i+2,  # +2 por conta do cabeçalho
            "municipalityID": municipalityID,
            "municipality": row["municipality"],
            "rgi": row["rgi"],
            "rgint": row["rgint"]
        })

# Salvar em arquivo
with open("sql/inserts_municipalities.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(inserts))

if not erros:
    print("\nTudo certo, patrão ✅🤠👍")
    print("Quantidade de Inserts gerados: ", len(inserts))
else:   
    erros_df = pd.DataFrame(erros)
    print("Algo deu errado, parceiro ❌🙅‍♂️")
    print("⚠️ Total de registros não convertidos: ", len(erros))
    print(erros_df)

