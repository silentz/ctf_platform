<template>
    <div class='categories'>
        <modal name="category-create" height='auto'>
            <div class='modal-wrapper'>
                <form @submit.prevent="postCategory">
                    <h3>Создать категорию</h3>
                    <input v-model='name' size="40" required placeholder="Название">
                    <button @click='$modal.hide("category-create")'>Создать</button>
                </form>
            </div>
        </modal>
        <button @click="name=''; $modal.show('category-create')" class='add-button'>Добавить категорию</button>
        <table cellpadding="0" cellspacing="0">
            <thead>
                <th>Название</th>
                <th>Операции</th>
            </thead>
            <tbody>
                <category-entry class='category-entry' v-for='cat in categories' :category="cat" :key='cat.id'>
                </category-entry>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import CategoryEntry from './category.vue'

export default {
    name: 'CategoryManager',
    data: function() {
        return  {
            name: '',
            categories: []
        }
    },
    created: function() {
        axios.get('/api/categories/').then(response => {
            this.categories = response.data
        })
    },
    components: {
        'category-entry': CategoryEntry
    },
    methods: {
        postCategory() {
            axios.post('/api/categories/', {name: this.name}).then(response => {
                this.categories.push(response.data)
            })
        }
    }
}
</script>

<style lang='scss'>
.categories {
    .add-button {
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

        .category-entry {

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