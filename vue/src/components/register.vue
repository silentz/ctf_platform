<template>
    <div class='ctf-register'>
        <h3>Registration</h3>
        <div class='ctf-from-error' v-show="showError">Error: {{ error }}</div>
        <form class='ctf-form' @submit.prevent="handleSubmit">
            <p>Username:</p>
            <input v-model='username' type='text' name='username'><br>
            <p>Password:</p>
            <input v-model='password' type='password' name='password'><br>
            <p>Repeat password:</p>
            <input v-model='repeatPassword' type='password' name='repeatpassword'><br><br>
            <button type='submit'>Submit</button>
        </form>
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
