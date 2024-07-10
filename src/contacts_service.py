import mysql.connector
import json
import base64 
import re

class ContactsService: 
    #Establish a primery conection to the database 
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",  
            user="root", 
            password="N!c0demus", 
            database="contact_app_test3" 
        )

        if not self.db_connection.is_connected():
            return "Unable to connect to the database"

        print("Connected to MySQL database")

    #Reresh the database connection when needed
    def refresh_connection(self):
        if self.db_connection.is_connected():
            self.db_connection.close()
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="N!c0demus",
            database="contact_app_test3"
        )

    #Get all the entries in the table contactos
    def get_contacts(self):
        self.refresh_connection()
        cursor = self.db_connection.cursor(dictionary=True)
        select_query = "select * from contactos;"
        cursor.execute(select_query)

        records = cursor.fetchall()

        cursor.close()
        return records
    
    #Returns a json of all the data of the user in the database
    def personal_info(self, id):
        self.refresh_connection()
        cursor = self.db_connection.cursor(dictionary=True)
        select_query = """
                        SELECT 
                            ci.*, 
                            GROUP_CONCAT(DISTINCT p.TipoTelefono SEPARATOR ', ') AS phone_type,
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
                            ci.id = """ + str(id) + """
                        GROUP BY 
                            ci.id;
                        """
        cursor.execute(select_query)
        contact = cursor.fetchall()

        print(contact)
        if contact[0]['FechaNacimiento'] is not None:
            contact[0]['FechaNacimiento'] = contact[0]['FechaNacimiento'].strftime('%m/%d/%Y')

        cursor.close()
        return contact
    
    #Creates a new contact with input method, for all posible values
    def new_contact(self, data):
        data = json.loads(data)
        cursor = self.db_connection.cursor(dictionary=True)

        #Handle exceptions that can happens and establish always an alias
        if data["Alias"] == "":
            data["Alias"] = data["Nombres"]

        if data["FechaNacimiento"] == "":
            data["FechaNacimiento"] = None

        select_query = """  INSERT INTO PersonalInfo (Nombres, ApellidoPaterno, ApellidoMaterno, FechaNacimiento, Alias)
                            VALUES (%s, %s, %s, %s, %s);"""
        
        val = (data["Nombres"], data["ApellidoPaterno"], data["ApellidoMaterno"], data["FechaNacimiento"], data["Alias"])
        cursor.execute(select_query, val)
        
        select_query = "SET @personal_info_id = LAST_INSERT_ID();"
        cursor.execute(select_query)

        select_query =  """ INSERT INTO Contactos (ID, contact_name)
                            VALUES (@personal_info_id, %s);"""
        
        val = (data["Alias"],)
        cursor.execute(select_query, val)

        #Insert the phone number and detail for all numbers passed 
        for telefono in data["phone_numbers"]:
            select_query = """  INSERT INTO Telefonos (ContactoID, TipoTelefono, NumeroTelefono)
                                VALUES (@personal_info_id, %s, %s);"""
            val = (telefono["key"], telefono["value"])
            cursor.execute(select_query, val)

        if data["emails"] != "":
            for email in data["emails"]:
                select_query = """  INSERT INTO Correos (ContactoID, CorreoElectronico)
                                    VALUES (@personal_info_id, %s);"""
                val = email
                cursor.execute(select_query, (val,))
        
        if data["addresses"] != "":
            for address in data["addresses"]:
                select_query = """  INSERT INTO Direcciones (ContactoID, Direccion)
                                    VALUES (@personal_info_id, %s);"""
                val = address
                cursor.execute(select_query, (val,))

        self.db_connection.commit()

        cursor.close()
        return "Success"
    
    #Updates the current info of the contact and ads o remove the necesary
    def edit_contact(self, data):
        data = json.loads(data)
        cursor = self.db_connection.cursor(dictionary=True)
        if data["Alias"] == "":
            data["Alias"] = data["Nombres"]

        if data["FechaNacimiento"] == "":
            data["FechaNacimiento"] = None

        select_query = """  UPDATE PersonalInfo
                            SET Nombres = %s, 
                                ApellidoPaterno = %s, 
                                ApellidoMaterno = %s, 
                                FechaNacimiento = %s, 
                                Alias = %s
                            WHERE ID = %s;"""
        val = (data["Nombres"], data["ApellidoPaterno"], data["ApellidoMaterno"], data["FechaNacimiento"], data["Alias"], data["id"])
        cursor.execute(select_query, val)

        select_query = """  UPDATE Contactos
                            SET contact_name = %s
                            WHERE ID = %s;"""
        val = (data["Alias"], data["id"])
        cursor.execute(select_query, val)

        #Deñetes the entries in the existing tables, to be able to rewrite an not be repeated data
        query = "DELETE FROM Telefonos WHERE ContactoID = " + str(data["id"]) + ";"
        cursor.execute(query)
 
        query = "DELETE FROM Correos WHERE ContactoID = " + str(data["id"]) + ";"
        cursor.execute(query)

        query = "DELETE FROM Direcciones WHERE ContactoID = " + str(data["id"]) + ";"
        cursor.execute(query)


        #Insert the data for the specific id
        for telefono in data["phone_numbers"]:
            select_query = """  INSERT INTO Telefonos (ContactoID, TipoTelefono, NumeroTelefono)
                                VALUES (%s, %s, %s);"""
            val = (data["id"], telefono["key"], telefono["value"])
            cursor.execute(select_query, val)

        if data["emails"] != "":
            for email in data["emails"]:
                select_query = """  INSERT INTO Correos (ContactoID, CorreoElectronico)
                                    VALUES (%s, %s);"""
                val = (data["id"], email)
                cursor.execute(select_query, val)
        
        if data["addresses"] != "":
            for address in data["addresses"]:
                select_query = """  INSERT INTO Direcciones (ContactoID, Direccion)
                                    VALUES (%s, %s);"""
                val = (data["id"], address)
                cursor.execute(select_query, val)

        self.db_connection.commit()

        cursor.close()
        return "Success"
    
    #Deletes all the entries of the contact in all the tables with the same id
    def delete_contact(self, id):
        self.refresh_connection()
        cursor = self.db_connection.cursor(dictionary=True)
        select_query = "  DELETE FROM PersonalInfo WHERE ID = " + str(id) + ";"
        cursor.execute(select_query)

        select_query = "  DELETE FROM Contactos WHERE ID = " + str(id) + ";"
        cursor.execute(select_query)

        self.db_connection.commit()
        cursor.close()
        return "Deleted"
    
    #Upload an image an save it in a image bucket
    def upload_image(self, event):
        self.refresh_connection()
        cursor = self.db_connection.cursor(dictionary=True)

        #Gets the event and exctract the needed data
        event_json = base64.b64decode(event["body"])
        
        boundary1 = event_json.split(b'\r\n')[0].decode('utf-8').strip()
        parts = event_json.split(boundary1.encode('utf-8'))[1:-1]

        data = {}

        #Saves image and contactid
        for part in parts:
            name_match = re.search(rb'Content-Disposition: form-data; name="([^"]+)"', part)
            if name_match:
                name = name_match.group(1).decode('utf-8')
                value_match = re.search(rb'\r\n\r\n(.*?)\r\n', part, re.DOTALL)
                if value_match:
                    value = value_match.group(1)
                    data[name] = value.decode('utf-8') if name != 'image' else value

        #Uses a specific director for local purposes, can be replaced for online files bucket
        file_path = "C:\\Users\\diego\\OneDrive\\Escritorio\\Proyectos\\prueba_contactos\\web\\src\\image_bucket\\"
        flie_name = "img_"+str(data["contactId"])+".jpg"

        with open(file_path + flie_name, 'wb') as f:
            f.write(data["image"])

        #Update tthe image path to be always the same as the upladed
        select_query = """  UPDATE PersonalInfo SET Fotografia_path = %s WHERE ID = %s;"""
        val = (flie_name, data["contactId"])
        cursor.execute(select_query, val)

        select_query = """  UPDATE Contactos SET img_path = %s WHERE ID = %s;"""
        val = (flie_name, data["contactId"])
        cursor.execute(select_query, val)

        self.db_connection.commit()
        cursor.close()

        return "Upload"
    