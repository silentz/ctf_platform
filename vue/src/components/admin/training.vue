<template>
    <tr class='training-entry' v-if='exists'>
        <td class='name'>{{ training.name }}</td>
        <td class='allowed_groups'>
            <span v-for='group in training.allowed_groups_names'>{{ group }} </span>
        </td>
        <td>
            <button @click='$modal.show("edit-training" + training.id)'>&#9998;</button>
            <button @click='$modal.show("delete-training" + training.id)'>&#x2715;</button>
        </td>
        
        <modal :name='"delete-training" + training.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить тренировку?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteTraining()">Да</button>
                    <button class='no' @click="$modal.hide('delete-training' + training.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-training" + training.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать тренировку</h2>
                <form @submit.prevent="updateTraining">
                    <input size="30" type='text' v-model='name' placeholder='Название тренировки' required>
                    <select v-model='allowed_groups' multiple size='7'>
                        <template v-for='group in groups'>
                            <option :value='group.id'>{{ group.name }}</option>
                        </template>
                    </select>
                    <button @click="$modal.hide('edit-training' + training.id)">Сохранить</button>
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
    props: ['training', 'groups'],
    data: function() {
        return {
            exists: true,
            name: this.training.name,
            start_datetime: this.training.start_datetime,
            finish_datetime: this.training.finish_datetime,
            allowed_groups: this.training.allowed_groups
        }
    },
    methods: {
        updateTraining() {
            axios.patch(`/api/contests/${this.training.id}/?training=true`, {
                name: this.name,
                allowed_groups: this.allowed_groups
            }).then(response => {
                this.training = response.data
            })
        },
        deleteTraining() {
            axios.delete(`/api/contests/${this.training.id}/?training=true`).then(response => {
                this.$modal.hide('delete-training' + this.training.id)
                this.exists = false
            })
        },
        getReadableDate(datestring) {
            return dateFormat(new Date(datestring), "HH:MM dd.mm.yyyy")
        },
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/edit-wrapper.scss';
@import '../../assets/style/delete-wrapper.scss';

.training-entry {
    .allowed_groups {
        font-style: italic;
    }
}
</style>