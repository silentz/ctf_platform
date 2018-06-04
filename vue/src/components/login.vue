<template>
    <div class="ctf-login">
        <h3>Log in</h3>
        <div class='ctf-form-error' v-show="showError">Error: {{ error }}</div>
        <form class='ctf-form' @submit.prevent="handleSubmit">
            <p>Username:</p>
            <input v-model='username' type='text' name='username' required><br>
            <p>Password:</p>
            <input v-model='password' type='password' name='password' required><br>
            <button type='submit'>Submit</button>
        </form>
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
