<template lang="html">
    <div class='scoreboard'>
        <h2>Скорборд</h2>
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

export default {
    name: "Scoreboard",
    data: function() {
        return {
            results: []
        }
    },
    methods: {
        loadScoreboard() {
            axios.get('/api/scoreboard/').then(response => {
                this.results = response.data.sort((a, b) => {
                    if (a.score > b.score)
                        return -1
                    else if (a.score < b.score)
                        return 1
                    return 0
                })
            })
        }
    },
    created: function() {
        this.loadScoreboard()
        setInterval(this.loadScoreboard, 1000 * 60 * 3)
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
