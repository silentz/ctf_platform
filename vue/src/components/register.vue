<template>
    <div class="ctf-auth">
        <div class='centered'>
            <h3>Регистрация</h3>
            <div class='error' v-show="showError">Error: {{ error }}</div>
            <form @submit.prevent="handleSubmit">
                <input size="40" v-model='username' type='text' required placeholder="Логин">
                <input size="40" v-model='full_name' type='text' required placeholder="ФИО">
                <input size="40" v-model='password' type='password' required placeholder="Пароль">
                <input size="40" v-model='repeatPassword' type='password' required placeholder="Повторите пароль">
                <button>Подтвердить</button>
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
            full_name: '',
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
                password: this.password,
                full_name: this.full_name
            }).then(response => {
                this.username = ""
                this.password = ""
                this.full_name = ""
                this.$router.push('/')
            }).catch(err => {
                this.printError('This username is already taken!')
            })
        }
    }
}
</script>

<style lang='scss'>
@import '../assets/style/auth.scss';
</style>
