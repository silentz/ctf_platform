<template>
    <tr class='message-entry' v-if='exists'>
        <td class='text'>{{ message.text }}</td>
        <td>
            <button @click='$modal.show("edit-message" + message.id)'>&#9998;</button>
            <button @click='$modal.show("delete-message" + message.id)'>&#x2715;</button>
        </td>

        <modal :name='"delete-message" + message.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить уведомление?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteMessage()">Да</button>
                    <button class='no' @click="$modal.hide('delete-message' + task.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-message" + message.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать уведомление</h2>
                <form @submit.prevent="updateMessage">
                    <textarea v-model='text' cols='50' rows='10' placeholder="Текст" required></textarea>
                    <button @click="$modal.hide('edit-message' + message.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>


<script>
import axios from 'axios'

export default {
    name: 'AdminMessageEntry',
    props: ['message'],
    data: function() {
        return {
            exists: true,
            text: this.message.text
        }
    },
    methods: {
        updateMessage() {
            axios.put(`/api/messages/${this.message.id}/?for=${this.message.contest}`, {
                text: this.text,
                contest: this.message.contest
            }).then(response => {
                this.message = response.data
            })
        },
        deleteMessage() {
            axios.delete(`/api/messages/${this.message.id}/?for=${this.message.contest}`).then(reponse => {
                this.exists = false
            })
        }
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';

.message-entry {
    form {
        display: flex;
        flex-direction: column;
        width: 90%;
    }
}
</style>