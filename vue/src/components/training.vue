<template lang="html">
    <div class="contests">
        <router-link class='item' v-for="training in trainings" :key="training.id"
            :to="{ name: 'contest_detail', params: {id: training.id} }">
            <div class='data'>
                <h3 class='name'>{{ training.name }}</h3>
            </div>
        </router-link>
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
