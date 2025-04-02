<template>
  <div class="operadoras">
    <h1>Lista de Operadoras</h1>

    <!-- Campo de busca -->
    <input v-model="searchTerm" type="text" placeholder="Buscar por operadora..." />

    <!-- Botão de busca -->
    <button @click="searchOperadoras">Buscar</button>

    <!-- Tabela de Operadoras -->
    <table v-if="operadoras.length">
      <thead>
        <tr>
          <th>Razão Social</th>
          <th>Nome Fantasia</th>
          <th>Registro ANS</th>
          <th>CNPJ</th>
          <th>Representante</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="operadora in operadoras" :key="operadora.registro_ans">
          <td>{{ operadora.razao_social }}</td>
          <td>{{ operadora.nome_fantasia }}</td>
          <td>{{ operadora.registro_ans }}</td>
          <td>{{ operadora.cnpj }}</td>
          <td>{{ operadora.representante }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Caso não haja resultados -->
    <p v-if="operadoras.length === 0">Nenhuma operadora encontrada.</p>

    <!-- Controle de Paginação -->
    <div v-if="totalPages > 1" class="pagination">
      <button @click="changePage(1)" :disabled="page === 1">Primeira</button>
      <button @click="changePage(page - 1)" :disabled="page === 1">Anterior</button>
      
      <span>Página {{ page }} de {{ totalPages }}</span>

      <button @click="changePage(page + 1)" :disabled="page === totalPages">Próxima</button>
      <button @click="changePage(totalPages)" :disabled="page === totalPages">Última</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: "",  // Termo de busca
      operadoras: [],  // Armazenará as operadoras encontradas
      page: 1,         // Página atual
      totalPages: 1    // Total de páginas (será atualizado após a consulta)
    };
  },
  methods: {
    // Método para realizar a busca das operadoras
    async searchOperadoras() {
      try {
        const response = await fetch(`http://localhost:5000/operadoras?search=${this.searchTerm}&page=${this.page}`);
        const data = await response.json();

        this.operadoras = data.operadoras;  // Atualiza a lista de operadoras
        this.totalPages = data.total_pages; // Atualiza o número total de páginas
      } catch (error) {
        console.error("Erro ao buscar operadoras:", error);
      }
    },

    // Método para mudar de página
    changePage(newPage) {
      if (newPage > 0 && newPage <= this.totalPages) {
        this.page = newPage;
        this.searchOperadoras();  // Refazer a busca com a nova página
      }
    }
  },
  watch: {
    // Sempre que o termo de busca mudar, refazemos a busca desde a primeira página
    searchTerm(newTerm) {
      this.page = 1;
      this.searchOperadoras();
    }
  },
  mounted() {
    this.searchOperadoras();  // Carregar os dados quando a página for carregada
  }
};
</script>

<style>
@import '../style.css';  /* Importando o CSS externo */
</style>
