from src.request_handler import data_response
from src.contacts_service import ContactsService

contacts_service = ContactsService()

#Get the contacts from the contacts service
def get_contacts(event, context):
    contacts = contacts_service.get_contacts()

    return data_response(contacts)

#Get the personal info details for a specific id
def personal_info(event, context):
    identifier = event["queryStringParameters"]["id"]   
    personal_data = contacts_service.personal_info(identifier)

    return data_response(personal_data[0])

#Creates a new contact with mandatory info
def new_contact(event, context):
    data = event["body"]
    add_contact = contacts_service.new_contact(data)

    if add_contact == "Success":
        return data_response({"message": "Contact uploaded successfully"})
    
    return data_response({"message": "Error uploading data"})

#Updates an existing contact
def edit_contact(event, context):
    data = event["body"]
    update_contact = contacts_service.edit_contact(data)

    if update_contact == "Success":
        return data_response({"message": "Contact updated successfully"})
    
    return data_response({"message": "Error updating data"})

#Deletes all entries of a specific id
def delete_contact(event, context):
    identifier = event["queryStringParameters"]["id"]
    delete_data = contacts_service.delete_contact(identifier)

    return data_response({"message": "Deleted contact"})

#Upload an img to an specific id
def upload_image(event, context):
    upload = contacts_service.upload_image(event)
    return data_response({"message": upload})