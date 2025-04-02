<template>
  <div class="container">
    <h2>Gastos Trimestrais</h2>
    
    <label for="ano">Filtrar por Ano:</label>
    <select v-model="anoSelecionado" @change="fetchGastosTrimestrais">
      <option value="">Todos</option>
      <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">{{ ano }}</option>
    </select>
    
    <table v-if="gastosTrimestrais.length">
      <thead>
        <tr>
          <th>EMPRESA</th>
          <th>NOME FANTASIA</th>
          <th>REGISTRO ANS</th>
          <th>DESCRIÇÃO</th>
          <th>ANO</th>
          <th>GASTOS TRIMESTRAIS</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="gasto in gastosTrimestrais" :key="gasto.id">
          <td>{{ gasto.empresa }}</td>
          <td>{{ gasto.nome_fantasia }}</td>
          <td>{{ gasto.registro_ans }}</td>
          <td>{{ gasto.descricao }}</td>
          <td>{{ gasto.ano }}</td>
          <td>{{ gasto.gastos_trimestrais }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Nenhum dado encontrado.</p>
    
    <div class="pagination">
      <button @click="pagina--" :disabled="pagina <= 1">Anterior</button>
      <span>Página {{ pagina }} de {{ totalPaginas }}</span>
      <button @click="pagina++" :disabled="pagina >= totalPaginas">Próxima</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GastosTrimestrais',
  data() {
    return {
      gastosTrimestrais: [],
      anosDisponiveis: [],
      anoSelecionado: '',
      pagina: 1,
      totalPaginas: 1
    };
  },
  mounted() {
    this.fetchAnosDisponiveis();
    this.fetchGastosTrimestrais();
  },
  methods: {
    async fetchGastosTrimestrais() {
      try {
        const response = await axios.get('http://localhost:5000/gastos_trimestrais', {
          params: {
            ano: this.anoSelecionado,
            page: this.pagina
          }
        });
        this.gastosTrimestrais = response.data.gastos_trimestrais;
        this.totalPaginas = response.data.totalPages;
      } catch (error) {
        console.error('Erro ao buscar os gastos trimestrais:', error);
      }
    },
    async fetchAnosDisponiveis() {
      try {
        const response = await axios.get("http://localhost:5000/anos_gastos_trimestrais");
        this.anosDisponiveis = response.data.anos;
      } catch (error) {
        console.error('Erro ao buscar os anos disponíveis:', error);
      }
    }
  }
};
</script>

<style>
@import '../style.css';

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination button {
  margin: 0 5px;
}
</style>