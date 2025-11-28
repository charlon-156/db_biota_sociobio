###############################################################
# Dev.: Charlon F. Monteiro
# project: Banco de Dados Sociobiodiversidade
# file: maps.py
# description: stores the global variables "maps" referring to 
#              the tables to relate to the foreign keys.
# Last update: 2025-11-19
###############################################################


'''
explicação maps.py

Módulo que centraliza dicionários de mapeamento entre valores textuais
provenientes de planilhas Excel e seus respectivos códigos numéricos no banco.

Exemplos: 
- map_tipo: converte nomes de tipos de políticas públicas em IDs.
- map_instituicao: relaciona nomes de instituições com seus IDs.

'''


map_tipo = {
    "Resolução": 1,
    "Decreto": 2,
    "Lei": 3,
    "Portaria": 4,
    "Programa": 5,
    "Relatório": 6,
    "Constituição": 7,
    "Normativa": 8
}

# institutions
map_instituicao = {
    "Secretaria de Infraestrutura e Meio Ambiente": 1,
    "Secretaria do Meio Ambiente": 2,
    "Secretaria do Meio Ambiente, Infraestrutura e Logistica": 3,
    "Secretaria de Agricultura e Abastecimento": 4,
    "Governo do Estado de São Paulo": 5,
    "Assembleia legislativa do Estado de São Paulo": 6,
    "Ministério do Meio Ambiente": 7,
    "Ministério do Meio Ambiente e Mudança do Clima": 8,
    "Ministério da Agricultura": 9,
    "Ministério da Agricultura e Pecuária": 10,
    "Presidência da República - Subchefia para Assuntos Jurídicos": 11,
    "Presidência da República - Casa Civil": 12,
    "Presidência da República - Secretaria-Geral": 13,
    "Câmara dos deputados": 14,
    "Governo Federal do Brasil": 15,
    "Secretaria de estado do Meio Ambiente" : 16,
    "Os Secretários de Estado do Meio Ambiente, de Agricultura e Abastecimento e da Justiça e da Defesa da Cidadania": 17,
    "Agência ambiental do vale do paraiba" : 18,
    "Companhia Ambiental do Estado de São Paulo" : 19,
    "Instituto Chico Mendes de Conservação da Biodiversidade" : 20,
    "Prefeitura Municipal da Estância Balneária de Ubatuba" : 21,
    "Planalto" : 22,
    "Ministério do Meio Ambiente Secretaria de Biodiversidade e Florestas Diretoria de Conservação da Biodiversidade Comissão Nacional de Biodiversidade - CONABIO": 23
}

map_statusLaw = {
    "Vigente": 1,
    "Revogada": 2,
    "Não consta revogação expressa": 3
}

# RGI
map_rgi = {
    "São Paulo": 350001, "Santos": 350002,
    "Sorocaba": 350003, "Itapeva": 350004,
    "Registro": 350005, "Bragança Paulista": 350041,
    "São José dos Campos": 350049, "Taubaté - Pindamonhangaba": 350050,
    "Caraguatatuba - Ubatuba - São Sebastião": 350051, "Guaratinguetá": 350052,
    "Cruzeiro": 350053,
}

# RGINT
map_rgint = {
    "São Paulo": 3501, "Sorocaba": 3502,
    "Campinas": 3510, "São José dos Campos": 3511,
}

# regiões
map_region = {
    "Vale do Ribeira": 1, "Vale do Paraíba": 2,
    "Ribeira de Iguape": 3, "Litoral Norte": 4
}

# municipalities
map_mun = {
    "Apiaí": 3502705, "Barra do Chapéu": 3505351, "Barra do Turvo": 3505401, "Cajati": 3509254,
    "Eldorado": 3514809, "Guapiara": 3517604, "Iporanga": 3521200, "Itaoca": 3522158,
    "Itapirapuã Paulista": 3522653, "Itariri": 3523305, "Jacupiranga": 3524600, "Juquiá": 3526100,
    "Juquitiba": 3526209, "Miracatu": 3529906, "Pariquera-Açu": 3536208, "Pedro de Toledo": 3537206,
    "Registro": 3542602, "Ribeira": 3542800, "Ribeirão Branco": 3543006, "Ribeirão Grande": 3543253,
    "São Lourenço da Serra": 3549953, "Sete Barras": 3551801, "Tapiraí": 3553500, 
    "Aparecida": 3502507, "Arapeí": 3503158, "Areias": 3503505, "Bananal": 3504909, 
    "Caçapava": 3508504, "Cachoeira Paulista": 3508603, "Campos do Jordão": 3509700,
    "Canas": 3509957, "Cruzeiro": 3513405, "Cunha": 3513603, "Guararema": 3518305,
    "Guaratinguetá": 3518404, "Igaratá": 3520202, "Jacareí": 3524402, "Jambeiro": 3524907,
    "Joanópolis": 3525508, "Lagoinha": 3526308, "Lavrinhas": 3526605, "Lorena": 3527207,
    "Monteiro Lobato": 3531704, "Natividade da Serra": 3532306, "Nazaré Paulista": 3532405,
    "Paraibuna": 3535606, "Pindamonhangaba": 3538006, "Piquete": 3538501, "Piracaia": 3538600,
    "Potim": 3540754, "Queluz": 3541901, "Redenção da Serra": 3542305, "Roseira": 3544301,
    "Salesópolis": 3545001, "Santa Branca": 3546009, "Santa Isabel": 3546801,
    "Santo Antônio do Pinhal": 3548203, "São Bento do Sapucaí": 3548609,
    "São José do Barreiro": 3549607, "São José dos Campos": 3549904,
    "São Luiz do Paraitinga": 3550001, "Silveiras": 3552007,"Taubaté": 3554102,
    "Tremembé": 3554805, "Cananéia": 3509908, "Iguape": 3520301,
    "Ilha Comprida": 3520426, "Caraguatatuba": 3510500, "Ilhabela": 3520400,
    "São Sebastião": 3550704, "Ubatuba": 3555406
} 

