select * from contactos;
select * from personalinfo;

SELECT 
    ci.*, 
    GROUP_CONCAT(DISTINCT p.NumeroTelefono SEPARATOR ', ') AS phone_numbers,
    GROUP_CONCAT(DISTINCT c.CorreoElectronico SEPARATOR ',') AS emails,
    GROUP_CONCAT(DISTINCT a.Direccion SEPARATOR '; ') AS addresses
FROM 
    personalinfo ci
LEFT JOIN 
    Telefonos p ON ci.id = p.ContactoID
LEFT JOIN
	Correos c ON ci.id = c.ContactoID
LEFT JOIN
    Direcciones a ON ci.id = a.ContactoID
WHERE 
    ci.id = 1
GROUP BY 
    ci.id;