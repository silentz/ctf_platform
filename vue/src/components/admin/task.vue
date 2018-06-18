<template>
    <tr class='task-entry' v-if='exists'>
        <td class='name'>{{ task.name }}</td>
        <td class='category'>{{ task.category_name }}</td>
        <td class='score'>{{ task.score }}</td>
        <td class='flag'>{{ task.flag }}</td>
        
        <td>
            <router-link :to='{name: "edit_task", params: {id: task.id}}'>
                <button>&#x21B3;</button>
            </router-link>
            <button @click='$modal.show("edit-task" + task.id)'>&#9998;</button>
            <button @click='$modal.show("delete-task" + task.id)'>&#x2715;</button>
        </td>

        <modal :name='"delete-task" + task.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить таск?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteTask()">Да</button>
                    <button class='no' @click="$modal.hide('delete-task' + task.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-task" + task.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать таск</h2>
                <form @submit.prevent="updateTask">
                    <input v-model='name' size="30" placeholder='Название таска' required>
                    <input type='number' v-model='score' size='30' placeholder="Очки" required>
                    <label><input type='checkbox' v-model='hidden'> Таск скрыт</label>
                    <select v-model='category'>
                        <option v-for='cat in categories' :key='cat.id' :value="cat.id">{{ cat.name }}</option>
                    </select>
                    <input v-model='flag' size="30" placeholder="Флаг" required>
                    <textarea v-model='description' cols='50' rows='10' placeholder="Описание" required></textarea>
                    <button @click="$modal.hide('edit-task' + task.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>


<script>
import axios from 'axios'
import dateFormat from 'dateformat'

export default {
    name: 'AdminTrainingEntry',
    props: ['task'],
    data: function() {
        return {
            exists: true,
            categories: [],
            name: this.task.name,
            category: this.task.category,
            score: this.task.score,
            description: this.task.description,
            flag: this.task.flag,
            hidden: this.task.hidden
        }
    },
    methods: {
        updateTask() {
            axios.put(`/api/tasks/${this.task.id}/`, {
                name: this.name,
                category: this.category,
                score: this.score,
                description: this.description,
                flag: this.flag,
                files: this.task.files,
                hints: this.task.hints,
                contest: this.task.contest,
                hidden: this.hidden
            }).then(response => {
                this.task = response.data
            })
        },
        deleteTask() {
            axios.delete(`/api/tasks/${this.task.id}/`).then(reponse => {
                this.exists = false
            })
        }
    },
    created: function() {
        axios.get('/api/categories/').then(response => {
            this.categories = response.data
        }) 
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';

.task-entry {
    form {
        display: flex;
        flex-direction: column;
        width: 90%;
    }
}
</style>