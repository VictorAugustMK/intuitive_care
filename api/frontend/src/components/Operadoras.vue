<template>
  <div>
    <h1>Lista de Operadoras</h1>
    <div>
      <label for="razaoSocial">Razão Social:</label>
      <input v-model="filtros.razao_social" id="razaoSocial" type="text" />
      
      <label for="nomeFantasia">Nome Fantasia:</label>
      <input v-model="filtros.nome_fantasia" id="nomeFantasia" type="text" />
      
      <label for="registroAns">Registro ANS:</label>
      <input v-model="filtros.registro_ans" id="registroAns" type="text" />
      
      <label for="cnpj">CNPJ:</label>
      <input v-model="filtros.cnpj" id="cnpj" type="text" />
      
      <label for="representante">Representante:</label>
      <input v-model="filtros.representante" id="representante" type="text" />
      
      <button @click="buscarOperadoras">Buscar</button>
      <button @click="buscarTodasOperadoras">Buscar Todos</button>
      <button @click="limparCampos">Limpar Campos</button>
    </div>
    
    <table>
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
    
    <div>
      <button @click="mudarPagina(pagina - 1)" :disabled="pagina <= 1">Anterior</button>
      <span>Página {{ pagina }} de {{ totalPaginas }}</span>
      <button @click="mudarPagina(pagina + 1)" :disabled="pagina >= totalPaginas">Próxima</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      operadoras: [],
      filtros: {
        razao_social: '',
        nome_fantasia: '',
        registro_ans: '',
        cnpj: '',
        representante: ''
      },
      pagina: 1,
      totalPaginas: 1
    };
  },
  methods: {
    async buscarOperadoras() {
      this.pagina = 1;
      await this.carregarOperadoras();
    },
    async buscarTodasOperadoras() {
      this.filtros = { razao_social: '', nome_fantasia: '', registro_ans: '', cnpj: '', representante: '' };
      this.pagina = 1;
      await this.carregarOperadoras();
    },
    limparCampos() {
      this.filtros = { razao_social: '', nome_fantasia: '', registro_ans: '', cnpj: '', representante: '' };
    },
    async carregarOperadoras() {
      try {
        const params = { ...this.filtros, page: this.pagina };
        const response = await axios.get('http://127.0.0.1:5000/operadoras', { params });
        this.operadoras = response.data.operadoras;
        this.totalPaginas = response.data.totalPages;
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error);
      }
    },
    mudarPagina(novaPagina) {
      if (novaPagina >= 1 && novaPagina <= this.totalPaginas) {
        this.pagina = novaPagina;
        this.carregarOperadoras();
      }
    }
  },
  created() {
    this.carregarOperadoras();
  }
};
</script>

<style>
@import '../style.css'; /* Importando o CSS externo */
</style>
