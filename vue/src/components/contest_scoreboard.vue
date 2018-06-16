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

export default {
    name: "ContestScoreboard",
    props: ['contest_id'],
    data: function() {
        return {
            results: []
        }
    },
    methods: {
        loadScoreboard() {
            axios.get(`/api/contests/${this.$route.params.id}/scoreboard/`)
            .then(response => {
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
    created: function () {
        this.loadScoreboard()
        setInterval(this.loadScoreboard, 1000 * 60 * 3)
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
