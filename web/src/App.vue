<template>
  <main>
    <!-- Search bar Section-->
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="Search contacts..." />
      <button @click="openAddContactModal">Add Contact</button>
    </div>

    <!-- Contacts Cards Section-->
    <div class="contacts-container">
      <div v-for="contact in filteredContacts" :key="contact.ID" class="contact-card" @click="fetchPersonalInfo(contact.ID)">
        <img :src="getContactImagePath(contact.img_path)" alt="contact image" class="contact-image" />
        <div class="contact-name">{{ contact.contact_name }}</div>
      </div>
    </div>

    <!-- Personal info Section-->
    <div class="personal-info" :class="{ 'personal-info-visible': selectedContact }">
      <button class="close-button" @click="closePersonalInfo">X</button>
      <div v-if="selectedContact">
        <h2>{{ selectedContact.Alias ?? 'N/A' }}</h2>
        <p><strong>Nombres:</strong> {{ selectedContact.Nombres ?? 'N/A' }}</p>
        <p><strong>Apellido Paterno:</strong> {{ selectedContact.ApellidoPaterno ?? 'N/A' }}</p>
        <p><strong>Apellido Materno:</strong> {{ selectedContact.ApellidoMaterno ?? 'N/A' }}</p>
        <p><strong>Fecha de Nacimiento:</strong> {{ selectedContact.FechaNacimiento ?? 'N/A' }}</p>
        <img :src="getContactImagePath(selectedContact.Fotografia_path)" alt="contact image" class="contact-image" @click="triggerFileUpload" />
        <input type="file" ref="fileInput" @change="uploadNewImage" style="display: none;" />
        <p><strong>Phone Numbers:</strong></p>
        <ul>
          <li v-for="(phone, index) in getPhoneDetails(selectedContact)" :key="index">
            {{ phone.number ?? 'N/A'}} ({{ phone.type ?? 'N/A'}})
          </li>
        </ul>
        <p><strong>Emails:</strong></p>
        <ul>
          <li v-for="email in (selectedContact.emails || '').split(',')" :key="email.trim()">{{ email.trim() || 'N/A' }}</li>
        </ul>
        <p><strong>Addresses:</strong></p>
        <ul>
          <li v-for="address in (selectedContact.addresses || '').split(';')" :key="address.trim()">{{ address.trim() || 'N/A' }}</li>
        </ul>
        <div class="buttons-container">
          <button class="edit-button" @click="openEditContactModal">Edit</button>
          <button class="delete-button" @click="deleteContact(selectedContact.ID)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add Contact Section-->
    <div class="add-contact-modal" v-if="showAddContactModal">
      <div class="modal-content">
        <button class="close-button" @click="closeAddContactModal">X</button>
        <h2>Add New Contact</h2>
        <form @submit.prevent="addNewContact">
          <div>
            <label>Nombres*</label>
            <input type="text" v-model="newContact.Nombres" required />
          </div>
          <div>
            <label>Apellido Paterno</label>
            <input type="text" v-model="newContact.ApellidoPaterno" />
          </div>
          <div>
            <label>Apellido Materno</label>
            <input type="text" v-model="newContact.ApellidoMaterno" />
          </div>
          <div>
            <label>Fecha Nacimiento</label>
            <input type="date" v-model="newContact.FechaNacimiento" />
          </div>
          <div>
            <label>Alias</label>
            <input type="text" v-model="newContact.Alias" />
          </div>
          <div>
            <label>Telefonos*</label>
            <div v-for="(phone, index) in newContact.phone_numbers" :key="index" class="phone-entry">
              <input type="text" :value="phone.key" @input="updatePhoneKey(index, $event.target.value)" placeholder="Label" />
              <input type="text" :value="phone.value" @input="updatePhoneValue(index, $event.target.value)" placeholder="Phone Number" />
              <button type="button" @click="removePhone(index)">Remove</button>
            </div>
            <button type="button" @click="addPhone">Add Phone</button>
          </div>
          <div>
            <label>Emails</label>
            <div v-for="(email, index) in newContact.emails" :key="index" class="email-entry">
              <input type="text" :value="email" @input="updateEmail(index, $event.target.value)" placeholder="Email" />
              <button type="button" @click="removeEmail(index)">Remove</button>
            </div>
            <button type="button" @click="addEmail">Add Email</button>
          </div>
          <div>
            <label>Direcciones</label>
            <div v-for="(address, index) in newContact.addresses" :key="index" class="address-entry">
              <input type="text" :value="address" @input="updateAddress(index, $event.target.value)" placeholder="Address" />
              <button type="button" @click="removeAddress(index)">Remove</button>
            </div>
            <button type="button" @click="addAddress">Add Address</button>
          </div>
          <button type="submit">Send</button>
        </form>
      </div>
    </div>

    <!-- Edit Contact Section-->
    <div class="edit-contact-modal" v-if="showEditContactModal">
      <div class="modal-content">
        <button class="close-button" @click="closeEditContactModal">X</button>
        <h2>Edit Contact</h2>
        <form @submit.prevent="editContact">
          <div>
            <label>Nombres*</label>
            <input type="text" v-model="editContactData.Nombres" required />
          </div>
          <div>
            <label>Apellido Paterno</label>
            <input type="text" v-model="editContactData.ApellidoPaterno" />
          </div>
          <div>
            <label>Apellido Materno</label>
            <input type="text" v-model="editContactData.ApellidoMaterno" />
          </div>
          <div>
            <label>Fecha Nacimiento</label>
            <input type="date" v-model="editContactData.FechaNacimiento" />
          </div>
          <div>
            <label>Alias</label>
            <input type="text" v-model="editContactData.Alias" />
          </div>
          <div>
            <label>Telefonos*</label>
            <div v-for="(phone, index) in editContactData.phone_numbers" :key="index" class="phone-entry">
              <input type="text" :value="phone.key" @input="updateEditPhoneKey(index, $event.target.value)" placeholder="Label" />
              <input type="text" :value="phone.value" @input="updateEditPhoneValue(index, $event.target.value)" placeholder="Phone Number" />
              <button type="button" @click="removeEditPhone(index)">Remove</button>
            </div>
            <button type="button" @click="addEditPhone">Add Phone</button>
          </div>
          <div>
            <label>Emails</label>
            <div v-for="(email, index) in editContactData.emails" :key="index" class="email-entry">
              <input type="text" :value="email" @input="updateEditEmail(index, $event.target.value)" placeholder="Email" />
              <button type="button" @click="removeEditEmail(index)">Remove</button>
            </div>
            <button type="button" @click="addEditEmail">Add Email</button>
          </div>
          <div>
            <label>Direcciones</label>
            <div v-for="(address, index) in editContactData.addresses" :key="index" class="address-entry">
              <input type="text" :value="address" @input="updateEditAddress(index, $event.target.value)" placeholder="Address" />
              <button type="button" @click="removeEditAddress(index)">Remove</button>
            </div>
            <button type="button" @click="addEditAddress">Add Address</button>
          </div>
          <button type="submit">Update</button>
        </form>
      </div>
    </div>
  </main>
