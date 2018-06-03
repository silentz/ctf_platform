<template>
    <div id="app">
        <h1>Main page</h1>
        <hr>
        <router-view></router-view>
    </div>
</template>

<script>
import VueRouter from 'vue-router'
import RegisterComponent from './components/register.vue'

let router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/register', component: RegisterComponent}
    ]
})

export default {
    name: 'app',
    router: router,
    data () {
        return {

        }
    }
}
</script>

<style lang="scss">

</style>
