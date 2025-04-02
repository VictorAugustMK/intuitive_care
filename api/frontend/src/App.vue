<template>
  <div>
    <button @click="executarScript">Executar Script Python</button>
    <p v-if="output">Resultado: {{ output }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      output: null,
    };
  },
  methods: {
    executarScript() {
      axios
        .get("http://127.0.0.1:5000/api/download")
        .then((response) => {
          if (response.data.status === "Sucesso") {
            this.output = response.data.output;
          } else {
            this.output = `Erro: ${response.data.output}`;
          }
        })
        .catch((error) => {
          this.output = `Erro: ${error.message}`;
        });
    },
  },
};
</script>
