-- Update PersonalInfo table
UPDATE PersonalInfo
SET Nombres = 'Luis', 
    ApellidoPaterno = 'Guitierrez', 
    ApellidoMaterno = 'Calderon', 
    FechaNacimiento = '2000-23-12', 
    Alias = 'Luis'
WHERE ID = 10;  -- Replace with the actual ID of the personal info to be updated

-- Update Contactos table
UPDATE Contactos
SET contact_name = 'Luis'
WHERE ID = 10;

-- Update Telefonos table
UPDATE Telefonos
SET TipoTelefono = 'Casa', 
    NumeroTelefono = '8441791818'
WHERE ContactoID = 10; -- Adjust this query if there are multiple phone numbers

-- Update Direcciones table
UPDATE Direcciones
SET Direccion = 'Tamaulipas 135, Saltillo, Coahuila'
WHERE ContactoID = 10; -- Adjust this query if there are multiple addresses

-- Update Correos table
UPDATE Correos
SET CorreoElectronico = 'deigoarr@hotmail.es'
WHERE ContactoID = 10; -- Adjust this query if there are multiple emails
