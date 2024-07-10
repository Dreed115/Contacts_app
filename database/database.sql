CREATE DATABASE IF NOT EXISTS contact_app;
USE contact_app;

CREATE TABLE IF NOT EXISTS Contactos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    contact_name VARCHAR(100) NOT NULL
);

CREATE TABLE PersonalInfo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombres VARCHAR(255) NOT NULL,
    ApellidoPaterno VARCHAR(255) NOT NULL,
    ApellidoMaterno VARCHAR(255),
    FechaNacimiento DATE,
    Alias VARCHAR(255),
    Fotografia MEDIUMBLOB, -- Store the .png file as a binary large object (BLOB)
    CONSTRAINT check_png CHECK (Fotografia IS NULL OR Fotografia LIKE '%.png'), -- Ensure uploaded file is .png
    UNIQUE KEY (Nombres, ApellidoPaterno, ApellidoMaterno) -- Ensure uniqueness based on names
);

CREATE TABLE Correos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ContactoID INT,
    CorreoElectronico VARCHAR(255),
    FOREIGN KEY (ContactoID) REFERENCES PersonalInfo(ID) ON DELETE CASCADE
);

CREATE TABLE Telefonos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ContactoID INT,
    TipoTelefono VARCHAR(50), -- User-defined label for the phone type
    NumeroTelefono VARCHAR(20),
    FOREIGN KEY (ContactoID) REFERENCES PersonalInfo(ID) ON DELETE CASCADE
);

CREATE TABLE Direcciones (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ContactoID INT,
    Direccion TEXT,
    FOREIGN KEY (ContactoID) REFERENCES PersonalInfo(ID) ON DELETE CASCADE
);
