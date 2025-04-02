<template>
  <div class="operadoras">
    <h1>Lista de Operadoras</h1>

    <!-- Campos de busca -->
    <div class="search-fields">
      <input v-model="searchTerm.razao_social" type="text" placeholder="Buscar por Razão Social" />
      <input v-model="searchTerm.nome_fantasia" type="text" placeholder="Buscar por Nome Fantasia" />
      <input v-model="searchTerm.registro_ans" type="text" placeholder="Buscar por Registro ANS" />
      <input v-model="searchTerm.cnpj" type="text" placeholder="Buscar por CNPJ" />
      <input v-model="searchTerm.representante" type="text" placeholder="Buscar por Representante" />

      <!-- Botões de busca -->
      <button @click="searchOperadoras">Buscar</button>
      <button @click="searchAll">Buscar Todos</button>
      <button @click="clearSearch">Limpar Busca</button> <!-- Novo botão -->
    </div>

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

    <!-- Paginação -->
    <div class="pagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1">Anterior</button>
      <span>{{ currentPage }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage * 15 >= totalItems">Próximo</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: {
        razao_social: "",
        nome_fantasia: "",
        registro_ans: "",
        cnpj: "",
        representante: "",
      },
      operadoras: [],
      currentPage: 1,
      totalItems: 0,
    };
  },
  methods: {
    // Busca as operadoras com filtros
    async searchOperadoras() {
      try {
        const params = new URLSearchParams();
        for (const key in this.searchTerm) {
          if (this.searchTerm[key]) {
            params.append(key, this.searchTerm[key]);
          }
        }
        params.append("page", this.currentPage);
        const response = await fetch(`http://localhost:5000/operadoras?${params.toString()}`);
        const data = await response.json();
        this.operadoras = data.operadoras;
        this.totalItems = data.totalCount;
      } catch (error) {
        console.error("Erro ao buscar operadoras:", error);
      }
    },

    // Busca todas as operadoras sem filtros
    async searchAll() {
      this.clearSearch(); // Reseta os filtros antes de buscar todas
      this.searchOperadoras();
    },

    // Limpa os campos de busca e recarrega todas as operadoras
    clearSearch() {
      this.searchTerm = {
        razao_social: "",
        nome_fantasia: "",
        registro_ans: "",
        cnpj: "",
        representante: "",
      };
      this.currentPage = 1;
      this.searchOperadoras();
    },

    // Troca de página
    changePage(page) {
      if (page >= 1 && page <= Math.ceil(this.totalItems / 15)) {
        this.currentPage = page;
        this.searchOperadoras();
      }
    }
  },

  mounted() {
    this.searchOperadoras();
  }
};
</script>

<style>
@import '../style.css'; /* Importando o CSS externo */
</style>
