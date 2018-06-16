<template>
    <div class='group-management'>
        <modal name="group-create" height='auto'>
            <div class='modal-wrapper'>
                <form @submit.prevent="postGroup">
                    <h3>Создать группу</h3>
                    <input v-model='group_name' size="30" type='text' required placeholder="Имя группы">
                    <input v-model='group_invite_code' size="30" tyle='text' required placeholder="Инвайт-код">
                    <button>Создать</button>
                </form>
            </div>
        </modal>
        <button @click="addGroup()" class='add-group-button'>Добавить группу</button>
        <table cellpadding="0" cellspacing="0">
            <thead>
                <th>Название</th>
                <th>Инвайт-код</th>
                <th>Операции</th>
            </thead>
            <tbody>
                <group class='group-entry' v-for='group in groups' :group="group" :key='group.id'></group>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import Group from './group.vue'

export default {
    name: 'GroupManager',
    data: function() {
        return {
            groups: [],
            group_name: '',
            group_invite_code: ''
        }
    },
    created: function() {
        axios.get('/api/groups/').then(response => {
            this.groups = response.data
        })
    },
    components: {
        group: Group
    },
    methods: {
        clearGroupCreate() {
            this.group_name = ""
            this.group_invite_code = ""
        },
        addGroup() {
            this.clearGroupCreate()
            this.$modal.show('group-create')
        },
        postGroup() {
            console.log(this.group_name)
            axios.post('/api/groups/', {
                name: this.group_name,
                invite_code: this.group_invite_code
            }).then(response => {
                this.groups.push(response.data)
                this.$modal.hide('group-create')
            })
        }
    }
}
</script>

<style lang='scss'>
.group-management {
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

        .group-entry {

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