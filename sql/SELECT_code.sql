SELECT pp.resourceID, pp.title, pp.description, t.TYPE AS tipo, i.institution AS instituicao, pp.bibliographicCitation, pp.references_url FROM public_policies pp
JOIN type_pp t ON pp.typeID = t.typeID
JOIN institutions i ON pp.institutionID = i.institutionID
ORDER BY pp.resourceID;

SELECT m.municipalityID AS 'Código do município', m.municipality AS 'Município', gi.rgi AS 'Região Imediata', g.rgint AS 'Região Intermédiarias', m.areaKM2 AS 'Área KM²', m.population AS 'População', m.man AS 'Qntd. Homens', m.woman AS 'Qntd. Mulheres', m.genderRatio AS 'Razão de gênero', m.middleAge AS 'Idade média', m.populationDensity AS 'Densidade populacional', m.populationProtectedArea AS 'população em área de proteção', m.insideIndigenousLand AS 'indigena dentro de território', m.outsideIndigenousLand AS 'indigena fora de território', m.quilombolaPopulation AS 'população quilombola', m.insideQuilombolaLand AS 'quilombola dentro de território', m.outsideQuilombolaLand AS 'quilombola fora de território', m.populationByRaceAmarela AS 'Qntd. de Amarelos', m.populationByRaceBranca AS 'Qntd. de Brancos', m.populationByRaceIndigena AS 'Qntd. de Indigenas', m.populationByRaceParda AS 'Qntd. de Pardos', m.populationByRacePreta AS 'Qntd. de Pretos' FROM municipalities m 
JOIN RGI gi ON m.rgiID = gi.rgiID
JOIN RGINT g ON m.rgintID = g.rgintID
ORDER BY m.municipality; 

SELECT * FROM municipalities;

SELECT * FROM institutions;