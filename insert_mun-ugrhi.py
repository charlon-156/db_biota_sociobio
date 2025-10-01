import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_mun

# Carregar a planilha
file_path = "docs/Dados abióticos.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

for i, row in df.iterrows():
    ugrhi_id = int(row["ugrhiID"]) 
    municipalities = str(row["municipality"]).split("//") if pd.notna(row["municipality"]) else []

    for m in municipalities:
        m = m.strip()
        municipality_id = map_mun.get(m, "NULL")

        if municipality_id:
            sql = f"INSERT INTO municipality_ugrhi (municipalityID, ugrhiID) VALUES ({municipality_id}, {ugrhi_id});"
            db.inserts.append(sql)
        else:
            db.erros.append({"linha": i+2, "municipality": m, "ugrhiID": ugrhi_id})

# Salvar e relatar o arquivo SQL
db.save_sql("inserts_mun_ugrhi.sql")
db.report()
