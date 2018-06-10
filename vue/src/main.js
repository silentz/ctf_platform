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
        // need SYNCHRONOUS request to set status
        // axios doesn't let to do them :D
        let xhr = new XMLHttpRequest()
        xhr.open('GET', '/api/auth/status/', false)
        xhr.send()
        if (xhr.status == 200) {
            let data = JSON.parse(xhr.responseText)
            this.$store.commit('setUserStatus', data.status)
            this.$store.commit('setUsername', data.username)
        }
    }
})
