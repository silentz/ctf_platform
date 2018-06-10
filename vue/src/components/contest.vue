<template lang="html">
    <div class="contests">
        <router-link class='item' v-for="contest in contests" :key="contest.id"
            :to="{ name: 'contest_detail', params: {id: contest.id} }">
                <div class='data'>
                    <h3 class='name'>{{ contest.name }}</h3>
                    <p class='time'>
                        &#128336; c {{ getReadableDate(contest.start_datetime) }}
                                 до {{ getReadableDate(contest.finish_datetime) }}
                    </p>
                </div>
        </router-link>
    </div>
</template>

<script>
import axios from 'axios'
import dateFormat from 'dateformat'

export default {
    name: 'Contests',
    data: function() {
        return {
            contests: []
        }
    },
    methods: {
        getReadableDate(datestring) {
            return dateFormat(new Date(datestring), "HH:MM:ss dd.mm.yyyy")
        }
    },
    created: function() {
        axios.get("/api/contests/?training=false").then(response => {
            this.contests = response.data
        }).catch(error => {
            // pass
        })
    }
}
</script>

<style lang="scss">
@import '../assets/style/contest.scss';
</style>