</template>


<script>
import axios from 'axios';
import defaultImage from './assets/logo_contacto.png';

/* Varables and data used*/
export default {
  name: 'App',
  data() {
    return {
      contacts: [],
      selectedContact: null,
      searchQuery: '',
      apiurl: "http://localhost:3000/offline",
      defaultImage: defaultImage,
      showAddContactModal: false,
      showEditContactModal: false,
      newContact: {
        Nombres: '',
        ApellidoPaterno: '',
        ApellidoMaterno: '',
        FechaNacimiento: '',
        Alias: '',
        phone_numbers: [{ key: '', value: '' }],
        emails: [''],
        addresses: ['']
      },
      editContactData: {
        ID: null,
        Nombres: '',
        ApellidoPaterno: '',
        ApellidoMaterno: '',
        FechaNacimiento: '',
        Alias: '',
        phone_numbers: [{ key: '', value: '' }],
        emails: [''],
        addresses: [''],
      },
    };
  },
  /* Fetch contact information*/
  created() {
    this.fetchContacts();
  },
  computed: {
    filteredContacts() {
      if (!this.searchQuery) {
        return this.contacts;
      }
      return this.contacts.filter(contact => 
        contact.contact_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    /* Gets the information of the contacts from the api endpoints */
    async fetchContacts() {
      try {
        const response = await axios.get(`${this.apiurl}/get_contacts`);
        this.contacts = response.data;
      } catch (error) {
        console.error("Error fetching contacts:", error);
      }
    },
    async fetchPersonalInfo(contactId) {
      try {
        const response = await axios.get(`${this.apiurl}/personal_info`, {
          params: {
            id: contactId
          }
        });
        this.selectedContact = response.data;
      } catch (error) {
        console.error("Error fetching personal info:", error);
      }
    },
    closePersonalInfo() {
      this.selectedContact = null;
    },

    /* Gets the image from the path and handle uploading from the api */
    getContactImagePath(imgName) {
      if (!imgName) {
        return this.defaultImage;
      }
      try {
        return require(`@/image_bucket/${imgName}`);
      } catch (error) {
        console.error("Error loading image:", error);
        return this.defaultImage;
      }
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    async uploadNewImage(event) {
      const file = event.target.files[0];
      if (!file) return;

      let formData = new FormData();
      formData.append('image', file);
      formData.append('contactId', this.selectedContact.ID);

      axios.post(`${this.apiurl}/upload_image`, formData)
        .then(response => {
          this.selectedContact.Fotografia_path = response.data.filePath;
        })
        .catch(error => {
          console.error("Error uploading image:", error);
        });
      const response1 = await axios.get(`${this.apiurl}/get_contacts`);
      this.contacts = response1.data;
      this.closePersonalInfo()
    },

    /* Methods that handle open and close models */
    openAddContactModal() {
      this.showAddContactModal = true;
    },
    openEditContactModal() {
      this.prefillEditContactForm();
      this.showEditContactModal = true;
    },
    closeAddContactModal() {
      this.showAddContactModal = false;
      this.resetNewContactForm();
    },
    closeEditContactModal() {
      this.showEditContactModal = false;
    },

    /* Reset of informstion for not overlapping */
    resetNewContactForm() {
      this.newContact = {
        Nombres: '',
        ApellidoPaterno: '',
        ApellidoMaterno: '',
        FechaNacimiento: '',
        Alias: '',
        phone_numbers: [{ key: '', value: '' }],
        emails: [''],
        addresses: ['']
      };
    },

    /* Prefill method to gets the information from the selected contact to the edit section */
    prefillEditContactForm() {
      const phoneNumbers = this.selectedContact.phone_numbers ? this.selectedContact.phone_numbers.split(',').map(num => num.trim()) : [];
      const phoneTypes = this.selectedContact.phone_type ? this.selectedContact.phone_type.split(',').map(type => type.trim()) : [];

      const phoneDetails = phoneNumbers.map((number, index) => ({
        key: phoneTypes[index] || '',
        value: number || ''
      }));

      const fechaNacimiento = this.selectedContact.FechaNacimiento ? this.selectedContact.FechaNacimiento.split('/').reverse().join('-') : '';

      this.editContactData = {
        ID: this.selectedContact.ID,
        Nombres: this.selectedContact.Nombres || '',
        ApellidoPaterno: this.selectedContact.ApellidoPaterno || '',
        ApellidoMaterno: this.selectedContact.ApellidoMaterno || '',
        FechaNacimiento: fechaNacimiento,
        Alias: this.selectedContact.Alias || '',
        phone_numbers: phoneDetails,
        emails: this.selectedContact.emails ? this.selectedContact.emails.split(',').map(email => email.trim()) : [''],
        addresses: this.selectedContact.addresses ? this.selectedContact.addresses.split(';').map(address => address.trim()) : [''],
      };
    },

    /* Methods that handle the add and edit sections buttons to add and remove phone numbers, emails and address */
    addPhone() {
      this.newContact.phone_numbers.push({ key: '', value: '' });
    },
    removePhone(index) {
      this.newContact.phone_numbers.splice(index, 1);
    },
    updatePhoneKey(index, value) {
      this.newContact.phone_numbers[index].key = value;
    },
    updatePhoneValue(index, value) {
      this.newContact.phone_numbers[index].value = value;
    },
    addEmail() {
      this.newContact.emails.push('');
    },
    removeEmail(index) {
      this.newContact.emails.splice(index, 1);
    },
    updateEmail(index, value) {
      this.newContact.emails.splice(index, 1, value);
    },
    addAddress() {
      this.newContact.addresses.push('');
    },
    removeAddress(index) {
      this.newContact.addresses.splice(index, 1);
    },
    updateAddress(index, value) {
      this.newContact.addresses.splice(index, 1, value);
    },
    addEditPhone() {
      this.editContactData.phone_numbers.push({ key: '', value: '' });
    },
    removeEditPhone(index) {
      this.editContactData.phone_numbers.splice(index, 1);
    },
    updateEditPhoneKey(index, value) {
      this.editContactData.phone_numbers[index].key = value;
    },
    updateEditPhoneValue(index, value) {
      this.editContactData.phone_numbers[index].value = value;
    },
    addEditEmail() {
      this.editContactData.emails.push('');
    },
    removeEditEmail(index) {
      this.editContactData.emails.splice(index, 1);
    },
    updateEditEmail(index, value) {
      this.editContactData.emails.splice(index, 1, value);
    },
    addEditAddress() {
      this.editContactData.addresses.push('');
    },
    removeEditAddress(index) {
      this.editContactData.addresses.splice(index, 1);
    },
    updateEditAddress(index, value) {
      this.editContactData.addresses.splice(index, 1, value);
    },
    getPhoneDetails(contact) {
      const phoneTypes = (contact.phone_type || '').split(',').map(type => type.trim());
      const phoneNumbers = (contact.phone_numbers || '').split(',').map(number => number.trim());
      return phoneNumbers.map((number, index) => ({
        number: number || 'N/A',
        type: phoneTypes[index] || 'N/A'
      }));
    },

    /* Method that sends to the backend the new contact data */
    async addNewContact() {
      try {

        const newContactData = {
          Nombres: this.newContact.Nombres,
          ApellidoPaterno: this.newContact.ApellidoPaterno,
          ApellidoMaterno: this.newContact.ApellidoMaterno,
          FechaNacimiento: this.newContact.FechaNacimiento,
          Alias: this.newContact.Alias,
          phone_numbers: this.newContact.phone_numbers,
          emails: this.newContact.emails,
          addresses: this.newContact.addresses,
        };

        const response = await fetch(`${this.apiurl}/new_contact`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newContactData)
        });

        const data = await response.json();
        this.contacts.push(data);
        this.closeAddContactModal();

      } catch (error) {
        console.error("Error adding new contact:", error);
      }
      const response1 = await axios.get(`${this.apiurl}/get_contacts`);
      this.contacts = response1.data;
    },

    /* Method that sent the edit contact data */
    async editContact() {
      try {

        const newContactData = {
          id: this.editContactData.ID,
          Nombres: this.editContactData.Nombres,
          ApellidoPaterno: this.editContactData.ApellidoPaterno,
          ApellidoMaterno: this.editContactData.ApellidoMaterno,
          FechaNacimiento: this.editContactData.FechaNacimiento,
          Alias: this.editContactData.Alias,
          phone_numbers: this.editContactData.phone_numbers,
          emails: this.editContactData.emails,
          addresses: this.editContactData.addresses,
        };

        const response = await fetch(`${this.apiurl}/edit_contact`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newContactData)
        });

        const data = await response.json();
        this.contacts.push(data);
        this.closeEditContactModal();
        this.closePersonalInfo()

      } catch (error) {
        console.error("Error editing contact:", error);
      }
      const response1 = await axios.get(`${this.apiurl}/get_contacts`);
      this.contacts = response1.data;
    },
    async deleteContact(contactId) {
      if (confirm("Are you sure you want to delete this contact?")) {
        try {
          const response = await axios.get(`${this.apiurl}/delete_contact`, {
            params: {
              id: contactId
            }
          });
          this.selectedContact = response.data;
          this.closePersonalInfo()
        } catch (error) {
          console.error("Error fetching personal info:", error);
        }
        const response1 = await axios.get(`${this.apiurl}/get_contacts`);
        this.contacts = response1.data;
      }
    }
  }
}
</script>



