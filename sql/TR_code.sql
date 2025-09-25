DELIMITER /

CREATE TRIGGER tr_vallidationMunicipalities BEFORE INSERT ON municipalities for each ROW
BEGIN
	IF (new.indigenousPopulation < (new.insideIndigenousLand + new.outsideIndigenousLand)) THEN
    	signal sqlstate '45000' set message_text = 'ERRO: Quantidade populacional dos indigenas inconscistente';
    ELSEIF (new.quilombolaPopulation < (new.insideQuilombolaLand + new.outsideQuilombolaLand)) THEN
        signal sqlstate '45000' set message_text = 'ERRO: Quantidade populacional dos quilombolas inconscistente';
    ELSEIF (new.population < (new.man + new.woman)) THEN
        signal sqlstate '45000' set message_text = 'ERRO: Quantidade populacional de gênero inconscistente';
    END IF;
END /

DELIMITER ;