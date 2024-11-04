import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'; // Путь к вашему компоненту Login
import Register from '../components/Register.vue'; // Путь к вашему компоненту Register

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login // Компонент для маршрута "/"
  },
  {
    path: '/register',
    name: 'Register',
    component: Register // Компонент для маршрута "/register"
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
