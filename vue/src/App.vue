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
import PlatfromComponent, {PlatformRoutes} from './components/platform.vue'
import AdminBase, {AdminRoutes} from './components/admin/base.vue'
import ContestEdit from './components/admin/edit_contest.vue'
import VuexStore from './store.js'

let router = new VueRouter({
    mode: 'history',
    linkActiveClass: 'link-active',
    linkExactActiveClass: 'link-active',
    routes: [
        {path: '/', redirect: '/platform', name: 'root'},
        {path: '/register', component: RegisterComponent, name: 'register'},
        {path: '/login', component: LoginComponent, name: 'login'},
        {
            path: '/platform',
            component: PlatfromComponent,
            name: 'platfrom',
            children: PlatformRoutes,
            meta: {requiresAuth: true}
        },
        {
            path: '/admin',
            component: AdminBase,
            name: 'admin-root',
            meta: {requiresAuth: true},
        },
        {
            path: '/admin/edit/:id',
            component: ContestEdit,
            name: 'edit_contest',
            meta: {requiresAuth: true}
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (VuexStore.getters.isAuthenticated) {
            next()
        } else {
            next({ path: '/login' })
        }
    } else {
        next()
    }
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
@import url('https://fonts.googleapis.com/css?family=Ubuntu');

$background-color: #e1e1e1;
$global-font: 'Ubuntu', sans-serif;
$navigation-bar-height: 60px;

html {
    margin: 0;
    padding: 0;
    height: 100%;
    background-color: $background-color;
    font-family: $global-font;
}

body {
    margin: 0;
    padding: 0;
    min-height: 100%;
    height: 100%;
}

#app {
    height: 100%;
    width: 100%;
    display: grid;
    grid-template-rows: $navigation-bar-height auto;
    grid-template-columns: auto;
    grid-row-gap: 0;
    grid-column-gap: 0;
}
</style>
