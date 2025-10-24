DROP DATABASE IF EXISTS biota_sociobiodiversidade;

CREATE DATABASE biota_sociobiodiversidade
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE biota_sociobiodiversidade;

-- -------------------------------------------------------------------
-- Tipos (Lei, Decreto, Resolução, Portaria, Programa etc.)
-- -------------------------------------------------------------------

CREATE TABLE type_pp (
	typeID TINYINT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Instituições (Secretaria, Ministério, Governo, Presidência etc.)
-- -------------------------------------------------------------------

CREATE TABLE institutions (
    institutionID TINYINT AUTO_INCREMENT PRIMARY KEY,
    institution VARCHAR(200) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Situação Legal (Vigente, Revogada, Vetado)
-- -------------------------------------------------------------------

CREATE TABLE legislativeStatus (
    legislativeStatusID TINYINT AUTO_INCREMENT PRIMARY KEY,
    legislativeStatus VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Políticas Públicas (Nº 4.703, DE 21 DE MAIO DE 2003...)
-- -------------------------------------------------------------------

CREATE TABLE public_policies (
    resourceID SMALLINT AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(100) NOT NULL,                
    description TEXT,                           
    bibliographicCitation TEXT,                 
    references_url TEXT,                        
    typeID TINYINT NOT NULL,
    institutionID TINYINT NOT NULL,
    legislativeStatusID TINYINT,

    FOREIGN KEY (typeID) REFERENCES type_pp(typeID),
    FOREIGN KEY (institutionID) REFERENCES institutions(institutionID),
    FOREIGN kEY (legislativeStatusID) REFERENCES legislativeStatus(legislativeStatusID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Região Imediata (Itapeva, Registro...)
-- -------------------------------------------------------------------

CREATE TABLE RGI (
	rgiID MEDIUMINT PRIMARY KEY,
    rgi VARCHAR(80)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Região Intermediária (Sorocaba, São José dos Campos)
-- -------------------------------------------------------------------

CREATE TABLE RGINT (
	rgintID SMALLINT PRIMARY KEY,
    rgint VARCHAR(80)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Koppen (Cfa, Cwa, Cwb...)
-- -------------------------------------------------------------------

CREATE TABLE koppen (
    koppenID TINYINT PRIMARY KEY AUTO_INCREMENT,
    dynamicProper VARCHAR(5),
    description VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- regiões (Vale do Ribeira, Litoral Norte)
-- -------------------------------------------------------------------

CREATE TABLE regions (
	regionID TINYINT PRIMARY KEY AUTO_INCREMENT,
	region VARCHAR(50) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Municípios (Barra do Chapéu, Ubatuba...)
-- -------------------------------------------------------------------

CREATE TABLE municipalities (
	municipalityID MEDIUMINT PRIMARY KEY,
    municipality VARCHAR(100) not null,
    rgiID MEDIUMINT NOT NULL,
    rgintID	SMALLINT NOT NULL,
    regionID TINYINT NOT NULL,
    areaKM2	FLOAT,
    population MEDIUMINT,
    man	MEDIUMINT,
    woman MEDIUMINT,	
    genderRatio FLOAT,	
    middleAge FLOAT,
    populationDensity FLOAT,
    populationProtectedArea MEDIUMINT,
    indigenousPopulation SMALLINT,
    insideIndigenousLand SMALLINT,
    outsideIndigenousLand SMALLINT,
    quilombolaPopulation SMALLINT,
    insideQuilombolaLand SMALLINT,
    outsideQuilombolaLand SMALLINT,
    populationByRaceAmarela MEDIUMINT,
    populationByRaceBranca MEDIUMINT,
    populationByRaceIndigena MEDIUMINT,
    populationByRaceParda MEDIUMINT,
    populationByRacePreta MEDIUMINT,
    FOREIGN KEY (rgiID) REFERENCES RGI(rgiID),
    FOREIGN KEY (rgintID) REFERENCES RGINT(rgintID),
    FOREIGN KEY (regionID) REFERENCES regions(regionID) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- Climas dos munícipios ()
-- -------------------------------------------------------------------

CREATE TABLE climate_mun (
    municipalityID MEDIUMINT NOT NULL PRIMARY KEY,
    koppenID TINYINT NOT NULL,
    elevation FLOAT,
    measurementOrFact_T_jan FLOAT,
    measurementOrFact_T_feb FLOAT,
    measurementOrFact_T_mar FLOAT,
    measurementOrFact_T_apr FLOAT,
    measurementOrFact_T_may FLOAT,
    measurementOrFact_T_jun FLOAT,
    measurementOrFact_T_jul FLOAT,
    measurementOrFact_T_aug FLOAT,
    measurementOrFact_T_sep FLOAT,
    measurementOrFact_T_oct FLOAT,
    measurementOrFact_T_nov FLOAT,
    measurementOrFact_T_dec FLOAT,
    measurementOrFact_R_jan SMALLINT,
    measurementOrFact_R_feb SMALLINT,
    measurementOrFact_R_mar SMALLINT,
    measurementOrFact_R_apr SMALLINT,
    measurementOrFact_R_may SMALLINT,
    measurementOrFact_R_jun SMALLINT,
    measurementOrFact_R_jul SMALLINT,
    measurementOrFact_R_aug SMALLINT,
    measurementOrFact_R_sep SMALLINT,
    measurementOrFact_R_oct SMALLINT,
    measurementOrFact_R_nov SMALLINT,
    measurementOrFact_R_dec SMALLINT,
    geometry LONGTEXT,
    FOREIGN KEY (koppenID) REFERENCES koppen(koppenID),
    FOREIGN KEY (municipalityID) REFERENCES municipalities(municipalityID)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- UGRHI (Unidade de Gerenciamento de Recursos Hídricos)
-- -------------------------------------------------------------------

CREATE TABLE ugrhis (
    ugrhiID TINYINT PRIMARY KEY,
    ugrhi VARCHAR(100) NOT NULL,
    geometry LONGTEXT -- armazenar a string "intacta"
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------------------------------------------------------
-- UGRHIs dos municipios (Unidade de Gerenciamento de Recursos Hídricos)
-- -------------------------------------------------------------------

CREATE TABLE municipality_ugrhi (
    municipalityID MEDIUMINT,
    ugrhiID TINYINT,
    PRIMARY KEY (municipalityID, ugrhiID),
    FOREIGN KEY (municipalityID) REFERENCES municipalities(municipalityID),
    FOREIGN KEY (ugrhiID) REFERENCES ugrhis(ugrhiID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE lifeForms (
    lifeFormID TINYINT PRIMARY KEY AUTO_INCREMENT,
    lifeForm VARCHAR(40)
);

CREATE TABLE substrate (
    substrateID TINYINT PRIMARY KEY AUTO_INCREMENT,
    substrate VARCHAR(30)
);

CREATE TABLE localityStates (
    localityStatesID TINYINT PRIMARY KEY AUTO_INCREMENT,
    localityStates VARCHAR(50)
);

CREATE TABLE biomes (
    biomeID TINYINT PRIMARY KEY AUTO_INCREMENT,
    biome VARCHAR(80)
);

CREATE TABLE species (
    speciesID TINYINT PRIMARY KEY AUTO_INCREMENT,
    species VARCHAR(50),
    family VARCHAR(30),
    scientificName (50),
    authorship VARCHAR(50),
    threatenedStatusIUCN VARCHAR(4),
    threatenedStatusCNCFLORA VARCHAR(4),
    origin ENUM('Nativa', 'Naturalizada', 'Cultivada'),
    endemism ENUM('Sim', 'Não'),

);
