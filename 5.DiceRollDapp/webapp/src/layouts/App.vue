<template>
  <div id="app">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {
  }
};
</script>

<style lang="scss" scoped>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;

  padding: 0 8px;
}
</style>
