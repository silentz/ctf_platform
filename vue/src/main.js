import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VModal from 'vue-js-modal'
import {Tabs, Tab} from 'vue-tabs-component'
import App from './App.vue'
import axios from 'axios'
import VuexStore from './store.js'

Vue.use(VueRouter)
Vue.use(VModal)
Vue.component('tabs', Tabs)
Vue.component('tab', Tab)

axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

new Vue({
    el: '#app',
    store: VuexStore,
    render: h => h(App),
    created: function() {
        axios.get("/api/auth/status/").then(response => {
            this.$store.commit('setUserStatus', response.data.status)
            this.$store.commit('setUsername', response.data.username)
        }).catch(error => {
            // pass
        })
    }
})
