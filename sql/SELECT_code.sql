-- -------------------------------------------------------------
-- Dev.: Charlon F. Monteiro
-- project: Banco de Dados Sociobiodiversidade
-- file: select_code.py
-- description: Important module responsible for centralizing
--              functions to support the generation of SQL
--              commands for insertion from Excel spreadsheets
-- Last update: 2026-05-28
-- --------------------------------------------------------------
 USE biota_sociobiodiversidade;

---
 -- CONSULTAS ANALÍTICAS PARA PESQUISA
-- Projeto BIOTA/FAPESP - Sociobiodiversidade
 -- Políticas públicas com maior alcance sobre espécies ameaçadas

SELECT pp.title AS título,
	   pt.type AS tipo,
       COUNT(DISTINCT s.speciesID) AS especies_ameacadas
FROM public_policies pp
JOIN type_pp pt ON pp.typeID = pt.typeID
JOIN public_policies_species pps ON pp.resourceID = pps.resourceID
JOIN species s ON pps.speciesID = s.speciesID
WHERE s.threatenedStatusIUCN IN ('CR','EN', 'VU','EW')
GROUP BY pp.resourceID, pp.title
ORDER BY especies_ameacadas DESC;

-- Quantidade de políticas por tipologia

SELECT t.typology,
       COUNT(DISTINCT pp.resourceID) AS total_politicas
FROM typologies t
JOIN pp_typology ppt ON t.typologyID = ppt.typologyID
JOIN public_policies pp ON pp.resourceID = ppt.resourceID
GROUP BY t.typology
ORDER BY total_politicas DESC;

-- Espécies ameaçadas sem cobertura normativa

SELECT s.speciesID,
       s.scientificNameAuthorship,
       s.threatenedStatusIUCN
FROM species s
JOIN public_policies_species pps ON s.speciesID = pps.speciesID
WHERE s.threatenedStatusIUCN IN ('CR','EN', 'VU','EW')
;

-- Municípios com maior quantidade de políticas públicas

SELECT m.municipality,
       COUNT(DISTINCT ppm.resourceID) AS total_politicas
FROM municipalities m
JOIN public_policies_municipalities ppm ON m.municipalityID = ppm.municipalityID
GROUP BY m.municipality
ORDER BY total_politicas DESC;

-- Municípios com políticas e populações tradicionais

SELECT m.municipality,
       COUNT(DISTINCT ppm.resourceID) AS politicas,
       m.indigenousPopulation,
       m.quilombolaPopulation
FROM municipalities m
JOIN public_policies_municipalities ppm ON m.municipalityID = ppm.municipalityID
GROUP BY m.municipality,
         m.indigenousPopulation,
         m.quilombolaPopulation
ORDER BY politicas DESC;

-- Cobertura normativa por bioma

SELECT b.biome,
       COUNT(DISTINCT pp.resourceID) AS total_politicas
FROM biomes b
JOIN species_biomes sb ON b.biomeID = sb.biomeID
JOIN public_policies_species pps ON sb.speciesID = pps.speciesID
JOIN public_policies pp ON pps.resourceID = pp.resourceID
GROUP BY b.biome
ORDER BY total_politicas DESC;

---
 -- Instituições mais atuantes na produção normativa

SELECT i.institution,
       COUNT(*) AS total_politicas
FROM public_policies pp
JOIN institutions i ON pp.institutionID = i.institutionID
GROUP BY i.institution
ORDER BY total_politicas DESC;

---
 -- Espécies ameaçadas por forma de vida

SELECT lf.lifeForm,
       s.threatenedStatusIUCN,
       COUNT(*) AS total
FROM species s
JOIN species_lifeForms slf ON s.speciesID = slf.speciesID
JOIN lifeForms lf ON slf.lifeFormID = lf.lifeFormID
WHERE s.threatenedStatusIUCN IS NOT NULL
GROUP BY lf.lifeForm,
         s.threatenedStatusIUCN
ORDER BY total DESC;

---
 -- Distribuição de espécies ameaçadas por bioma

SELECT b.biome,
       s.threatenedStatusIUCN,
       COUNT(DISTINCT s.speciesID) AS total_especies
FROM species s
JOIN species_biomes sb ON s.speciesID = sb.speciesID
JOIN biomes b ON sb.biomeID = b.biomeID
WHERE s.threatenedStatusIUCN IN ('CR','EN', 'VU','EW')
GROUP BY b.biome,
         s.threatenedStatusIUCN
ORDER BY total_especies DESC;

-- Políticas públicas por tipo de instrumento

SELECT tp.type AS tipo,
       COUNT(*) AS total
FROM public_policies pp
JOIN type_pp tp ON pp.typeID = tp.typeID
GROUP BY tp.type
ORDER BY total DESC;

-- Municípios com maior presença indígena e cobertura normativa

SELECT m.municipality,
       m.indigenousPopulation,
       COUNT(DISTINCT ppm.resourceID) AS total_politicas
FROM municipalities m
LEFT JOIN public_policies_municipalities ppm ON m.municipalityID = ppm.municipalityID
WHERE m.indigenousPopulation > 0
GROUP BY m.municipality,
         m.indigenousPopulation
ORDER BY m.indigenousPopulation DESC;

-- Municípios com maior presença quilombola e cobertura normativa

SELECT m.municipality,
       m.quilombolaPopulation,
       COUNT(DISTINCT ppm.resourceID) AS total_politicas
