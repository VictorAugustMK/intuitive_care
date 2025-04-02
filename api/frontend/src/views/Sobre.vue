<template>
  <div class="sobre">
    <h1>Sobre o Projeto</h1>
    
    <section>
      <h2>Visão Geral</h2>
      <p>
        Este projeto é uma aplicação web para consulta e análise de dados de operadoras de planos de saúde. Ele permite 
        a busca de operadoras, visualização de gastos anuais e trimestrais e a configuração automatizada do banco de dados.
      </p>
    </section>

    <section>
      <h2>Tecnologias Utilizadas</h2>
      <ul>
        <li><strong>Frontend:</strong> Vue.js</li>
        <li><strong>Backend:</strong> Flask + PostgreSQL</li>
        <li><strong>Banco de Dados:</strong> PostgreSQL</li>
        <li><strong>Estilização:</strong> CSS</li>
      </ul>
    </section>

    <section>
      <h2>Funcionalidades</h2>
      
      <h3>Página Inicial</h3>
      <ul>
        <li>Acesso à listagem de operadoras</li>
        <li>Botão para configurar o banco de dados automaticamente</li>
      </ul>

      <h3>Operadoras</h3>
      <ul>
        <li>Busca avançada por Razão Social, Nome Fantasia, Registro ANS, CNPJ e Representante</li>
        <li>Paginação para exibir resultados em blocos de 15 itens</li>
        <li>Botão "Buscar Todos"</li>
      </ul>

      <h3>Gastos Anuais</h3>
      <ul>
        <li>Tabela com Empresa, Nome Fantasia, Registro ANS, Descrição, Ano e Gastos Anuais</li>
        <li>Filtro por ano que mantém os valores disponíveis mesmo após buscas</li>
      </ul>

      <h3>Gastos Trimestrais</h3>
      <ul>
        <li>Similar à tela de gastos anuais, mas focado nos gastos por trimestre</li>
        <li>Paginação corrigida para evitar duplicação de resultados</li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: "Sobre"
};
</script>

<style scoped>
.sobre {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

h1, h2, h3 {
  color: #4CAF50;
}

p {
  line-height: 1.6;
}

ul {
  list-style: disc;
  margin-left: 20px;
}
</style>
