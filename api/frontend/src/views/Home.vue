<template>
  <div class="home">
    <h1>Bem-vindo à página inicial!</h1>
    
    <p>Clique em um dos botões abaixo para navegar:</p>
    <div class="button-group">
      <button @click="goToOperadoras">Ir para Operadoras</button>
      <button @click="goToGastosAnuais">Ver Gastos Anuais</button>
      <button @click="goToGastosTrimestrais">Ver Gastos Trimestrais</button>
    </div>

    <p>Clique no botão abaixo para configurar o banco de dados:</p>
    <button @click="setupDatabase">Configurar Banco de Dados</button>

    <p>Clique no botão abaixo para executar o Web Scraper:</p>
    <button @click="runCrawler">Executar Crawler</button>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      message: ''
    };
  },
  methods: {

    goToOperadoras() {
      this.$router.push('/operadoras');
    },

    async setupDatabase() {
      try {
        const response = await axios.post('http://localhost:5000/setup-db');
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data?.error || 'Erro ao configurar o banco de dados';
      }
    },

    async runCrawler() {
      try {
        const response = await axios.post('http://localhost:5000/download_files');
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data?.error || 'Erro ao executar o Web Scraper';
      }
    },

    goToGastosAnuais() {
      this.$router.push('/gastos-anuais');
    },

    goToGastosTrimestrais() {
      this.$router.push('/gastos-trimestrais');
    }
  }
};
</script>

<style>
@import '../style.css';


</style>
