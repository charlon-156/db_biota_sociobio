import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_lifeForm, map_substrate, map_biomes, map_states, map_typesOfUses, map_luminosity


file_path = "docs/dados_biologicos.xlsx"
df = pd.read_excel(file_path, "espécies")


db = SQLGenerator(df)

# === Loop principal ===
for i, row in df.iterrows():

    species_id = int(row["speciesID"]) 

    # ===== Life Forms =====
    
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

    # ===== Substract =====
    
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

    # ===== Biomes =====
    
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

    # ===== LocalityStates ====== 

    localityStates = str(row["locality"]).split("//") if pd.notna(row["locality"]) else []
    for l in localityStates:
        l = l.strip()
        localityStatesID = map_states.get(l, None)

        if localityStatesID:
            sql_l = f"INSERT INTO species_localityStates VALUES ({species_id}, {localityStatesID});"
            db.inserts.append(sql_l)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "locality": l
            })
            
    # ====== typesOfUses =====
    typesOfUses = str(row["typesOfUses"]).split("//") if pd.notna(row["typesOfUses"]) else []
    for t in typesOfUses:
        t = t.strip()
        typesOfUsesID = map_typesOfUses.get(t, None)
        
        if typesOfUsesID:
            sql_t = f"INSERT INTO species_typesOfUses VALUES ({species_id}, {typesOfUsesID});"
            db.inserts.append(sql_t)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "locality": t
            })
            
    # ===== luminosity =====
    
    luminosity = str(row["luminosity"]).split("//") if pd.notna(row["luminosity"]) else []
    for lu in luminosity:
        lu = t.strip()
        luminosityID = map_luminosity.get(t, None)
        
        if luminosityID:
            sql_lu = f"INSERT INTO species_luminosity VALUES ({species_id}, {luminosityID});"
            db.inserts.append(sql_lu)
        else:
            db.erros.append({
                "linha Excel": i+3,
                "speciesID": species_id,
                "locality": lu
            })

# === Salvar tudo em um único arquivo SQL ===
db.save_sql("inserts_species_fk.sql")

# === Relatar resultados ===
print("\n===== RELATÓRIO FINAL =====")
db.report()
