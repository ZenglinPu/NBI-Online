import Vue from 'vue';
import App from './App.vue';
import axios from 'axios';
import vueRouter from 'vue-router'
import router from '@/router/index'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.prototype.$axios = axios
Vue.config.productionTip = false

Vue.use(vueRouter)
Vue.use(ElementUI);

new Vue({
  el: "#root",
  components: {App},
  render: h => h(App),
  // 组件通信的组件实例
  beforeCreate() {
    Vue.prototype.$bus = this;
  },
  router:router,
});
