<template lang="html">
    <div class="ctf-items">
        <div class="ctf-contest-item" v-for="contest in contests">
            <div class='ctf-contest-item-data'>
                <h3 class='ctf-contest-item-label'>{{ contest.name }}</h3>
                <p class='ctf-contest-item-time'>
                    &#128336; c 15:00 10.10.2010 до 16:00 11.11.2011
                </p>
            </div>
        </div>
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

<style lang="css">
</style>
