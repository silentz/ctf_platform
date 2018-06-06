<template lang="html">
    <div class="ctf-items">
        <div class="ctf-contest-item" v-for="training in trainings">
            <div class='ctf-contest-item-data'>
                <h3 class='ctf-contest-item-label'>{{ training.name }}</h3>
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
    name: 'Trainings',
    data: function() {
        return {
            trainings: []
        }
    },
    created: function() {
        axios.get('/api/trainings/').then(response => {
            this.trainings = response.data
        }).catch(error => {
            // pass
        })
    }
}
</script>

<style lang="css">
</style>
