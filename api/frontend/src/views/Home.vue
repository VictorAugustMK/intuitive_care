<template>
  <div class="home">
    <h1>Bem-vindo à página inicial!</h1>
    
    
    <p>Clique no botão abaixo para executar o Web Scraper junto ao PDF para CSV:</p>
    <button @click="runCrawler">1 - Executar WebScraper</button>
    <button @click="transformPdfToCsv">2 - Transformar PDF em CSV</button>

    <p>Clique no botão abaixo para configurar o banco de dados:</p>
    <button @click="setupDatabase">3 - Configurar Banco de Dados</button>

    <p>Clique em um dos botões abaixo para navegar:</p>
    <div class="button-group">
      <button @click="goToOperadoras">4.1 - Ir para Operadoras</button>
      <button @click="goToGastosAnuais">4.2 -Ver Gastos Anuais</button>
      <button @click="goToGastosTrimestrais">4.3 - Ver Gastos Trimestrais</button>
    </div>

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
        const response = await axios.post('http://localhost:5000/setup_db');
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
    async transformPdfToCsv() {
      try {
        const response = await fetch("http://localhost:5000/pdf_csv", { method: "POST" });
        const data = await response.json();
        this.message = data.message || "Erro ao transformar PDF!";
      } catch (error) {
        this.message = error.response?.data?.error || 'Erro ao transformar PDF!';
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
