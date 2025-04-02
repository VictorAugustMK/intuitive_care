<template>
  <div id="app">
    <h1>Aplicação de Operadoras</h1>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/sobre">Sobre</router-link> |
      <router-link to="/operadoras">Operadoras</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>