<style scoped>
/* General Styles */
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
}

/* Search Bar */
.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  margin-top: 20px;
}

.search-bar input[type="text"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.search-bar button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Contact Cards */
.contacts-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  align-items: center;
}

.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 150px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
}

.contact-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
  cursor: pointer;
}

.contact-name {
  font-weight: bold;
}

/* Personal Info Section */
.personal-info {
  position: fixed;
  right: 0;
  top: 0;
  width: 300px;
  height: 100%;
  background-color: #fff;
  border-left: 1px solid #ddd;
  padding: 20px;
  overflow-y: auto;
  transform: translateX(100%);
  transition: transform 0.3s ease;
}

.personal-info-visible {
  transform: translateX(0);
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.personal-info ul {
  list-style-type: none;
  padding: 0;
}

.add-contact-modal,
.edit-contact-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); 
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; 
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px; 
  width: 90%;
  max-width: 500px; 
  max-height: 80vh; 
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
  position: relative; 
  overflow-y: auto; 
}

.modal-content h2 {
  text-align: center;
  margin-bottom: 20px; 
  font-family: 'Arial', sans-serif; 
}

.modal-content label {
  display: block;
  margin-bottom: 8px; 
  font-weight: bold; 
}

.modal-content input[type="text"],
.modal-content input[type="date"],
.modal-content input[type="file"] {
  width: 100%; 
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd; 
  border-radius: 4px; 
  box-sizing: border-box;
}

