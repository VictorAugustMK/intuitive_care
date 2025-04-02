<template>
  <div class="gastos-trimestral">
    <h2>Gastos Trimestrais</h2>
    
    <div class="search-fields">
      <label for="ano">Filtrar por Ano:</label>
      <select v-model="filtroAno">
        <option value="">Todos</option>
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
      </select>
      <button @click="buscarGastos(1)">Buscar</button>
    </div>
    
    <table>
      <thead>
        <tr>
          <th>Empresa</th>
          <th>Nome Fantasia</th>
          <th>Registro ANS</th>
          <th>Descrição</th>
          <th>Ano</th>
          <th>Gastos Trimestral</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="gasto in gastos" :key="gasto.registro_ans">
          <td>{{ gasto.empresa }}</td>
          <td>{{ gasto.nome_fantasia }}</td>
          <td>{{ gasto.registro_ans }}</td>
          <td>{{ gasto.descricao }}</td>
          <td>{{ gasto.ano }}</td>
          <td>{{ gasto.gastos_trimestrais }}</td>
        </tr>
      </tbody>
    </table>

    <div class="pagination">
      <button @click="mudarPagina(pagina - 1)" :disabled="pagina <= 1">Anterior</button>
      <span>Página {{ pagina }} de {{ totalPaginas }}</span>
      <button @click="mudarPagina(pagina + 1)" :disabled="pagina >= totalPaginas">Próxima</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filtroAno: "",
      gastos: [],
      anosDisponiveis: [],
      pagina: 1,
      totalPaginas: 1
    };
  },
  methods: {
    async buscarGastos(novaPagina = this.pagina) {
      try {
        this.pagina = novaPagina; // Atualiza a página atual
        this.gastos = []; // 🔥 LIMPA a lista antes de buscar novos dados 🔥

        let url = `http://localhost:5000/gastos_trimestrais?page=${this.pagina}`;
        if (this.filtroAno) {
          url += `&ano=${this.filtroAno}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        this.gastos = data.gastos_trimestrais; // Substitui os dados antigos pelos novos
        this.totalPaginas = data.totalPages; // Atualiza o total de páginas
      } catch (error) {
        console.error("Erro ao buscar os gastos trimestrais:", error);
      }
    },
    async carregarAnosDisponiveis() {
      try {
        const response = await fetch("http://localhost:5000/anos_gastos_trimestrais");
        const data = await response.json();
        this.anosDisponiveis = data.anos;
      } catch (error) {
        console.error("Erro ao carregar anos disponíveis:", error);
      }
    },
    mudarPagina(novaPagina) {
      if (novaPagina >= 1 && novaPagina <= this.totalPaginas) {
        this.buscarGastos(novaPagina); // Chama a função corretamente
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
.gastos-trimestral {
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

.pagination {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
