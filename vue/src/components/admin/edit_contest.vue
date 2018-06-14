<template>
    <div class='contest-detail'>
        <h2 class='header'>Редактировать контест: {{ contest.name }}</h2>
        <tabs>
            <tab name='Таски'>
                <table cellpadding="0" cellspacing="0">
                    <thead>
                        <th>Название</th>
                        <th>Категория</th>
                        <th>Стоимость</th>
                        <th>Флаг</th>
                        <th>Операции</th>
                    </thead>
                    <tbody>
                        <task class='task-entry' v-for='task in tasks' :key='task.id' :task='task'></task>
                    </tbody>
                </table>
            </tab>
            <tab name='Уведомления'>

            </tab>
        </tabs>
    </div>
</template>

<script>
import axios from 'axios'
import TaskComponent from './task.vue'

export default {
    name: 'ContestAdminEdit',
    data: function() {
        return {
            contest: {},
            tasks: []
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
    components: {
        task: TaskComponent
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/tabs.scss';

.contest-detail {
    .header {
        padding: 10px 40px;
    }

    table {
        width: 100%;
        border: none;

        th {
            text-align: left;
        }

        td {
            padding: 4px;
        }

        .task-entry {

            &:nth-child(even) {
                background-color: white;
            }
            &:nth-child(odd) {
                background-color: #ddd;
            }
        }
    }
}
</style>