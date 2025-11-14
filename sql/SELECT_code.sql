-- -------------------------------------------------------------
-- Dev.: Charlon F. Monteiro
-- project: Banco de Dados Sociobiodiversidade
-- file: base.py
-- description: Important module responsible for centralizing 
--              functions to support the generation of SQL 
--              commands for insertion from Excel spreadsheets
-- Last update: 2025-10-10
-- --------------------------------------------------------------

-- dados de políticas públicas (visual)
SELECT pp.resourceID as "ID da politica", pp.title AS "Título", pp.description AS "Descrição", l.legislativeStatus AS 'Status da legislação', t.TYPE AS "Tpo da Política Pública", i.institution AS "instituicao", pp.bibliographicCitation AS "Referências bibliográficas", pp.references_url  AS "URL" FROM public_policies pp
JOIN type_pp t ON pp.typeID = t.typeID
JOIN institutions i ON pp.institutionID = i.institutionID
LEFT JOIN legislativestatus l ON pp.legislativeStatusID = l.legislativeStatusID  
ORDER BY pp.resourceID;

-- dados de políticas públicas (cru)
SELECT pp.resourceID, pp.title, pp.description, l.legislativeStatus, t.type, i.institution, pp.bibliographicCitation, pp.references_url FROM public_policies pp
JOIN type_pp t ON pp.typeID = t.typeID
JOIN institutions i ON pp.institutionID = i.institutionID
LEFT JOIN legislativestatus l ON pp.legislativeStatusID = l.legislativeStatusID  
ORDER BY pp.resourceID;

-- dados de políticas públicas selecionados por: instituição
-- WHERE i.institution LIKE ''
--
-- dados de políticas públicas selecionados por: tipo
-- WHERE t.type LIKE ''
--
-- dados de políticas públicas selecionados por: status legislativo
-- WHERE l.legislativestatus LIKE ''

SELECT * FROM species s ;
-- JOIN species_lifeForms sl ON s.speciesID = sl.speciesID
-- JOIN species_substrates ss ON s.speciesID = ss.speciesID
-- JOIN species_biomes sb ON s.speciesID = sb.speciesID
-- JOIN species_localityStates sc ON s.speciesID = sc.speciesID;

-- -- dados de municipios (visual)
SELECT m.municipalityID AS 'Código do município', m.municipality AS 'Município', gi.rgi AS 'Região Imediata', g.rgint AS 'Região Intermédiarias', m.areaKM2 AS 'Área KM²', m.population AS 'População', m.man AS 'Qntd. Homens', m.woman AS 'Qntd. Mulheres', m.genderRatio AS 'Razão de gênero', m.middleAge AS 'Idade média', m.populationDensity AS 'Densidade populacional', m.indigenousPopulation AS 'população indigena', m.insideIndigenousLand AS 'indigena dentro de território', m.outsideIndigenousLand AS 'indigena fora de território', m.quilombolaPopulation AS 'população quilombola', m.insideQuilombolaLand AS 'quilombola dentro de território', m.outsideQuilombolaLand AS 'quilombola fora de território', m.populationByRaceAmarela AS 'Qntd. de Amarelos', m.populationByRaceBranca AS 'Qntd. de Brancos', m.populationByRaceIndigena AS 'Qntd. de Indigenas', m.populationByRaceParda AS 'Qntd. de Pardos', m.populationByRacePreta AS 'Qntd. de Pretos' FROM municipalities m 
JOIN RGI gi ON m.rgiID = gi.rgiID
JOIN RGINT g ON m.rgintID = g.rgintID
JOIN regions r ON m.regionID = r.regionID
JOIN climate_mun cm ON m.municipalityID = cm.municipalityID
JOIN koppens k ON cm.koppenID = k.koppenID
ORDER BY m.municipality; 

SELECT m.municipalityID AS 'Código do município', m.municipality AS 'Município', u.ugrhi AS 'UGRHI' from municipality_ugrhi mu
JOIN municipalities m ON mu.municipalityID = m.municipalityID
JOIN ugrhis u ON mu.ugrhiID = u.ugrhiID;
