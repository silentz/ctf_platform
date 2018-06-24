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
import {WebSocketBridge} from '../assets/js/websocketbridge.js'

export default {
    name: 'Notifications',
    data: function() {
        return {
            messages: [],
            socket: {}
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
        },
        notify(text) {
            let n = new Notification('Новое уведомление', {
                body: text,
                icon: '../../../flag-icon.png'
            })
        }
    },
    created: function() {
        this.loadMessages()
        this.socket = new WebSocketBridge();
        this.socket.connect(`/ws/contest/${this.$route.params.id}/notifications/`)
        this.socket.listen((action, stream) => {
            if (action.text) {
                if (Notification.permission.toLowerCase() == "granted") {
                    this.notify(action.text)
                } else if(Notification.permission.toLowerCase() == "denied") {
                    // nothing :C
                } else {
                    Notification.requestPermission((result) => {
                        if (result.toLowerCase() == "granted") {
                            this.notify(action.text)
                        } 
                    });
                }
            }
            this.loadMessages()
        })
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
