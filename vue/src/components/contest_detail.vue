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
@import '../assets/style/tabs.scss';

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
