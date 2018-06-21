<template lang="html">
    <div class='task' @click="showTask()" :class="{ solved: task.solved }">
        <modal :name='"task" + task.id' height="auto">
            <div class='modal-wrapper'>
                <div class="task-detail">
                    <div class='about'>
                        <div class='cross' @click.stop="hideTask()">&#x2715;</div>
                        <h2>{{ task.name }} ({{ task.category_name }}, {{ task.score }})</h2>
                        <vue-markdown>{{ task.description }}</vue-markdown>
                        <p v-for="(hint, index) in hints" class='hint'>
                            Hint {{ index + 1 }}: {{ hint.text }}
                        </p>
                        <div class='files' v-if="this.files.length > 0">
                            <h3>Файлы:</h3>
                            <ul>
                                <li class='file' v-for='file in this.files'>
                                    <a :href="'/api/files/' + file.id + '/download/'">
                                        {{ file.name }}
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <form @submit.prevent="sendFlag">
                        <p v-show="mistake" class='form-mistake'>Неверный флаг</p>
                        <p v-show="task.solved" class='form-solved'>Верно!</p>
                        <div class='fields' v-if='!task.solved'>
                            <input v-model='flag' type='text' required placeholder="Flag">
                            <button type='submit'>Check</button>
                        </div>
                    </form>
                </div>
            </div>
        </modal>

        <div class='score'>
            {{ task.score }}
        </div>
        <div class='category'>
            {{ task.category_name }}
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import VueMarkdown from 'vue-markdown'

export default {
    props: ['task'],
    data: function() {
        return {
            flag: '',
            files: [],
            hints: [],
            mistake: false
        }
    },
    created: function() {
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
    },
    methods: {
        showTask() {
            this.$modal.show('task' + this.task.id)
        },
        hideTask() {
            this.$modal.hide('task' + this.task.id)
        },
        sendFlag() {
            axios.post(`/api/tasks/${this.task.id}/pass_flag/`, {flag: this.flag})
            .then(response => {
                this.task.solved = true
                this.mistake = false
            }).catch(err => {
                this.mistake = true
            })
        }
    },
    components: {
        VueMarkdown
    }
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css?family=Roboto+Mono');

$task-width: 120px;
$task-height: 80px;

.solved {
    background-color: #2FCF39 !important;
}

.task {
    display: inline-flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: $task-width;
    height: $task-height;
    background-color: #e1e1e1;
    color: black;
    border-radius: 5px;
    margin: 5px;

    .score {
        font-size: 1.6rem;
        user-select: none;
    }

    .category {
        font-size: 1rem;
        user-select: none;
    }
}

.tasks-enter-active {
    transition: all .5s;
}

.tasks-enter {
    opacity: 0;
}

.modal-wrapper {
    height: 100%;
    width: 100%;
    background-color: #222222;
    color: white;
    box-sizing: border-box;

    .task-detail {
        padding: 10px 15px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-start;
        height: 100%;
        box-sizing: border-box;

        a {
            color: red;
            text-decoration: none;
        }

        .hint {
            margin: 3px 0;
        }

        .files {
            margin: 10px 0;
            h3 { margin: 5px 0; }

            ul {
                padding: 0 20px;
                a {
                    text-decoration: none;
                    color: yellow;
                }
            }
        }

        h2 {
            margin-top: 15px;
        }

        .form-mistake {
            color: red;
        }

        .form-solved {
            color: #76ff03;
        }

        .fields {
            margin: 5px 0;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: stretch;
            max-width: 100%;

            input {
                outline: none;
                margin-right: 10px;
                font-size: 1rem;
                padding: 5px 5px;
                font-family: 'Roboto Mono', monospace;
                border: none;
                display: inline-block;
                transition: .3s;
            }

            button {
                display: inline-block;
                font-size: 1rem;
                margin-top: 0;
                color: #614444;
                display: inline-block;
                padding: 0 5px;
                border: none;
                background-color: inherit;
                margin: 0;
                background-color: #616161;
                font-size: 1.1rem;
                color: white;
                outline: none;
            }
        }

        .cross {
            cursor: pointer;
            user-select: none;
            top: 5px;
            right: 10px;
            position: absolute;
            font-size: 2rem;
            float: right;
        }
    }
}
</style>
