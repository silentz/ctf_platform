<template lang="html">
    <div class="contests">
        <div class="item" v-for="training in trainings">
            <div class='data'>
                <h3 class='name'>{{ training.name }}</h3>
                <p class='time'>
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
        axios.get('/api/contests/?training=true').then(response => {
            this.trainings = response.data
        }).catch(error => {
            // pass
        })
    }
}
</script>

<style lang="scss">
@import '../assets/style/contest.scss';
</style>
