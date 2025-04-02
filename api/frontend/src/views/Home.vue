<template>
  <div class="home">
    <h1>Bem-vindo à página inicial!</h1>
    <p>Clique no botão abaixo para acessar as operadoras:</p>
    <button @click="goToOperadoras">Ir para Operadoras</button>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    // Método para navegar até a tela de operadoras
    goToOperadoras() {
      this.$router.push('/operadoras'); // certo e operadoras
    }
  }
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #45a049;
}
</style>
