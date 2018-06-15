<template>
    <div class='contest-detail'>
        <h2 class='header'>Редактировать контест: {{ contest.name }}</h2>
        <tabs>
            <tab name='Таски'>
                <modal name="task-create" height='auto'>
                    <div class='modal-wrapper'>
                        <form @submit.prevent="postTask">
                            <h3>Создать таск</h3>
                            <input v-model='name' size="30" placeholder='Название таска' required>
                            <input type='number' v-model='score' size='30' placeholder="Очки" required>
                            <select v-model='category'>
                                <option v-for='cat in categories' :key='cat.id' :value="cat.id">{{ cat.name }}</option>
                            </select>
                            <input v-model='flag' size="30" placeholder="Флаг" required>
                            <textarea v-model='description' cols='50' rows='10' placeholder="Описание" required></textarea>
                            
                            <button @click='$modal.hide("task-create")'>Создать</button>
                        </form>
                    </div>
                </modal>
                <button class='create-task-button' @click='showCreate()'>Создать таск</button>
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
                <modal name="message-create" height='auto'>
                    <div class='modal-wrapper'>
                        <form @submit.prevent="postMessage">
                            <h3>Создать уведомление</h3>
                            <textarea v-model='message' cols='50' rows='10' placeholder="Текст" required></textarea>
                            <button @click='$modal.hide("message-create")'>Создать</button>
                        </form>
                    </div> 
                </modal>
                <button class='create-task-button' @click="createMessage()">Создать уведомление</button>
                <table cellpadding="0" cellspacing="0">
                    <thead>
                        <th>Текст</th>
                        <th>Операции</th>
                    </thead>
                    <tbody>
                        <message class='message-entry' v-for='msg in messages' :key='msg.id' :message='msg'></message>
                    </tbody>
                </table>
            </tab>
        </tabs>
    </div>
</template>

<script>
import axios from 'axios'
import TaskComponent from './task.vue'
import MessageComponent from './message.vue'

export default {
    name: 'ContestAdminEdit',
    data: function() {
        return {
            messages: [],
            message: "",

            contest: {},
            tasks: [],
            categories: [],
            name: "",
            score: 0,
            description: "",
            flag: "",
            category: 1
        }
    },
    methods: {
        postTask() {
            axios.post('/api/tasks/', {
                name: this.name,
                category: this.category,
                flag: this.flag,
                description: this.description,
                score: this.score,
                files: [],
                hints: [],
                contest: this.contest.id
            }).then(response => {
                this.tasks.push(response.data)
            })
        },
        postMessage() {
            axios.post(`/api/messages/?for=${this.contest.id}`, {
                contest: this.contest.id,
                text: this.message
            }).then(response => {
                this.messages.unshift(response.data)
            })
        },
        createMessage() {
            this.message = ""
            this.$modal.show('message-create')
        },
        showCreate() {
            this.name = ""
            this.score = 0
            this.description = ""
            this.flag = ""
            this.category = 1
            this.$modal.show('task-create')
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
            axios.get(`/api/messages/?for=${this.contest.id}`).then(response => {
                this.messages = response.data
            })
        })
        axios.get('/api/categories/').then(response => {
            this.categories = response.data
        })
        
    },
    components: {
        task: TaskComponent,
        message: MessageComponent
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/tabs.scss';

.contest-detail {
    .header {
        padding: 10px 40px;
    }

    .create-task-button {
        margin-bottom: 20px;
    }

    .modal-wrapper {
        width: 100%;
        height: 100%;
        padding: 10px;
        box-sizing: border-box;
        background-color: #222222;
        color: white;

        form {
            h3 {
                font-size: 1.5rem;
            }
            input, select, textarea {
                display: block;
                margin: 5px 0;
                font-size: 1rem;
                outline: none;
                padding: 6px;
                border: none;
            }
            button {
                outline: none;
                border: none;
                font-size: 1rem;
                background-color: lightgreen;
                padding: 5px;
                margin-top: 10px;
            }
        }
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

        .task-entry, .message-entry {

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