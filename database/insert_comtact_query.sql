INSERT INTO PersonalInfo (Nombres, ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Alias)
VALUES ('Pedro2', 'no se', 'no se', '', 'luis');

SET @personal_info_id = LAST_INSERT_ID();

INSERT INTO Contactos (ID, contact_name)
VALUES (@personal_info_id, 'Pedro');

-- Example for Telefonos table
INSERT INTO Telefonos (ContactoID, TipoTelefono, NumeroTelefono)
VALUES (@personal_info_id, 'Casa', '8441791818');

-- Example for Direcciones table
INSERT INTO Direcciones (ContactoID, Direccion)
VALUES (@personal_info_id, 'Tamaulipas 135, Saltillo, Coahuila');

-- Example for Correos table
INSERT INTO Correos (ContactoID, CorreoElectronico)
VALUES (@personal_info_id, 'deigoarr@hotmail.es');
