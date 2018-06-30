import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        full_name: "",
        username: "",
        user_status: "anonymous",
    },
    mutations: {
        setUserStatus(state, status) {
            state.user_status = status
        },
        setUsername(state, username) {
            state.username = username
        },
        setFullName(state, full_name) {
            state.full_name = full_name
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
