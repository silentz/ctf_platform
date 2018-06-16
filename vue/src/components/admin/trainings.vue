<template>
    <div class='training-management'>
        <modal name="training-create" height='auto'>
            <div class='modal-wrapper'>
                <form @submit.prevent="postTraining">
                    <h3>Создать тренировку</h3>
                    <input v-model='name' size="30" type='text' required placeholder="Название тренировки">
                    <select v-model='allowed_groups' multiple size='7'>
                        <option v-for='group in groups' :value="group.id">{{ group.name }}</option>
                    </select>
                    <button>Создать</button>
                </form>
            </div>
        </modal>
        <button @click="addTraining()" class='add-group-button'>Добавить тренировку</button>
        <table cellpadding="0" cellspacing="0">
            <thead>
                <th>Название тренировки</th>
                <th>Допущенные группы</th>
                <th>Операции</th>
            </thead>
            <tbody>
                <training-entry class='training-entry' v-for='training in trainings'
                    :training="training" :key='training.id' :groups='groups'>
                </training-entry>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import TrainingEntry from './training.vue'

export default {
    name: 'TrainingAdmin',
    data: function() {
        return {
            trainings: [],
            groups: [],
            name: '',
            allowed_groups: []
        }
    },
    created: function() {
        axios.get('/api/groups/').then(response => {
            this.groups = response.data
        })
        axios.get('/api/contests/?training=true').then(response => {
            this.trainings = response.data
        })
    },
    methods: {
        clearFields() {
            this.name = ''
            this.allowed_groups = []
        },
        addTraining() {
            this.clearFields()
            this.$modal.show('training-create')
        },
        postTraining() {
            axios.post('/api/contests/', {
                name: this.name,
                allowed_groups: this.allowed_groups,
                tasks: [],
                messages: [],
                training: true
            }).then(response => {
                this.trainings.push(response.data)
                this.$modal.hide('training-create')
            })
        }
    },
    components: {
        'training-entry': TrainingEntry
    }
}    
</script>

<style lang='scss'>

.training-management {
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

        .training-entry {

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