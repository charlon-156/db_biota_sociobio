DROP DATABASE IF EXISTS biota_sociobiodiversidade;

CREATE DATABASE biota_sociobiodiversidade
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE biota_sociobiodiversidade;

-- -------------------------------------------------------------------
-- Tipos (Lei, Decreto, Resolução, Portaria, Programa etc.)
-- -------------------------------------------------------------------

CREATE TABLE tipo_pp (
	tipoID TINYINT AUTO_INCREMENT PRIMARY KEY,
    nome TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -------------------------------------------------------------------
-- Instituições (Secretaria, Ministério, Governo, Presidência etc.)
-- -------------------------------------------------------------------

CREATE TABLE instituicao (
    instituicaoID TINYINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(500) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- -------------------------------------------------------------------
-- Domínios (Estadual, Federal, Municipal etc.)
-- -------------------------------------------------------------------

CREATE TABLE dominio (
    dominioID TINYINT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE politicas_publicas (
    resourceID INT AUTO_INCREMENT PRIMARY KEY,  -- DarwinCore: identificador
    title VARCHAR(200) NOT NULL,                -- DarwinCore: title
    description TEXT,                           -- DarwinCore: description
    bibliographicCitation TEXT,                 -- DarwinCore: bibliographicCitation
    references_url TEXT,                        -- DarwinCore: references
    tipoID TINYINT NOT NULL,
    instituicaoID TINYINT NOT NULL,
    dominioID TINYINT NOT NULL,

    -- Relacionamentos
    FOREIGN KEY (tipoID) REFERENCES tipo_pp( tipoID),
    FOREIGN KEY (instituicaoID) REFERENCES instituicao(instituicaoID),
    FOREIGN KEY (dominioID) REFERENCES dominio(dominioID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;