.modal-content button[type="submit"] {
  width: 100%; 
  padding: 10px;
  background-color: #007BFF;
  color: #fff; 
  border: none; 
  border-radius: 4px; 
  cursor: pointer;
  font-size: 16px; 
}

.modal-content button[type="submit"]:hover {
  background-color: #0056b3; 
}

.close-button {
  position: absolute; 
  top: 10px;
  right: 10px;
  background: none; 
  border: none; 
  font-size: 1.5em; 
  cursor: pointer;
}

.edit-button, .delete-button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.edit-button {
  background-color: #4CAF50;
  color: white;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.buttons-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.phone-entry,
.email-entry,
.address-entry {
  display: flex;
  align-items: center;
  margin-bottom: 10px; 
}

.phone-entry input,
.email-entry input,
.address-entry input {
  flex: 1; 
  margin-right: 5px;
  padding: 8px; 
  border: 1px solid #ddd; 
  border-radius: 4px; 
}

.phone-entry button,
.email-entry button,
.address-entry button {
  padding: 6px 10px; 
  background-color: #dc3545;
  color: #fff; 
  border: none; 
  border-radius: 4px; 
  cursor: pointer;
}

.phone-entry button:hover,
.email-entry button:hover,
.address-entry button:hover {
  background-color: #c82333; 
}

button[type="button"] {
  display: block;
  width: auto; 
  margin: 10px 0; 
  padding: 8px 12px; 
  background-color: #28a745; 
  color: #fff; 
  border: none; 
  border-radius: 4px; 
  cursor: pointer;
}

button[type="button"]:hover {
  background-color: #218838; 
}
</style>
