import * as Vue from 'vue'; // in Vue 3
import App from './App.vue';

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css';
import Button from "primevue/button";
import FileUpload from 'primevue/fileupload';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Card from 'primevue/card';
import Divider from 'primevue/divider';
import ProgressBar from 'primevue/progressbar';
import DataView from 'primevue/dataview';

import axios from 'axios';
import VueAxios from 'vue-axios';

import 'primeflex/primeflex.css';
import 'primeicons/primeicons.css';

const app = Vue.createApp(App);

app.use(VueAxios, axios);
app.use(PrimeVue);
app.component("PrimeButton", Button);
app.component('DataTable', DataTable);
app.component('DataColumn', Column);
app.component('InfoCard', Card);
app.component('InfoDivider', Divider);
app.component('ProgressBar', ProgressBar);
app.component('FileUpload', FileUpload);
app.component('DataView', DataView);
app.mount('#app');
