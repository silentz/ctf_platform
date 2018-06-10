<template lang="html">
    <div class="contest">
        <h2 class='contest-name'>{{ contest.name }}</h2>
        <tabs>
            <tab name="Таски">
                <transition-group name='tasks' tag='div' class='board'>
                    <task v-for="task in tasks" :task="task" :key="task.id"></task>
                </transition-group>
            </tab>
            <tab name='Скорборд'>
                <contest-scoreboard></contest-scoreboard>
            </tab>
            <tab name='Уведомления'>
                <notifications></notifications>
            </tab>
        </tabs>
    </div>
</template>

<script>
import axios from 'axios'
import TaskComponent from './task.vue'
import ScoreboardContestComponent from './contest_scoreboard.vue'
import NotificationsComponent from './notifications.vue'

export default {
    name: "ContestDetail",
    components: {
        task: TaskComponent,
        'contest-scoreboard': ScoreboardContestComponent,
        notifications: NotificationsComponent
    },
    data: function() {
        return {
            contest: "",
            tasks: [],
            task: {}
        }
    },
    created: function() {
        axios.get(`/api/contests/${this.$route.params.id}/`).then(response => {
            this.contest = response.data
            for (let index in this.contest.tasks) {
                let task_id = this.contest.tasks[index]
                axios.get(`/api/tasks/${task_id}/`).then(response => {
                    this.tasks.push(response.data)
                })
            }
        })
    },
    methods: {
        showTask(task_id) {
            axios.get(`/api/tasks/${task_id}/`).then(response => {
                this.task = response.data
            })
        }
    }
}
</script>

<style lang="scss">

.tabs-component {
    .tabs-component-panels {
        background-color: #fff;
        border: solid 1px #ddd;
        padding: 40px;
    }

    .tabs-component-tabs {
        border-radius: 6px;
        border: 0;
        align-items: stretch;
        display: flex;
        justify-content: flex-start;
        margin-bottom: -1px;
        padding-left: 40px;
    }

    .tabs-component-tab {
        color: #999;
        font-size: 14px;
        font-weight: 600;
        margin-right: 0;
        list-style: none;
        background-color: #fff;
        border: solid 1px #ddd;
        border-radius: 3px 3px 0 0;
        margin-right: 8px;

        &.is-active {
            color: #000;
            border-bottom: solid 1px #fff;
            z-index: 2;
        }

        .tabs-component-tab-a {
            align-items: center;
            color: inherit;
            display: flex;
            padding: 11px 14px;
            text-decoration: none;
        }

        .is-disabled * {
            color: #cdcdcd;
            cursor: not-allowed !important;
        }

        &:hover {
          color: #666;
        }
    }
}

.contest {
    .board {
        flex: 2;
        padding: 10px;
    }

    .contest-name {
        margin: 20px 40px;
    }
}

</style>
