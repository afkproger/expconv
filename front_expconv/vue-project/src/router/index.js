import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'; // Путь к вашему компоненту Login
import Register from '../components/Register.vue'; // Путь к вашему компоненту Register
import Tasks from '@/components/Tasks.vue';
import TaskSettings from '@/components/TaskSettings.vue';

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
  } , 
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks
  },
  {
    path: '/settings',
    name: 'TaskSettings',
    component: TaskSettings
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
