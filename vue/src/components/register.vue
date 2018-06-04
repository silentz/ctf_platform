<template>
    <div class="ctf-login">
        <div class='ctf-centered'>
            <h3 class='ctf-login-header'>Sign up</h3>
            <div class='ctf-form-error' v-show="showError">Error: {{ error }}</div>
            <form class='ctf-form' @submit.prevent="handleSubmit">
                <input class='ctf-input' size="40" v-model='username' type='text' required placeholder="Username">
                <input class='ctf-input' size="40" v-model='password' type='password' required placeholder="Password">
                <input class='ctf-input' size="40" v-model='repeatPassword' type='password' required placeholder="Repeat password">
                <button class='ctf-form-button'>Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'register',
    data: function () {
        return {
            username: '',
            password: '',
            repeatPassword: '',
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
            if (this.repeatPassword != this.password) {
                this.printError("Passwords are not equal!")
            } else {
                this.disableError()
                this.registerUser()
            }
        },
        registerUser() {
            axios.post("/api/auth/register/", {
                username: this.username,
                password: this.password
            }).then(response => {
                this.username = ""
                this.password = ""
                this.$router.push('/')
            }).catch(err => {
                this.printError('This username is already taken!')
            })
        }
    }
}
</script>

<style lang='scss'>

</style>