map_koppen = {
    "Cfb": 1, "Cfa": 2, "Cwb": 3, 
    "Cwa": 4, "Af": 5, "Am": 6, 
    "As": 7, "BSw": 8, "BSh": 9
}

map_lifeForm = {
    "Arbustiva": 1, "Arbórea": 2, "Liana": 3,
    "Volúvel": 4, "Trepadeira": 5, "Herbácea": 6,
    "Subarbustiva": 7, "Palmeira": 8, "Hemiepífitas": 9,
    "Turfo": 10, "Saprófita": 11, "Liana": 12
}

map_substrate = {
    "Terrícola": 1, "Hemiepífita": 2, "Epífita": 3,
    "Rupícola": 4, "Aquática": 5, "Hemiparasita": 6,
    "Saprófita": 7
}

map_biomes = {
    "Caatinga": 1, "Cerrado": 2, "Mata Atlântica": 3,
    "Floresta Amazônica": 4, "Pampa": 5, "Pantanal": 6
}

map_vegetation = {
    "Área Antrópica": 1, "Campo limpo": 2,
    "Cerrado (lato sensu)": 3, "Floresta Ciliar ou Galeria": 4,
    "Floresta Estacional Semidecidual": 5, "Floresta Ombrófila (Floresta Pluvial)": 6,
    "Floresta Ombófila Mista": 7, "Manguezal": 8, "Vegetação de praias (Restinga)": 9,
    "Mata/Vegetação Ciliar ou Galeria": 10, "Floresta Estacional Perenifólia": 11,
    "Campo de Altitude": 12, "Campo de Várzea": 13, "Campo Rupestre": 14,
    "Floresta Estacional Decidual": 15, "Vegetação Sobre Afloramentos Rochosos": 16,
    "Caatinga (stricto sensu)": 17, "Restinga": 18, "Vegetação sobre afloramentos rochosos": 19,
    "Campo Limpo": 20, "Campinarana amazônica": 21, "Floresta de Terra Firme": 22,
    "Área antrópica": 23, "Vegetação aquática": 24, "Compo Rupestre": 25,
    "Vegetação de Carrasco": 26, "Mata/vegetação ciliar ou Galeira": 27,
    "Floresta de Igapó": 28, "Floresta de Várzea": 29,
    "Palmeiral": 30, "Savana amazônica": 31, "Campo de várzea (Várzea)": 32, 
    "Floresta Ombrófila (Tropical Pluvial)": 33, "Floresta Ombrófila Mista": 34
}

map_states = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23, 
    "DF": 53, "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50,
    "MG": 31, "PA": 15, "PB": 25, "PR": 41, "PE": 26, "PI": 22,
    "RJ": 33, "RN": 24, "RS": 43, "RO": 11, "RR": 14, "SC": 42,
    "SP": 35, "SE": 28, "TO": 17
}

map_typesOfUses = {
    "Medicinal": 1, "Madeireiro": 2, "Artesanal": 3, 
    "Alimentício - humano": 4, "Alimentício - animais": 5, 
    "Arborização Urbana": 6, "Ornamental": 7, "Paisagismo": 8, 
    "Higiene": 9, "Combustível": 10, "Recomposição de áreas degradadas": 11, 
    "Reflorestamento": 12, "Aromático": 13
}

map_luminosity = {
    "Heliófita": 1, "Pleno sol ou meia-sombra": 2, "Seletiva Higrófita": 3, 
    "Ciófita": 4, "Esciófita": 5, "Seletiva Xerófita": 6
}