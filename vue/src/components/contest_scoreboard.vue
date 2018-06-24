<template lang="html">
    <div class='contest-scoreboard'>
        <table cellspacing="0" cellpadding="0">
            <thead>
                <th>Позиция</th>
                <th>Имя команды</th>
                <th>Результат</th>
            </thead>
            <tbody>
                <tr v-for="(result, index) in results">
                    <td>{{ index + 1 }}</td>
                    <td>{{ result.username }}</td>
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
    name: "ContestScoreboard",
    props: ['contest_id'],
    data: function() {
        return {
            results: [],
            socket: {}
        }
    },
    methods: {
        loadScoreboard() {
            axios.get(`/api/contests/${this.$route.params.id}/scoreboard/`)
            .then(response => {
                this.results = response.data
            })
        }
    },
    created: function () {
        this.loadScoreboard()
        this.socket = new WebSocketBridge();
        this.socket.connect(`/ws/contest/${this.$route.params.id}/scoreboard/`)
        this.socket.listen((action, stream) => {
            this.loadScoreboard()
        })
    }
}
</script>

<style lang="scss">

.contest-scoreboard {
    table {
        width: 100%;
        border: none;

        thead {
            background-color: #e1e1e1;

            th {
                text-align: left;
                padding: 10px;
                font-size: 1rem;
                font-weight: normal;
            }
        }

        tbody {
            tr {
                &:nth-child(even) {
                    background-color: lightgreen;
                }

                &:nth-child(odd) {
                    background-color: white;
                }

                td {
                    padding: 5px 10px;
                }
            }

        }
    }
}

</style>
