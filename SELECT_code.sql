SELECT pp.resourceID, pp.title, pp.description, t.TYPE AS tipo, i.institution AS instituicao, pp.bibliographicCitation, pp.references_url FROM public_policies pp
JOIN type_pp t ON pp.typeID = t.typeID
JOIN institutions i ON pp.institutionID = i.institutionID
ORDER BY pp.resourceID;

SELECT * FROM municipalities;

SELECT * FROM institutions;