FROM municipalities m
LEFT JOIN public_policies_municipalities ppm ON m.municipalityID = ppm.municipalityID
WHERE m.quilombolaPopulation > 0
GROUP BY m.municipality,
         m.quilombolaPopulation
ORDER BY m.quilombolaPopulation DESC;

-- dados de políticas públicas (visual)

SELECT pp.resourceID AS "ID da politica",
       pp.title AS "Título",
       pp.description AS "Descrição",
       pp.justification AS "Justificativa",
       l.legislativeStatus AS 'Status da legislação',
       t.TYPE AS "Tpo da Política Pública",
       i.institution AS "instituicao",
       pp.bibliographicCitation AS "Referências bibliográficas",
       pp.references_url AS "URL"
FROM public_policies pp
JOIN type_pp t ON pp.typeID = t.typeID
JOIN institutions i ON pp.institutionID = i.institutionID
LEFT JOIN legislativestatus l ON pp.legislativeStatusID = l.legislativeStatusID
ORDER BY pp.resourceID;


SELECT *
FROM public_policies;


SELECT pp.resourceID,
       pp.title,
       tp.type AS tipo,
       i.institution AS instituicao,
       ls.legislativeStatus AS situacao_legal,
       t.typology AS tipologia
FROM public_policies pp
LEFT JOIN type_pp tp ON pp.typeID = tp.typeID
LEFT JOIN institutions i ON pp.institutionID = i.institutionID
LEFT JOIN legislativeStatus ls ON pp.legislativeStatusID = ls.legislativeStatusID
JOIN pp_typology ppt ON pp.resourceID = ppt.resourceID
JOIN typologies t ON ppt.typologyID = t.typologyID;


SELECT s.speciesID,
       s.scientificNameAuthorship,
       s.vernacularName,
       s.scientificNameAuthorship,
       s.origin,
       s.endemism,
       s.threatenedStatusIUCN,
       s.threatenedStatusCNCFLORA,
       b.biome,
       v.vegetationType,
       lf.lifeForm,
       sub.substrate
FROM species s
LEFT JOIN species_biomes sb ON s.speciesID = sb.speciesID
LEFT JOIN biomes b ON sb.biomeID = b.biomeID
LEFT JOIN species_vegetation sv ON s.speciesID = sv.speciesID
LEFT JOIN vegetationTypes v ON sv.vegetationTypeID = v.vegetationTypeID
LEFT JOIN species_lifeForms slf ON s.speciesID = slf.speciesID
LEFT JOIN lifeForms lf ON slf.lifeFormID = lf.lifeFormID
LEFT JOIN species_substrates ss ON s.speciesID = ss.speciesID
LEFT JOIN substrates sub ON ss.substrateID = sub.substrateID ;

;

-- dados de políticas públicas (cru)

SELECT pp.resourceID,
       pp.title,
       pp.description,
       l.legislativeStatus,
       t.type,
       i.institution,
       pp.bibliographicCitation,
       pp.references_url
FROM public_policies pp
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

SELECT *
FROM species s ;

-- JOIN species_lifeForms sl ON s.speciesID = sl.speciesID
-- JOIN species_substrates ss ON s.speciesID = ss.speciesID
-- JOIN species_biomes sb ON s.speciesID = sb.speciesID
-- JOIN species_localityStates sc ON s.speciesID = sc.speciesID;
 -- -- dados de municipios (visual)

SELECT m.municipalityID AS 'Código do município',
       m.municipality AS 'Município',
       gi.rgi AS 'Região Imediata',
       g.rgint AS 'Região Intermédiarias',
       m.areaKM2 AS 'Área KM²',
       m.population AS 'População',
       m.man AS 'Qntd. Homens',
       m.woman AS 'Qntd. Mulheres',
       m.genderRatio AS 'Razão de gênero',
       m.middleAge AS 'Idade média',
       m.populationDensity AS 'Densidade populacional',
       m.indigenousPopulation AS 'população indigena',
       m.insideIndigenousLand AS 'indigena dentro de território',
       m.outsideIndigenousLand AS 'indigena fora de território',
       m.quilombolaPopulation AS 'população quilombola',
       m.insideQuilombolaLand AS 'quilombola dentro de território',
       m.outsideQuilombolaLand AS 'quilombola fora de território',
       m.populationByRaceAmarela AS 'Qntd. de Amarelos',
       m.populationByRaceBranca AS 'Qntd. de Brancos',
       m.populationByRaceIndigena AS 'Qntd. de Indigenas',
       m.populationByRaceParda AS 'Qntd. de Pardos',
       m.populationByRacePreta AS 'Qntd. de Pretos'
FROM municipalities m
JOIN RGI gi ON m.rgiID = gi.rgiID
JOIN RGINT g ON m.rgintID = g.rgintID
JOIN regions r ON m.regionID = r.regionID
JOIN climate_mun cm ON m.municipalityID = cm.municipalityID
JOIN koppens k ON cm.koppenID = k.koppenID
ORDER BY m.municipality;


SELECT m.municipalityID AS 'Código do município',
       m.municipality AS 'Município',
       u.ugrhi AS 'UGRHI'
FROM municipality_ugrhi mu
JOIN municipalities m ON mu.municipalityID = m.municipalityID
JOIN ugrhis u ON mu.ugrhiID = u.ugrhiID;


SELECT *
FROM species;


SELECT *
FROM typesofuses;


SELECT *
FROM typesOfUses;