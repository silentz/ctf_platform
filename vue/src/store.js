import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
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
        isAuthenticated: state => {
                return state.user_status != "anonymous"
        },
        isDefaultUser: state => {
            return state.user_status === "user"
        },
        isAdmin: state => {
            return state.user_status === "admin"
        }
    }
})
