<template>
    <div class='news'>
        <modal name="news-create" height='auto'>
            <div class='modal-wrapper'>
                <form @submit.prevent="postNews">
                    <h3>Создать новость</h3>
                    <textarea v-model='text' cols="60" rows='10' required placeholder="Текст новости">
                    </textarea>
                    <button>Создать</button>
                </form>
            </div>
        </modal>
        <button @click="addNewsEntry()" class='add-group-button'>Добавить новость</button>
        <table cellpadding="0" cellspacing="0">
            <thead>
                <th>Текст</th>
                <th>Дата</th>
                <th>Операции</th>
            </thead>
            <tbody>
                <news-entry class='news-entry' v-for='entry in news' :entry="entry" :key='entry.id'></news-entry>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import NewsEntry from './news_entry.vue'

export default {
    name: 'NewsManager',
    data: function() {
        return  {
            text: '',
            news: []
        }
    },
    created: function() {
        axios.get('/api/news/').then(response => {
            this.news = response.data
        })
    },
    components: {
        'news-entry': NewsEntry
    },
    methods: {
        addNewsEntry() {
            this.text = ''
            this.$modal.show('news-create')
        },
        postNews() {
            axios.post('/api/news/', {text: this.text}).then(response => {
                this.news.unshift(response.data)
                this.$modal.hide('news-create')
            })
        }
    }
}
</script>

<style lang='scss'>
.news {
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

        .news-entry {

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

            textarea {
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