<template>
  <div class="gastos-anuais">
    <h2>Gastos Anuais</h2>
    
    <div class="search-fields">
      <label for="ano">Filtrar por Ano:</label>
      <select v-model="filtroAno">
        <option value="">Todos</option>
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
      </select>
      <button @click="buscarGastos">Buscar</button>
    </div>
    
    <table>
      <thead>
        <tr>
          <th>Empresa</th>
          <th>Nome Fantasia</th>
          <th>Registro ANS</th>
          <th>Descrição</th>
          <th>Ano</th>
          <th>Gastos Anuais</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="gasto in gastos" :key="gasto.registro_ans">
          <td>{{ gasto.EMPRESA }}</td>
          <td>{{ gasto['NOME FANTASIA'] }}</td>
          <td>{{ gasto['REGISTRO ANS'] }}</td>
          <td>{{ gasto.DESCRIÇÃO }}</td>
          <td>{{ gasto.ANO }}</td>
          <td>{{ gasto['GASTOS ANUAIS'] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filtroAno: "",
      gastos: [],
      anosDisponiveis: []
    };
  },
  methods: {
    async buscarGastos() {
      try {
        let url = "http://localhost:5000/gastos_anuais";
        if (this.filtroAno) {
          url += `?ano=${this.filtroAno}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        this.gastos = data.gastos_anuais;
      } catch (error) {
        console.error("Erro ao buscar os gastos anuais:", error);
      }
    },

    async carregarAnosDisponiveis() {
      try {
        const response = await fetch("http://localhost:5000/gastos_anuais");
        const data = await response.json();
        
        // Extrai os anos únicos da tabela sem afetar os dados de busca
        this.anosDisponiveis = [...new Set(data.gastos_anuais.map(gasto => gasto.ANO))].sort();
      } catch (error) {
        console.error("Erro ao carregar anos disponíveis:", error);
      }
    }
},

mounted() {
    this.carregarAnosDisponiveis();
    this.buscarGastos();
}

};
</script>

<style scoped>
.gastos-anuais {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin-top: 40px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.search-fields {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  font-size: 16px;
  border-radius: 10px;
  border: 1px solid #ccc;
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

table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #535bf2;
  color: white;
}

</style>
