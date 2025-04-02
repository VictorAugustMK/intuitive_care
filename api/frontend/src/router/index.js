import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Sobre from '../views/Sobre.vue';
import Operadoras from '../components/Operadoras.vue';  // Importando o componente Operadoras

const routes = [
  { path: '/', component: Home },
  { path: '/sobre', component: Sobre },
  { path: '/operadoras', component: Operadoras }  // Rota para a tela de operadoras
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
