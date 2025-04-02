<template>
    <div class="container">
      <h2>Gastos Anuais</h2>
      <table v-if="gastosAnuais.length">
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
          <tr v-for="gasto in gastosAnuais" :key="gasto['REGISTRO ANS']">
            <td>{{ gasto["EMPRESA"] }}</td>
            <td>{{ gasto["NOME FANTASIA"] }}</td>
            <td>{{ gasto["REGISTRO ANS"] }}</td>
            <td>{{ gasto["DESCRIÇÃO"] }}</td>
            <td>{{ gasto["ANO"] }}</td>
            <td>{{ gasto["GASTOS ANUAIS"] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        gastosAnuais: [],
      };
    },
    async mounted() {
      await this.fetchGastosAnuais();
    },
    methods: {
      async fetchGastosAnuais() {
        try {
          const response = await axios.get("http://localhost:5000/gastos_anuais");
          console.log("Dados recebidos:", response.data);
          this.gastosAnuais = response.data.gastos_anuais;
        } catch (error) {
          console.error("Erro ao buscar gastos anuais:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  @import '../style.css';
  </style>
  