<template>
    <div class='contest-management'>
        <modal name="contest-create" height='auto'>
            <div class='modal-wrapper'>
                <form @submit.prevent="postContest">
                    <h3>Создать контест</h3>
                    <input v-model='name' size="30" type='text' required placeholder="Название контеста">
                    <datetime v-model='start_datetime' type='datetime' placeholder='Время начала'></datetime>
                    <datetime v-model='finish_datetime' type='datetime' placeholder='Время конца'></datetime>
                    <select v-model='allowed_groups' multiple size='7'>
                        <option v-for='group in groups' :value="group.id">{{ group.name }}</option>
                    </select>
                    <button>Создать</button>
                </form>
            </div>
        </modal>
        <button @click="addContest()" class='add-group-button'>Добавить контест</button>
        <table cellpadding="0" cellspacing="0">
            <thead>
                <th>Название контеста</th>
                <th>Время начала</th>
                <th>Время конца</th>
                <th>Допущенные группы</th>
                <th>Операции</th>
            </thead>
            <tbody>
                <contest-entry class='contest-entry' v-for='contest in contests'
                    :contest="contest" :key='contest.id' :groups='groups'>
                </contest-entry>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import ContestEntry from './contest.vue'

export default {
    name: 'ContestAdmin',
    data: function() {
        return {
            contests: [],
            groups: [],
            name: '',
            start_datetime: '',
            finish_datetime: '',
            allowed_groups: []
        }
    },
    created: function() {
        axios.get('/api/groups/').then(response => {
            this.groups = response.data
        })
        axios.get('/api/contests/?training=false').then(response => {
            this.contests = response.data
        })
    },
    methods: {
        clearFields() {
            this.name = ''
            this.start_datetime = ''
            this.finish_datetime = ''
            this.allowed_groups = []
        },
        addContest() {
            this.clearFields()
            this.$modal.show('contest-create')
        },
        postContest() {
            axios.post('/api/contests/', {
                name: this.name,
                start_datetime: this.start_datetime,
                finish_datetime: this.finish_datetime,
                allowed_groups: this.allowed_groups,
                tasks: [],
                messages: [],
                training: false
            }).then(response => {
                this.contests.push(response.data)
                this.$modal.hide('contest-create')
            })
        }
    },
    components: {
        'contest-entry': ContestEntry
    }
}    
</script>

<style lang='scss'>

.contest-management {
    .add-group-button {
        margin-bottom: 15px;
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

        .contest-entry {

            &:nth-child(even) {
                background-color: white;
            }
            &:nth-child(odd) {
                background-color: #ddd;
            }
        }
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

            input {
                display: block;
                margin: 5px 0;
                font-size: 1rem;
                outline: none;
                padding: 6px;
                border: none;
                width: 70%;
            }
            select {
                display: block;
                margin: 5px 0;
                font-size: 1rem;
                outline: none;
                width: 70%;
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
}
</style>