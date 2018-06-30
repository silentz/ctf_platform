
<template>
    <nav class='ctf-nav'>
        <h1 class='logo'>
            <router-link :to="{ name: 'root' }">CTFPro</router-link>
        </h1>
        <ul class='list'>
            <template v-if="isAuthenticated">
                <li>
                    <a @click="logout" href="" class='link'>
                        Выйти
                    </a>
                </li>
            </template>
            <template v-else>
                <li>
                    <router-link class='link' :to="{ name: 'login' }">Вход</router-link>
                </li>
                <li>
                    <router-link class='link' :to="{ name: 'register' }">Регистрация</router-link>
                </li>
            </template>
        </ul>
    </nav>
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
.ctf-nav {
    grid-column: 1 / span 1;
    grid-row: 1 / span 1;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    background-color: #12355b;

    .logo a {
        display: inline-block;
        margin: 20px 20px;
        color: white;
        text-decoration: none;
    }

    .list {
        display: inline-block;
        list-style-type: none;
        margin: 0 10px;

        li {
            display: inline-block;

            .link {
                color: white;
                font-size: 1.1rem;
                text-decoration: none;
                margin: 0 10px;
            }

            .link-active {
                color: yellow;
            }
        }
    }
}

</style>
