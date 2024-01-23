from rest_framework import serializers
from .models import Player, Game


class PlayerSerializer(serializers.Serializer):
    def to_representation(self, obj):
        if isinstance(obj, str):
            return {'name': obj}
        return {'name': obj.name, 'symbol': obj.symbol}

    class Meta:
        model = Player
        fields = ['name', 'symbol']


class GameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    starting_player = PlayerSerializer()
    next_turn = PlayerSerializer()

    winner = PlayerSerializer()

    class Meta:
        model = Game
        fields = ['id', 'players', 'starting_player', 'movements_played',
                  'next_turn', 'board', 'winner']


class SubmitPlaySerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    player = serializers.CharField()
    row = serializers.IntegerField()
    column = serializers.IntegerField()

    def validate(self, data):
        return data


class GameListSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    starting_player = PlayerSerializer()

    class Meta:
        model = Game
        fields = ['id', 'players', 'starting_player', 'movements_played',
                  'next_turn', 'board', 'winner']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['movements_played'] == 9 \
           and representation['winner'] is None:
            representation['winner'] = 'Tie'
        elif isinstance(representation['winner'], dict):
            representation['winner'] = \
                representation['winner'].get('name', None)

        return representation


class SingleGameSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    starting_player = PlayerSerializer()
    next_turn = PlayerSerializer()
    winner = PlayerSerializer()

    class Meta:
        model = Game
        fields = ['id', 'players', 'starting_player', 'movements_played',
                  'next_turn', 'board', 'winner']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['movements_played'] == 9 \
                and representation['winner'] is None:
            representation['winner'] = 'Tie'
        elif isinstance(representation['winner'], dict):
            representation['winner'] = \
                representation['winner'].get('name', None)

        return representation
