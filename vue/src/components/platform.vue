<template lang="html">
    <div class="platform">
        <div class="sidebar">
            <h3 class='username'>{{ username }}</h3>
            <hr class='delimiter'>
            <ul class='list'>
                <li class='item'>Новости</li>
                <li class='item'>
                    <router-link class='link' :to="{ name: 'trainings' }">Тренировки</router-link>
                </li>
                <li class='item'>
                    <router-link class='link' :to="{ name: 'contests' }">Контесты</router-link>
                </li>
                <li class='item'>
                    <router-link class='link' :to="{ name: 'account' }">Личный кабинет</router-link>
                </li>
                <li class='item'>Группы</li>
                <li class='item'>Скорборд</li>
            </ul>
        </div>
        <div class="screen">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import VueRouter from 'vue-router'
import TrainingComponent from './training.vue'
import ContestComponent from './contest.vue'
import AccountComponent from './account.vue'

export let PlatformRoutes = [
    {path: 'trainings', component: TrainingComponent, name: 'trainings'},
    {path: 'contests', component: ContestComponent, name: 'contests'},
    {path: 'account', component: AccountComponent, name: 'account'}
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

<style lang="scss">

.platform {
    display: flex;
    flex-direction: row;
    align-items: stretch;

    .screen {
        flex-grow: 1;
    }

    .sidebar {
        color: white;
        background-color: #222222;
        width: 200px;
        padding: 10px;

        .username {
            text-align: center;
            margin: 15px;
        }

        .delimiter {
            border-color: #444444;
        }

        .list {
            list-style-type: none;
            padding: 0;
        }

        .item {
            background-color: #333333;
            margin: 5px 0;
            padding: 10px 10px;
            border-radius: 3px;
            font-size: 0.9rem;

            .link {
                text-decoration: none;
                color: white;
            }

            .link-active {
                color: yellow;
            }
        }
    }
}

</style>
