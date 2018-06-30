from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class ContestScoreboardConsumer(JsonWebsocketConsumer):

    def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            self.contest_id = self.scope['url_route']['kwargs']['contest_id']
            async_to_sync(self.channel_layer.group_add)(
                'contest_{}_scoreboard'.format(self.contest_id),
                self.channel_name
            )
            self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            'contest_{}_scoreboard'.format(self.contest_id),
            self.channel_name
        )

    def scoreboard_changed(self, event):
        self.send_json(content={'action': 'update'})


class ContestNotificationConsumer(JsonWebsocketConsumer):

    def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            self.contest_id = self.scope['url_route']['kwargs']['contest_id']
            contest_group = 'contest_{}_notifications'.format(self.contest_id)
            async_to_sync(self.channel_layer.group_add)(contest_group, self.channel_name)
            self.accept()

    def disconnect(self, code):
        contest_group = 'contest_{}_notifications'.format(self.contest_id)
        async_to_sync(self.channel_layer.group_discard)(contest_group, self.channel_name)

    def notifications_changed(self, event):
        if event['data'] is not None:
            self.send_json(content={'action': 'update', 'text': event['data']})
        else:
            self.send_json(content={'action': 'update'})


class ScoreboardConsumer(JsonWebsocketConsumer):

    def connect(self):
        if self.scope['user'].is_anonymous:
            self.close()
        else:
            async_to_sync(self.channel_layer.group_add)('scoreboard', self.channel_name)
            self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)('scoreboard', self.channel_name)

    def scoreboard_changed(self, event=None):
        self.send_json(content={'action': 'update'})