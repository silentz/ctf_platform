import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import App from './App.vue'
import axios from 'axios'

Vue.use(VueRouter)
Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        username: "",
        user_status: "anonymous",
    },
    mutations: {
        setUserStatus(state, status) {
            state.user_status = status
        },
        setUsername(state, username) {
            state.username = username
        }
    },
    getters: {
        isAnonymous: state => {
            return state.user_status === "anonymous"
        },
        isDefaultUser: state => {
            return state.user_status === "user"
        },
        isAdmin: state => {
            return state.user_status === "admin"
        }
    }
})

new Vue({
    el: '#app',
    store: store,
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
