import pandas as pd
from utils.base import SQLGenerator
from utils.maps import map_tipo, map_instituicao, map_statusLaw

# Carregar a planilha
file_path = "docs/public_policies.xlsx"
df = pd.read_excel(file_path)

db = SQLGenerator(df)

for i, row in df.iterrows():
    title = str(row["title"]).replace("'", "''") if pd.notna(row["title"]) else  'NULL'
    description = str(row["description"]).replace("'", "''") if pd.notna(row["description"]) else  'NULL'
    fonte = str(row[" bibliographicCitation"]).replace("'", "''") if pd.notna(row[" bibliographicCitation"]) else  'NULL'
    site = str(row["referencesURL"]).replace("'", "''") if pd.notna(row["referencesURL"]) else  'NULL'
    
    tipo = map_tipo.get(str(row["type"]).strip(),  'NULL')
    instituicao = map_instituicao.get(str(row["institution"]).strip(),  'NULL')
    status = map_statusLaw.get(str(row["LegislativeStatus"]).strip(), 'NULL')
    
    if tipo != 'NULL' and instituicao != 'NULL' and status != 'NULL':
        sql = f"""INSERT INTO public_policies 
        (title, description, bibliographicCitation, references_url, typeID, institutionID, LegislativeStatusID)
        VALUES ('{title}', '{description}', '{fonte}', '{site}', {tipo}, {instituicao}, {status});"""
        db.inserts.append(sql)
    else:
        db.erros.append({
            "linha": i+2,  # +2 porque Excel tem cabeçalho
            "tipo": row["type"],
            "instituicao": row["institution"]
        })

# Salvar e relatar o arquivo SQL
db.save_sql("inserts_public_policies.sql")
db.report()