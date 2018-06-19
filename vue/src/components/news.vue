<template lang="html">
    <div class="news">
        <h2>Новости</h2>
        <div class="entry" v-for='entry in news'>
            <vue-markdown>{{ entry.text }}</vue-markdown>
            <h5>&#128336; {{ getReadableDate(entry.time) }}</h5>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import dateFormat from 'dateformat'
import VueMarkdown from 'vue-markdown'

export default {
    name: "News",
    data: function() {
        return {
            news: []
        }
    },
    methods: {
        getReadableDate(datestring) {
            return dateFormat(new Date(datestring), "HH:MM:ss dd.mm.yyyy")
        }
    },
    created: function() {
        axios.get('/api/news/').then(response => {
            this.news = response.data
        })
    },
    components: {
        'vue-markdown': VueMarkdown
    }
}
</script>

<style lang="scss">

.news {
    padding: 10px 30px;

    .entry {
        background-color: white;
        padding: 10px;
        margin: 10px;

        p {
            margin: 0 0 10px 0;
        }

        h5 {
            margin: 0;
            font-size: 0.8rem;
            font-weight: normal;
        }
    }
}

</style>
