<template>
  <div>
    <h1>{{ mensagem }}</h1>
    <p>{{ descricao }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      mensagem: "Carregando mensagem...",
      descricao: "Carregando descrição...",
    };
  },
  mounted() {
    axios
      .get("http://127.0.0.1:5000/api/mensagem")
      .then((response) => {
        this.mensagem = response.data.mensagem;
      })
      .catch((error) => {
        console.error("Erro ao buscar mensagem:", error);
      });

    axios
      .get("http://127.0.0.1:5000/api/sobre")
      .then((response) => {
        this.descricao = response.data.sobre;
      })
      .catch((error) => {
        console.error("Erro ao buscar sobre:", error);
      });
  },
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
