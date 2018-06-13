<template>
    <tr class='group-entry' v-if='exists'>
        <td class='name'>{{ group.name }}</td>
        <td class='invite_code'>{{ group.invite_code }}</td>
        <td>
            <button @click='$modal.show("edit-group" + group.id)'>&#9998;</button>
            <button @click='$modal.show("delete-group" + group.id)'>&#x2715;</button>
        </td>
        
        <modal :name='"delete-group" + group.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить группу?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteGroup()">Да</button>
                    <button class='no' @click="$modal.hide('delete-group' + group.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-group" + group.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать группу</h2>
                <form @submit.prevent="updateGroup">
                    <input size="30" type='text' v-model='name' placeholder='Имя группы' required>
                    <input size="30" type='text' v-model='invite_code' placeholder="Инвайт-код" required>
                    <button @click="$modal.hide('edit-group' + group.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AdminGroup',
    props: ['group'],
    data: function() {
        return {
            exists: true,
            name: this.group.name,
            invite_code: this.group.invite_code
        }
    },
    methods: {
        updateGroup() {
            axios.put(`/api/groups/${this.group.id}/`, {
                name: this.name,
                invite_code: this.invite_code
            }).then(response => {
                this.group.name = this.name
                this.group.invite_code = this.invite_code
            })
        },
        deleteGroup() {
            axios.delete(`/api/groups/${this.group.id}/`).then(response => {
                this.exists = false
            })
        }
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';
</style>