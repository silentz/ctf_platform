<template lang="html">
    <div class='scoreboard'>
        <h2>Скорборд</h2>
        <table cellspacing="0" cellpadding="0">
            <thead>
                <th>Позиция</th>
                <th>Логин</th>
                <th>Имя участника</th>
                <th>Результат</th>
            </thead>
            <tbody>
                <tr v-for="(result, index) in results">
                    <td>{{ index + 1 }}</td>
                    <td>{{ result.username }}</td>
                    <td>{{ result.full_name }}</td>
                    <td>{{ result.score }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import {WebSocketBridge} from '../assets/js/websocketbridge.js'

export default {
    name: "Scoreboard",
    data: function() {
        return {
            results: [],
            socket: {}
        }
    },
    methods: {
        loadScoreboard() {
            axios.get('/api/scoreboard/').then(response => {
                this.results = response.data
            })
        }
    },
    created: function () {
        this.loadScoreboard()
        this.socket = new WebSocketBridge();
        this.socket.connect('/ws/scoreboard/')
        this.socket.listen((action, stream) => {
            this.loadScoreboard()
        })
    }
}
</script>

<style lang="scss">
.scoreboard {
    padding: 40px;

    h2 {
        margin: 0;
        margin-bottom: 20px;
    }

    table {
        width: 100%;
        border: none;

        thead {
            background-color: white;

            th {
                text-align: left;
                padding: 10px;
                font-size: 1rem;
                font-weight: normal;
            }
        }

        tbody {
            tr {
                border: none;

                &:nth-child(even) {
                    background-color: white;
                }

                &:nth-child(odd) {
                    background-color: lightgreen;
                }

                td {
                    padding: 5px 10px;
                }
            }
        }
    }
}
</style>
