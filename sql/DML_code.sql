USE biota_sociobiodiversidade;

INSERT INTO type_pp (type) VALUES
('Resolução'),
('Decreto'),
('Lei'),
('Portaria'),
('Programa'),
('Relatório'),
('Constituição');

INSERT INTO institutions (institution) VALUES
('Secretaria de Infraestrutura e Meio Ambiente'),
('Secretaria do Meio Ambiente'),
('Secretaria do Meio Ambiente, Infraestrutura e Logistica'),
('Secretaria de Agricultura e Abastecimento'),
('Governo do Estado de São Paulo'),
('Assembleia legislativa do Estado de São Paulo'),
('Ministério do Meio Ambiente'),
('Ministério do Meio Ambiente e Mudança do Clima'),
('Ministério da Agricultura'),
('Ministério da Agricultura e Pecuária'),
('Presidência da República - Subchefia para Assuntos Jurídicos'),
('Presidência da República - Casa Civil'),
('Presidência da República - Secretaria-Geral'),
('Câmara dos deputados'),
('Governo Federal do Brasil'),
('Secretaria de estado do Meio Ambiente'),
('Os Secretários de Estado do Meio Ambiente, de Agricultura e Abastecimento e da Justiça e da Defesa da Cidadania'),
('Agência ambiental do vale do paraiba'),
('Companhia Ambiental do Estado de São Paulo'),
('Instituto Chico Mendes de Conservação da Biodiversidade'),
('Prefeitura Municipal da Estância Balneária de Ubatuba'),
('Planalto');

INSERT INTO RGI (rgiID, rgi) VALUES
(350001, 'São Paulo'),
(350002, 'Santos'),
(350003, 'Sorocaba'),
(350004, 'Itapeva'),
(350005, 'Registro'),
(350041, 'Bragança Paulista'),
(350049, 'São José dos Campos'),
(350050, 'Taubaté - Pindamonhangaba'),
(350051, 'Caraguatatuba - Ubatuba - São Sebastião'),
(350052, 'Guaratinguetá'),
(350053, 'Cruzeiro');

INSERT INTO RGINT (rgintID, rgint) VALUES
(3501, 'São Paulo'),
(3502, 'Itapeva'),
(3510,'Campinas'),
(3511, 'São José dos Campos');

INSERT INTO ugrhis (ugrhiID, ugrhi, geometry) VALUES
(1, 'Mantiqueira', ''),
(2, 'Paraíba do Sul', ''),
(3, 'Litoral Norte', ''),
(5, 'Piracicaba/Capivari/Jundaí', ''),
(6, 'Alto Tietê', ''),
(7, 'Baixada Santista', ''),
(11, 'Ribeira de Iguape e Litoral Sul', ''),
(14, 'Alto Paranapanema', '');

-- SELECT pp.resourceID, pp.title, pp.description, t.nome AS tipo, i.nome AS instituicao, d.nome AS dominio, pp.bibliographicCitation, pp.references_url FROM politicas_publicas pp
-- JOIN tipo_pp t ON pp.tipoID = t.tipoID
-- JOIN instituicao i ON pp.instituicaoID = i.instituicaoID
-- JOIN dominio d ON pp.dominioID = d.dominioID
-- WHERE t.nome LIKE 'Decreto' ORDER BY pp.resourceID;

-- SELECT count(t.nome) FROM politicas_publicas pp
-- JOIN tipo_pp t ON pp.tipoID = t.tipoID
-- JOIN instituicao i ON pp.instituicaoID = i.instituicaoID
-- JOIN dominio d ON pp.dominioID = d.dominioID
-- WHERE pp.tipoID = 2
-- ORDER BY pp.resourceID;