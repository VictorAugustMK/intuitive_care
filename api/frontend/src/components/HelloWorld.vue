<template>
  <div>
    <h1>{{ mensagem }}</h1>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mensagem: "Carregando...",
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5000/api/mensagem") // Chama a API Flask
      .then((response) => {
        this.mensagem = response.data.mensagem;
      })
      .catch((error) => {
        console.error("Erro ao buscar dados:", error);
      });
  },
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
