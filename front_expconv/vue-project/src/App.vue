<template>
  <div id="app">
    <router-view></router-view> <!-- Здесь будут отображаться компоненты в зависимости от маршрута -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* Вы можете добавить стили для общего оформления приложения */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
