<template lang="html">
    <div class="platform">
        <div class="sidebar" v-if='visible'>
            <div @click='visible=false' class='hide-button'>&#9776;</div>
            <div class='inner'>
                <h3 class='username'>{{ username }}</h3>
                <hr class='delimiter'>
                <ul class='list'>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'news' }">Новости</router-link>
                    </li>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'trainings' }">Тренировки</router-link>
                    </li>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'contests' }">Контесты</router-link>
                    </li>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'account' }">Личный кабинет</router-link>
                    </li>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'groups' }">Группы</router-link>
                    </li>
                    <li class='item'>
                        <router-link class='link' :to="{ name: 'scoreboard' }">Скорборд</router-link>
                    </li>
                    <li class='item' v-if='isAdmin'>
                        <router-link class='link' :to="{ name: 'admin-root'}">Администрирование</router-link>
                    </li>
                </ul>
            </div>
        </div>
        <div class='hidden-sidebar' v-else>
            <div @click='visible=true' class='hide-button'>&#9776;</div>
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
import ContestDetailComponent from './contest_detail.vue'
import ScoreboardComponent from './scoreboard.vue'
import NewsComponent from './news.vue'
import GroupsComponent from './groups.vue'
import AdminBase, {AdminRoutes} from './admin/base.vue'
import ContestEdit from './admin/edit_contest.vue'
import TaskEdit from './admin/edit_task.vue'

export let PlatformRoutes = [
    {path: 'trainings', component: TrainingComponent, name: 'trainings'},
    {path: 'contests', component: ContestComponent, name: 'contests'},
    {path: 'contest/:id', component: ContestDetailComponent, name: 'contest_detail'},
    {path: 'account', component: AccountComponent, name: 'account'},
    {path: 'scoreboard', component: ScoreboardComponent, name: 'scoreboard'},
    {path: 'news', component: NewsComponent, name: 'news'},
    {path: 'groups', component: GroupsComponent, name: 'groups'},
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
    },
    {
        path: '/admin/edit-task/:id',
        component: TaskEdit,
        name: 'edit_task',
        meta: {requiresAuth: true}
    }
]

export default {
    name: 'Platfrom',
    computed: {
        username: function() {
            return this.$store.state.username;
        },
        isAdmin: function() {
            return this.$store.getters.isAdmin;
        }
    },
    data: function() {
        return {
            visible: true
        }
    }
}
</script>

<style lang="scss">

$sidebar-width: 250px;
$sidebar-hidden-width: 40px;

.platform {
    display: flex;
    flex-direction: row;
    align-items: stretch;

    .screen {
        flex-grow: 1;
    }

    .hide-button {
        display: block;
        color: white;
        font-size: 1.5rem;
        text-align: center;
        margin-top: 5px;
        user-select: none;
        cursor: pointer;
    }

    .hidden-sidebar {
        background-color: #222222;
        min-width: $sidebar-hidden-width;
    }

    .sidebar {
        color: white;
        background-color: #222222;
        min-width: $sidebar-width;
        padding: 0;
        box-sizing: border-box;

        .hide-button {
            position: relative;
            top: 0;
            right: 5px;
            float: right;
        }
        .inner {
            padding: 10px;

            .username {
                text-align: center;
                margin: 15px;
            }

            .delimiter {
                border-color: #444444;
                margin-top: 10px;
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
                    user-select: none;
                }

                .link-active {
                    color: yellow;
                }
            }
        }
    }
}

</style>
