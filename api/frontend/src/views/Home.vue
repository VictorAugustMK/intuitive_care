<template>
  <div class="home">
    <h1>Bem-vindo à página inicial!</h1>
    <p>Clique no botão abaixo para acessar as operadoras:</p>
    <button @click="goToOperadoras">Ir para Operadoras</button>
    <p>Clique no botão abaixo para configurar o banco de dados:</p>
    <button @click="setupDatabase">Configurar Banco de Dados</button>
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
    // Método para navegar até a tela de operadoras
    goToOperadoras() {
      this.$router.push('/operadoras');
    },
    // Método para configurar o banco de dados
    async setupDatabase() {
      try {
        const response = await axios.post('http://localhost:5000/setup-db');
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data?.error || 'Erro ao configurar o banco de dados';
      }
    }
  }
};
</script>

<style>
@import '../style.css';  /* Importando o CSS externo */
</style>
