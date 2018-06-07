<template lang="html">
    <div class="contests">
        <router-link class='item' v-for="contest in contests" :key="contest.id"
            :to="{ name: 'contest_detail', params: {id: contest.id} }">
                <div class='data'>
                    <h3 class='name'>{{ contest.name }}</h3>
                    <p class='time'>
                        &#128336; c 15:00 10.10.2010 до 16:00 11.11.2011
                    </p>
                </div>
        </router-link>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Contests',
    data: function() {
        return {
            contests: []
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
