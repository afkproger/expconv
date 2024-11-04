// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Импортируйте маршрутизатор

const app = createApp(App);
app.use(router); // Подключите маршрутизатор
app.mount('#app');
