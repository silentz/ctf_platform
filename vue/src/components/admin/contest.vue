<template>
    <tr class='contest-entry' v-if='exists'>
        <td class='name'>{{ contest.name }}</td>
        <td class='starts_at'>{{ getReadableDate(contest.start_datetime) }}</td>
        <td class='finished_at'>{{ getReadableDate(contest.finish_datetime) }}</td>
        <td class='allowed_groups'>
            <span v-for='group in contest.allowed_groups_names'>{{ group }} </span>
        </td>
        <td>
            
            <router-link :to='{name: "edit_contest", params: {id: contest.id}}'>
                <button>
                    &#x21B3;
                </button>
            </router-link>
            
            <button @click='$modal.show("edit-contest" + contest.id)'>&#9998;</button>
            <button @click='$modal.show("delete-contest" + contest.id)'>&#x2715;</button>
        </td>
        
        <modal :name='"delete-contest" + contest.id' height='auto'>
            <div class='delete-wrapper'>
                <h2>Удалить контест?</h2>
                <div class='buttons'>
                    <button class='yes' @click="deleteContest()">Да</button>
                    <button class='no' @click="$modal.hide('delete-contest' + contest.id)">Нет</button>
                </div>
            </div>
        </modal>
        <modal :name='"edit-contest" + contest.id' height='auto'>
            <div class='edit-wrapper'>
                <h2>Редактировать контест</h2>
                <form @submit.prevent="updateContest">
                    <input size="30" type='text' v-model='name' placeholder='Название контеста' required>
                    <datetime v-model='start_datetime' type='datetime' placeholder='Время начала'></datetime>
                    <datetime v-model='finish_datetime' type='datetime' placeholder='Время конца'></datetime>
                    <select v-model='allowed_groups' multiple size='7'>
                        <template v-for='group in groups'>
                            <option :value='group.id'>{{ group.name }}</option>
                        </template>
                    </select>
                    <button @click="$modal.hide('edit-contest' + contest.id)">Сохранить</button>
                </form>
            </div>
        </modal>
    </tr>
</template>


<script>
import axios from 'axios'
import dateFormat from 'dateformat'

export default {
    name: 'AdminContestEntry',
    props: ['contest', 'groups'],
    data: function() {
        return {
            exists: true,
            name: this.contest.name,
            start_datetime: this.contest.start_datetime,
            finish_datetime: this.contest.finish_datetime,
            allowed_groups: this.contest.allowed_groups
        }
    },
    methods: {
        updateContest() {
            axios.patch(`/api/contests/${this.contest.id}/`, {
                name: this.name,
                start_datetime: this.start_datetime,
                finish_datetime: this.finish_datetime,
                allowed_groups: this.allowed_groups
            }).then(response => {
                this.contest = response.data
            })
        },
        deleteContest() {
            axios.delete(`/api/contests/${this.contest.id}/`).then(response => {
                this.$modal.hide('delete-contest' + this.contest.id)
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

.contest-entry {
    .allowed_groups {
        font-style: italic;
    }
}
</style>