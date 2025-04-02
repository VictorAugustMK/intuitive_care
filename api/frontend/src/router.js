import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Sobre from './views/Sobre.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/sobre', component: Sobre }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
