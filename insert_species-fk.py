import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_lifeForm, map_substrate, map_biomes


file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, "espécies")


db = SQLGenerator(df)

# === Loop principal ===
for i, row in df.iterrows():

    species_id = int(row["speciesID"]) 

    # ===== LIFE FORMS =====
    lifeforms = str(row["lifeForm"]).split("//") if pd.notna(row["lifeForm"]) else []
    for lf in lifeforms:
        lf = lf.strip()
        lf_id = map_lifeForm.get(lf, None)

        if lf_id:
            sql_lf = f"INSERT INTO species_lifeForms (speciesID, lifeFormID) VALUES ({species_id}, {lf_id});"
            db.inserts.append(sql_lf)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "lifeForm": lf
            })

    # ===== SUBSTRATES =====
    substrates = str(row["substrate"]).split("//") if pd.notna(row["substrate"]) else []
    for s in substrates:
        s = s.strip()
        s_id = map_substrate.get(s, None)

        if s_id:
            sql_sub = f"INSERT INTO species_substrates (speciesID, substrateID) VALUES ({species_id}, {s_id});"
            db.inserts.append(sql_sub)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "substrate": s
            })

    # ===== BIOMES =====
    biomes = str(row["biome"]).split("//") if pd.notna(row["biome"]) else []
    for b in biomes:
        b = b.strip()
        biome_id = map_biomes.get(b, None)

        if biome_id:
            sql_b = f"INSERT INTO species_biomes (speciesID, biomeID) VALUES ({species_id}, {biome_id});"
            db.inserts.append(sql_b)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "biome": b
            })

# === Salvar tudo em um único arquivo SQL ===
db.save_sql("inserts_species_fk.sql")

# === Relatar resultados ===
print("\n===== RELATÓRIO FINAL =====")
db.report()
