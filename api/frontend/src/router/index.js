import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Sobre from '../views/Sobre.vue';
import Operadoras from '../components/Operadoras.vue';
import GastosAnuais from '../components/GastosAnuais.vue';
import GastosTrimestrais from '../components/GastosTrimestrais.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/sobre', component: Sobre },
  { path: '/operadoras', component: Operadoras },
  { path: "/gastos-anuais", name: "GastosAnuais", component: GastosAnuais },
  { path: "/gastos-trimestrais", name: "GastosTrimestrais", component: GastosTrimestrais }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
