<template>
    <div id="app">
        <NavComponent></NavComponent>
        <router-view></router-view>
    </div>
</template>

<script>
import VueRouter from 'vue-router'
import RegisterComponent from './components/register.vue'
import LoginComponent from './components/login.vue'
import NavComponent from './components/navigation.vue'

let router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/register', component: RegisterComponent, name: 'register'},
        {path: '/login', component: LoginComponent, name: 'login'}
    ]
})

export default {
    name: 'app',
    router: router,
    components: {
        'NavComponent': NavComponent
    },
    data () {
        return {

        }
    }
}
</script>

<style lang="scss">

</style>
