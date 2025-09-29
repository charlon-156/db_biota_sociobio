import pandas as pd

# Carregar a planilha
file_path = "docs/Dados abióticos.xlsx"
df = pd.read_excel(file_path)

map_mun = {
    "Apiaí": 3502705,
    "Barra do Chapéu": 3505351,
    "Barra do Turvo": 3505401,
    "Cajati": 3509254,
    "Eldorado": 3514809,
    "Guapiara": 3517604,
    "Iporanga": 3521200,
    "Itaoca": 3522158,
    "Itapirapuã Paulista": 3522653,
    "Itariri": 3523305,
    "Jacupiranga": 3524600,
    "Juquiá": 3526100,
    "Juquitiba": 3526209,
    "Miracatu": 3529906,
    "Pariquera-Açu": 3536208,
    "Pedro de Toledo": 3537206,
    "Registro": 3542602,
    "Ribeira": 3542800,
    "Ribeirão Branco": 3543006,
    "Ribeirão Grande": 3543253,
    "São Lourenço da Serra": 3549953,
    "Sete Barras": 3551801,
    "Tapiraí": 3553500,
    "Aparecida": 3502507,
    "Arapeí": 3503158,
    "Areias": 3503505,
    "Bananal": 3504909,
    "Caçapava": 3508504,
    "Cachoeira Paulista": 3508603,
    "Campos do Jordão": 3509700,
    "Canas": 3509957,
    "Cruzeiro": 3513405,
    "Cunha": 3513603,
    "Guararema": 3518305,
    "Guaratinguetá": 3518404,
    "Igaratá": 3520202,
    "Jacareí": 3524402,
    "Jambeiro": 3524907,
    "Joanópolis": 3525508,
    "Lagoinha": 3526308,
    "Lavrinhas": 3526605,
    "Lorena": 3527207,
    "Monteiro Lobato": 3531704,
    "Natividade da Serra": 3532306,
    "Nazaré Paulista": 3532405,
    "Paraibuna": 3535606,
    "Pindamonhangaba": 3538006,
    "Piquete": 3538501,
    "Piracaia": 3538600,
    "Potim": 3540754,
    "Queluz": 3541901,
    "Redenção da Serra": 3542305,
    "Roseira": 3544301,
    "Salesópolis": 3545001,
    "Santa Branca": 3546009,
    "Santa Isabel": 3546801,
    "Santo Antônio do Pinhal": 3548203,
    "São Bento do Sapucaí": 3548609,
    "São José do Barreiro": 3549607,
    "São José dos Campos": 3549904,
    "São Luiz do Paraitinga": 3550001,
    "Silveiras": 3552007,
    "Taubaté": 3554102,
    "Tremembé": 3554805,
    "Cananéia": 3509908,
    "Iguape": 3520301,
    "Ilha Comprida": 3520426,
    "Caraguatatuba": 3510500,
    "Ilhabela": 3520400,
    "São Sebastião": 3550704,
    "Ubatuba": 3555406
}

inserts = []
erros = []

for i, row in df.iterrows():
    ugrhi_id = int(row["ugrhiID"])  # supondo que existe essa coluna
    municipalities = str(row["municipality"]).split("//") if pd.notna(row["municipality"]) else []

    for m in municipalities:
        m = m.strip()
        municipality_id = map_mun.get(m, None)

        if municipality_id:
            sql = f"INSERT INTO municipality_ugrhi (municipalityID, ugrhiID) VALUES ({municipality_id}, {ugrhi_id});"
            inserts.append(sql)
        else:
            erros.append({"linha": i+2, "municipality": m, "ugrhiID": ugrhi_id})


with open("sql/inserts_mun_ugrhi.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(inserts))

# Verificação
if not erros:
    print("Tudo certo, patrão ✅")
    print("Quantidade de Inserts gerados: ", len(inserts))
else:
    erros_df = pd.DataFrame(erros)
    print("⚠️ Municípios não encontrados no mapa:")
    print(erros_df)
    erros_df.to_csv("sql/erros_municipality_ugrhi.csv", index=False, encoding="utf-8")
