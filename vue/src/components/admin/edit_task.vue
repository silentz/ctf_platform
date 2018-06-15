<template>
    <div class='task-edit'>
        <h2 class='header'>Редактировать таск: {{ task.name }}</h2>
        <tabs>
            <tab name='Файлы'>
                <modal name="file-create" height='auto'>
                    <div class='modal-wrapper'>
                        <form @submit.prevent="postFile">
                            <h3>Добавить файл</h3>
                            <input type="file" @change="filesChange($event.target.name, $event.target.files)">
                            <button @click='$modal.hide("file-create")'>Создать</button>
                        </form>
                    </div>
                </modal>
                <button class='create-button' @click='$modal.show("file-create"); file=undefined'>Добавить файл</button>
                <table cellpadding="0" cellspacing="0">
                    <thead>
                        <th>Название</th>
                        <th>Операции</th>
                    </thead>
                    <tbody>
                        <file class='file-entry' v-for='file in files' :key='file.id' :file="file"></file>
                    </tbody>
                </table>
            </tab>
            <tab name='Хинты'>
                <table cellpadding="0" cellspacing="0">
                    <thead>
                        <th>Текст</th>
                        <th>Операции</th>
                    </thead>
                    <tbody>
                        <hint class='hint-entry' v-for='hint in hints' :key='hint.id' :hint="hint"></hint>
                    </tbody>
                </table>
            </tab>
        </tabs>
    </div>
</template>

<script>
import axios from 'axios'
import FileComponent from './file.vue'

export default {
    name: 'AdminTaskEdit',
    data: function() {
        return {
            task: {},
            hints: [],
            files: [],
            file: undefined
        }
    },
    methods: {
        postFile() {
            let formData = new FormData()
            formData.append('task', this.task.id)
            formData.append('file', this.file)
            axios.post('/api/files/', formData, { 
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                axios.get(`/api/files/${response.data.id}/`).then(response => {
                    this.files.push(response.data)
                })
            })
        },
        filesChange(name, files) {
            if (files.length >= 1) {
                this.file = files[0]
            }
        }
    },
    created: function() {
        axios.get(`/api/tasks/${this.$route.params.id}`).then(response => {
            this.task = response.data
            for (let index in this.task.files) {
                let file_id = this.task.files[index]
                axios.get(`/api/files/${file_id}/`).then(response => {
                    this.files.push(response.data)
                })
            }
            for (let index in this.task.hints) {
                let hint_id = this.task.hints[index]
                axios.get(`/api/hints/${hint_id}/`).then(response => {
                    this.hints.push(response.data)
                })
            }
        })
    },
    components: {
        'file': FileComponent
    }
}
</script>

<style lang='scss'>
@import '../../assets/style/tabs.scss';

.task-edit {

    .header {
        margin-left: 40px;
        margit-top: 10px;
    }
    .create-button {
        margin-bottom: 20px;
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

        .hint-entry, .file-entry {

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
            input, select, textarea {
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