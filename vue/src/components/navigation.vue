
<template>
    <header>
        <nav class='ctf-nav'>
            <h1 class='ctf-nav-logo'>CTFPro</h1>
            <ul class='ctf-nav-list'>
                <template v-if="isAuthenticated">
                    <li class='ctf-nav-list-item'>
                        <a @click="logout" href="" class='ctf-nav-link'>
                            Logout
                        </a>
                    </li>
                </template>
                <template v-else>
                    <li class='ctf-nav-list-elem'>
                        <router-link :to="{ name: 'login' }">Log in</router-link>
                    </li>
                    <li class='ctf-nav-list-elem'>
                        <router-link :to="{ name: 'register' }">Sign up</router-link>
                    </li>
                </template>
            </ul>
        </nav>
    </header>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Navigation',
    computed: {
        isAuthenticated: function() {
            return this.$store.getters.isAuthenticated;
        }
    },
    methods: {
        updateVuex() {
            axios.get("/api/auth/status/").then(response => {
                this.$store.commit('setUserStatus', response.data.status)
                this.$store.commit('setUsername', response.data.username)
            }).catch(error => {
                // pass
            })
        },
        logout() {
            axios.get('/api/auth/logout/').then(response => {
                this.updateVuex()
                this.$router.push('/')
            }).catch(err => {
                this.updateVuex()
                this.$router.push('/')
            })
        }
    }
}
</script>

<style lang="scss">

</style>
