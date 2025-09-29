import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_rgi, map_rgint

# Carregar a planilha
file_path = "docs/municipality.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

for i, row in df.iterrows():

    municipalityID = db.num(row.get("municipalityID"))
    municipality = str(row["municipality"]).replace("'", "''") if pd.notna(row["municipality"]) else None
    rgi = map_rgi.get(str(row["rgi"]).strip(), None)
    rgint = map_rgint.get(str(row["rgint"]).strip(), None)  

    area = db.num(row.get("areaKM2"))
    population = db.num(row.get("population"))
    man = db.num(row.get("man"))
    woman = db.num(row.get("woman"))
    genderRatio = db.num(row.get("genderRatio"))
    averageAge = db.num(row.get("averageAge"))
    populationDensity = db.num(row.get("populationDensity"))
    populationProtectedArea = db.num(row.get("populationProtectedArea"))
    indigenousPopulation = db.num(row.get("indigenousPopulation"))
    insideIndigenousLand = db.num(row.get("insideIndigenousLand"))
    outsideIndigenousLand = db.num(row.get("outsideIndigenousLand"))
    quilombolaPopulation = db.num(row.get("quilombolaPopulation"))
    insideQuilombolaLand = db.num(row.get("insideQuilombolaLand"))
    outsideQuilombolaLand = db.num(row.get("outsideQuilombolaLand"))
    populationByRaceAmarela = db.num(row.get("populationByRaceAmarela"))
    populationByRaceBranca = db.num(row.get("populationByRaceBranca"))
    populationByRaceIndigena = db.num(row.get("populationByRaceIndigena"))
    populationByRaceParda = db.num(row.get("populationByRaceParda"))
    populationByRacePreta = db.num(row.get("populationByRacePreta"))

    if municipality and rgi and rgint:
        sql = f"""INSERT INTO municipalities
        (municipalityID, municipality, rgiID, rgintID, areaKM2, population, man, woman, genderRatio, middleAge, populationDensity, populationProtectedArea, indigenousPopulation, insideIndigenousLand, outsideIndigenousLand, quilombolaPopulation, insideQuilombolaLand, outsideQuilombolaLand, populationByRaceAmarela, populationByRaceBranca, populationByRaceIndigena, populationByRaceParda, populationByRacePreta)
        VALUES ({municipalityID}, '{municipality}', {rgi}, {rgint}, {area}, {population}, {man}, {woman}, {genderRatio}, {averageAge}, {populationDensity}, {populationProtectedArea}, {indigenousPopulation}, {insideIndigenousLand}, {outsideIndigenousLand}, {quilombolaPopulation}, {insideQuilombolaLand}, {outsideQuilombolaLand}, {populationByRaceAmarela}, {populationByRaceBranca}, {populationByRaceIndigena}, {populationByRaceParda}, {populationByRacePreta});"""
        db.inserts.append(sql)

    else:
        db.erros.append({
            "linha_excel": i+2,  # +2 por conta do cabeçalho
            "municipalityID": municipalityID,
            "municipality": row["municipality"],
            "rgi": row["rgi"],
            "rgint": row["rgint"]
        })

# Salvar e relatar o arquivo SQL
db.save_sql("inserts_municipalities.sql")
db.report()