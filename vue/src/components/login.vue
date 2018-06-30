<template>
    <div class="ctf-auth">
        <div class='centered'>
            <h3>Вход</h3>
            <div class='error' v-show="showError">Error: {{ error }}</div>
            <form @submit.prevent="handleSubmit">
                <input size="40" v-model='username' type='text' required placeholder="Логин">
                <input size="40" v-model='password' type='password' required placeholder="Пароль">
                <button>Подтвердить</button>
            </form>
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'login',
    data: function () {
        return {
            username: '',
            password: '',
            showError: false,
            error: ''
        }
    },
    methods: {
        printError(text) {
            this.error = text
            this.showError = true
        },
        disableError() {
            this.showError = false
        },
        handleSubmit() {
            this.disableError()
            this.loginUser()
        },
        updateVuexAndRedirect() {
            axios.get("/api/auth/status/").then(response => {
                this.$store.commit('setUserStatus', response.data.status)
                this.$store.commit('setUsername', response.data.username)
                this.$router.push('/')
            }).catch(error => {
                this.$router.push('/')
            })
        },
        loginUser() {
            axios.post("/api/auth/login/", {
                username: this.username,
                password: this.password
            }).then(response => {
                this.username = ""
                this.password = ""
                this.updateVuexAndRedirect()
            }).catch(err => {
                this.printError('Login or password wrong!')
            })
        }
    }
}
</script>

<style lang="scss">
@import '../assets/style/auth.scss';
</style>
