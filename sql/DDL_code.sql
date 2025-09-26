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
-- Domínios (Estadual, Federal, Municipal etc.)
-- -------------------------------------------------------------------

-- CREATE TABLE dominio (
--     dominioID TINYINT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(50) NOT NULL UNIQUE
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE public_policies (
    resourceID SMALLINT AUTO_INCREMENT PRIMARY KEY,  -- DarwinCore: identificador
    title VARCHAR(100) NOT NULL,                -- DarwinCore: title
    description TEXT,                           -- DarwinCore: description
    bibliographicCitation TEXT,                 -- DarwinCore: bibliographicCitation
    references_url TEXT,                        -- DarwinCore: references
    typeID TINYINT NOT NULL,
    institutionID TINYINT NOT NULL,
    -- dominioID TINYINT NOT NULL,

    -- Relacionamentos
    FOREIGN KEY (typeID) REFERENCES type_pp(typeID),
    FOREIGN KEY (institutionID) REFERENCES institutions(institutionID)
    -- FOREIGN KEY (dominioID) REFERENCES dominio(dominioID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE RGI (
	rgiID MEDIUMINT PRIMARY KEY,
    rgi VARCHAR(80)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE RGINT (
	rgintID SMALLINT PRIMARY KEY,
    rgint VARCHAR(80)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE municipalities (
	municipalityID MEDIUMINT PRIMARY KEY,
    municipality VARCHAR(100) not null,
    rgiID MEDIUMINT NOT NULL,
    rgintID	SMALLINT NOT NULL,
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
    FOREIGN KEY (rgintID) REFERENCES RGINT(rgintID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE ugrhis (
    ugrhiID TINYINT PRIMARY KEY,
    ugrhi VARCHAR(100) NOT NULL,
    geometry LONGTEXT -- armazenar a string "intacta"
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE municipality_ugrhi (
    municipalityID MEDIUMINT,
    ugrhiID TINYINT,
    PRIMARY KEY (municipalityID, ugrhiID),
    FOREIGN KEY (municipalityID) REFERENCES municipalities(municipalityID),
    FOREIGN KEY (ugrhiID) REFERENCES ugrhis(ugrhiID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;