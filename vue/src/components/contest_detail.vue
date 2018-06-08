<template lang="html">
    <div class="contest">
        <transition-group name='tasks' tag='div' class='board'>
            <task v-for="task in tasks" :task="task" :key="task.id"></task>
        </transition-group>
    </div>
</template>

<script>
import axios from 'axios'
import TaskComponent from './task.vue'

export default {
    name: "ContestDetail",
    components: {
        task: TaskComponent
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

$task_width: 120px;

.contest {
    min-height: 100%;
    display: flex;
    flex-direction: row-reverse;
    justify-content: flex-start;
    align-items: stretch;

    .board {
        flex: 2;
        padding: 10px;
    }
}

</style>
