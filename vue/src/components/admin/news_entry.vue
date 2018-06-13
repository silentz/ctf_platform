<template>
    <tr class='news-entry' v-if='exists'>
        <td class='name'>{{ entry.text | cut(40) }}</td>
        <td class='time'>{{ getReadableDate(entry.time) }}</td>
        <td>
            <button @click='$modal.show("edit-entry" + entry.id)'>&#9998;</button>
            <button @click='$modal.show("delete-entry" + entry.id)'>&#x2715;</button>
        </td>
        
        <modal :name='"delete-entry" + entry.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить новость?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteEntry()">Да</button>
                    <button class='no' @click="$modal.hide('delete-entry' + entry.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-entry" + entry.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать новость</h2>
                <form @submit.prevent="updateEntry">
                    <textarea cols="60" rows='10' v-model='text' placeholder="Текст новости" required></textarea>
                    <button @click="$modal.hide('edit-entry' + entry.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>

<script>
import axios from 'axios'
import dateFormat from 'dateformat'

export default {
    name: 'NewsEntry',
    props: ['entry'],
    data: function() {
        return {
            exists: true,
            text: this.entry.text
        }
    },
    methods: {
        getReadableDate(datestring) {
            return dateFormat(new Date(datestring), "HH:MM dd.mm.yyyy")
        },
        updateEntry() {
            axios.put(`/api/news/${this.entry.id}/`, {
                text: this.text
            }).then(response => {
                this.entry.text = this.text
            })
        },
        deleteEntry() {
            axios.delete(`/api/news/${this.entry.id}/`).then(response => {
                this.exists = false
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