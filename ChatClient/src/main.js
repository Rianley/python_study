import Vue from 'vue'
import VueSocketio from 'vue-socket.io'
import Framework7 from 'framework7'
import Framework7Vue from 'framework7-vue'
import Framework7Theme from 'framework7/dist/css/framework7.ios.min.css'
import Framework7ThemeColors from 'framework7/dist/css/framework7.ios.colors.min.css'
import AppStyles from './css/app.css'
import Routes from './routes.js'
import App from './app'
Vue.use(VueSocketio, 'http://localhost:3000')
Vue.use(Framework7Vue)

new Vue({
  el: '#app',
  template: '<app/>',
  framework7: {
    root: '#app',
    routes: Routes,
  },
  components: {
    app: App
  }
});
