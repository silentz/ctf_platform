<template>
    <tr class='hint-entry' v-if='exists'>
        <td>{{ hint.text | cut(90) }}</td>
        <td>
            <button @click='$modal.show("edit-hint" + hint.id)'>&#9998;</button>
            <button @click='$modal.show("delete-hint" + hint.id)'>&#x2715;</button>
        </td>

        <modal :name='"delete-hint" + hint.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить хинт?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteHint()">Да</button>
                    <button class='no' @click="$modal.hide('delete-hint' + hint.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-hint" + hint.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать хинт</h2>
                <form @submit.prevent="updateHint">
                    <textarea cols="60" rows='10' v-model='text' placeholder="Текст" required></textarea>
                    <button @click="$modal.hide('edit-hint' + hint.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>

<script>
import axios from 'axios'

export default {
    name: 'HintAdminEdit',
    props: ['hint'],
    data: function() {
        return  {
            exists: true,
            text: this.hint.text
        }
    },
    methods: {
        deleteHint() {
            axios.delete(`/api/hints/${this.hint.id}/`).then(response => {
                this.exists = false
            })
        },
        updateHint() {
            axios.put(`/api/hints/${this.hint.id}/`, {
                text: this.text,
                task: this.hint.task
            }).then(response => {
                this.hint = response.data
            })
        }
    },
    filters: {
        cut: function(value, len) {
            if (value.length <= len){ 
                return value
            } else {
                return value.substring(0, len) + '...'
            }
        }
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';
</style>