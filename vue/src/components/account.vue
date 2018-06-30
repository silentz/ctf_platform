<template lang="html">
    <div class="account">
        <div class="header">
            <h2>Личный кабинет</h2>
            <h3>{{ full_name }} [{{ username }}]</h3>
        </div>
        <div class="content">
            <tabs>
                <tab name='Смена пароля'>
                    <p class='status' v-if='statusEnabled'>{{ status }}</p>
                    <form @submit.prevent="handleSubmit" class='change-password'>
                        <input size="40" v-model='oldpass' type='password' required placeholder="Старый пароль">
                        <input size="40" v-model='newpass' type='password' required placeholder="Новый пароль">
                        <button>Сменить</button>
                    </form>
                </tab>
                <tab name="Решенные таски">
                    <table class='solved-tasks'>
                        <thead>
                            <th>Название</th>
                            <th>Категория</th>
                            <th>Очки</th>
                        </thead>
                        <tbody>
                            <tr v-for="task in solved_tasks" :key="task.id">
                                <td>{{ task.name }}</td>
                                <td>{{ task.category_name }}</td>
                                <td>{{ task.score }}</td>
                            </tr>
                        </tbody>
                    </table>
                </tab>
            </tabs>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Account",
    data: function() {
        return {
            oldpass: "",
            newpass: "",
            statusEnabled: false,
            status: "",
            solved_tasks: []
        }
    },
    methods: {
        clearFields() {
            this.oldpass = ""
            this.newpass = ""
        },
        hideStatus() {
            this.statusEnabled = false
        },
        showStatus(status) {
            this.status = status
            this.statusEnabled = true
            setTimeout(this.hideStatus, 1000 * 5)
        },
        handleSubmit() {
            axios.post('/api/auth/change/', {
                "old_password": this.oldpass,
                "new_password": this.newpass
            }).then(response => {
                this.clearFields()
                this.showStatus("Пароль успешно изменён")
            }).catch(err => {
                this.clearFields()
                this.showStatus("Неверный текущий пароль")
            })
        }
    },
    computed: {
        username: function() {
            return this.$store.state.username
        },
        full_name: function() {
            return this.$store.state.full_name
        }
    },
    created: function() {
        axios.get('/api/tasks/solved/').then(response => {
            this.solved_tasks = response.data
        })
    }
}
</script>

<style lang="scss">
@import "../assets/style/tabs.scss";

.account {
    margin: 10px;
    padding: 10px;
    background-color: white;

    .header {
        padding: 0 40px;
    }

    .change-password {
        input {
            display: block;
            margin: 10px 0;
            user-select: none;
            outline: none;
            padding: 5px;
            border-radius: 5px;
            border: 2px solid grey;
        }

        button {
            display: inline-block;
            outline: none;
            border: none;
            border-radius: 5px;
            background-color: #444;
            margin: 0;
            font-size: 0.9rem;
            color: white;
            padding: 7px;
        }
    }

    .solved-tasks {
        width: 100%;
        th {
            text-align: left;
            padding: 5px 0;
        }
    }
}
</style>
