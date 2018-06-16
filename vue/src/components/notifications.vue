<template lang="html">
    <div class='notifications'>
        <div class="message" v-for="message in messages" :key="message.id">
            <p>{{ message.text }}</p>
            <h5>&#128336; {{ getReadableDate(message.time) }}</h5>
            <!-- <hr> -->
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import dateFormat from 'dateformat'

export default {
    name: 'Notifications',
    data: function() {
        return {
            messages: []
        }
    },
    methods: {
        loadMessages() {
            axios.get(`/api/messages/?for=${this.$route.params.id}`)
            .then(response => {
                this.messages = response.data
            })
        },
        getReadableDate(datestring) {
            return dateFormat(new Date(datestring), "HH:MM:ss dd.mm.yyyy")
        }
    },
    created: function() {
        this.loadMessages()
        setInterval(this.loadMessages, 1000 * 60 * 3)
    }
}
</script>

<style lang="scss">
.notifications {
    .message {
        background-color: silver;
        border-radius: 5px;
        margin: 10px 0;
        padding: 5px;
        color: black;

        p {
            margin: 10px;
        }

        h5 {
            font-size: 0.8rem;
            font-weight: normal;
            margin: 10px;
        }
    }
}
</style>
