<template lang="html">
    <div class="contest">
        <div class='info'>
            <h2>{{ contest.name }}</h2>
            <hr>
            <div class='task-description'>
                <h2>{{ task.name }}</h2>
                <p>{{ task.description }}</p>
            </div>
        </div>
        <transition-group name='tasks' tag='div' class='board'>
            <div class='task' v-for="task in tasks" :key="task.id" @click="showTask(task.id)">
                <div class='score'>
                    {{ task.score }}
                </div>
                <div class='category'>
                    {{ categories[task.category].name }}
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "ContestDetail",
    data: function() {
        return {
            contest: "",
            tasks: [],
            categories: {},
            task: {}
        }
    },
    created: function() {
        axios.get(`/api/contests/${this.$route.params.id}/`).then(response => {
            this.contest = response.data
            for (let index in this.contest.categories) {
                let cat_id = this.contest.categories[index]
                axios.get(`/api/categories/${cat_id}/`).then(response => {
                    this.categories[cat_id] = response.data
                })
            }
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

    .info {
        flex: 1;
        background-color: #222222;
        min-width: 280px;
        color: white;
        padding: 20px;
        box-sizing: border-box;

        h2 {
            margin: 0;
        }
    }

    .tasks-enter-active {
        transition: all .5s;
    }
    .tasks-enter {
        opacity: 0;
    }

    .board {
        flex: 2;
        padding: 10px;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: flex-start;
        align-items: flex-start;

        .task {
            display: inline-flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 120px;
            height: 80px;
            background-color: white;
            border-radius: 5px;
            margin: 5px;

            .score {
                font-size: 1.6rem;
            }

            .category {
                font-size: 1rem;
            }
        }
    }
}

</style>
