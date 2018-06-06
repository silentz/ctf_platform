<template lang="html">
    <div class="ctf-platform">
        <div class="ctf-sidebar">
            <h3 class='ctf-sidebar-username'>{{ username }}</h3>
            <hr class='ctf-sidebar-delimiter'>
            <ul class='ctf-sidebar-list'>
                <li class='ctf-sidebar-list-item'>Новости</li>
                <li class='ctf-sidebar-list-item'>
                    <router-link :to="{ name: 'trainings' }">Тренировки</router-link>
                </li>
                <li class='ctf-sidebar-list-item'>
                    <router-link :to="{ name: 'contests' }">Контесты</router-link>
                </li>
                <li class='ctf-sidebar-list-item'>Личный кабинет</li>
                <li class='ctf-sidebar-list-item'>Группы</li>
                <li class='ctf-sidebar-list-item'>Скорборд</li>
            </ul>
        </div>
        <div class="ctf-screen">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import VueRouter from 'vue-router'
import TrainingComponent from './training.vue'
import ContestComponent from './contest.vue'

export let PlatformRoutes = [
    {path: 'trainings', component: TrainingComponent, name: 'trainings'},
    {path: 'contests', component: ContestComponent, name: 'contests'}
]

export default {
    name: 'Platfrom',
    computed: {
        username: function() {
            return this.$store.state.username;
        }
    }
}
</script>

<style lang="css">
</style>
