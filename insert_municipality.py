import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_rgi, map_rgint, map_region
from utils.helpers import normalize_map, safe_map

# CONFIG
file_path = "docs/municipality.xlsx"
output_sql = "inserts_municipalities.sql"

df = pd.read_excel(file_path)
db = SQLGenerator(df)

# normaliza maps
n_map_rgi = normalize_map(map_rgi)
n_map_rgint = normalize_map(map_rgint)
n_map_region = normalize_map(map_region)

# LOOP
for i, row in df.iterrows():

    municipality_id = db.num(row.get("municipalityID"))
    municipality = db.text(row.get("municipality"))

    rgi = safe_map(row.get("rgi"), n_map_rgi)
    rgint = safe_map(row.get("rgint"), n_map_rgint)
    region = safe_map(row.get("locality"), n_map_region)

    # NUMÉRICOS
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

    # VALIDAÇÃO

    if rgi and rgint:

        sql = f"""
        INSERT INTO municipalities
        (municipalityID, municipality, rgiID, rgintID, regionID, areaKM2, population, man, woman, genderRatio, middleAge, populationDensity, populationProtectedArea, indigenousPopulation, insideIndigenousLand, outsideIndigenousLand, quilombolaPopulation, insideQuilombolaLand, outsideQuilombolaLand, populationByRaceAmarela, populationByRaceBranca, populationByRaceIndigena, populationByRaceParda, populationByRacePreta)
        VALUES ({municipality_id}, {municipality}, {rgi}, {rgint}, {region}, {area}, {population}, {man}, {woman}, {genderRatio}, {averageAge}, {populationDensity}, {populationProtectedArea}, {indigenousPopulation}, {insideIndigenousLand}, {outsideIndigenousLand}, {quilombolaPopulation}, {insideQuilombolaLand}, {outsideQuilombolaLand}, {populationByRaceAmarela}, {populationByRaceBranca}, {populationByRaceIndigena}, {populationByRaceParda}, {populationByRacePreta});
        """

        db.add_insert(sql.strip())

    else:
        db.add_error({
            "linha_excel": i + 2,
            "municipalityID": row.get("municipalityID"),
            "municipality": row.get("municipality"),
            "rgi": row.get("rgi"),
            "rgint": row.get("rgint")
        })

# Output
db.save_sql(output_sql)
db.report()