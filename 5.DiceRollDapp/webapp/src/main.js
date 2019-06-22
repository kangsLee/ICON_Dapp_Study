// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import routes from "./routes";
import { store } from "./store";

const NotFound = { template: "<p>Page not found</p>" };

// import VueFire from 'vuefire';
// Vue.use(VueFire);

/* eslint-disable no-new */

new Vue({
  el: "#app",
  data: {
    currentRoute: window.location.pathname
  },
  store,
  computed: {
    ViewComponent() {
      return routes[this.currentRoute] || NotFound;
    }
  },
  beforeCreate() {
    this.$store.commit("initialiseStore");
  },
  render(h) {
    return h(this.ViewComponent);
  }
});

window.addEventListener("popstate", () => {
  app.currentRoute = window.location.pathname;
});
