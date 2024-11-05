import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'; 
import Register from '../components/Register.vue'; 
import Tasks from '@/components/Tasks.vue';
import TaskSettings from '@/components/TaskSettings.vue';
import Questionnaire from '@/components/Questionnaire.vue'; // Импортируйте компонент опроса

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks
  },
  {
    path: '/settings',
    name: 'TaskSettings',
    component: TaskSettings
  },
  {
    path: '/questionnaire/:id', // Убедитесь, что здесь правильный путь
    name: 'Questionnaire',
    component: Questionnaire
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
