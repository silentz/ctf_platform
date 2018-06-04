<template>
    <div class="ctf-login">
        <div class='ctf-centered'>
            <h3 class='ctf-login-header'>Log in</h3>
            <div class='ctf-form-error' v-show="showError">Error: {{ error }}</div>
            <form class='ctf-form' @submit.prevent="handleSubmit">
                <input class='ctf-input' size="40" v-model='username' type='text' required placeholder="Username">
                <input class='ctf-input' size="40" v-model='password' type='password' required placeholder="Password">
                <button class='ctf-form-button'>Submit</button>
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
        updateVuex() {
            axios.get("/api/auth/status/").then(response => {
                this.$store.commit('setUserStatus', response.data.status)
                this.$store.commit('setUsername', response.data.username)
            }).catch(error => {
                // pass
            })
        },
        loginUser() {
            axios.post("/api/auth/login/", {
                username: this.username,
                password: this.password
            }).then(response => {
                this.updateVuex()
                this.username = ""
                this.password = ""
                this.$router.push('/')
            }).catch(err => {
                console.log(err.response)
                this.printError('Login or password wrong!')
            })
        }
    }
}
</script>

<style lang="scss">

</style>
