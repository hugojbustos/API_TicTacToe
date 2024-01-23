from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Game, Player
from .serializers import GameSerializer, SubmitPlaySerializer, \
                         GameListSerializer, \
                         SingleGameSerializer


class CreateGameView(APIView):
    def post(self, request, format=None):
        players_data = request.data.get('players', [])
        starting_player_name = request.data.get('starting_player', '')

        if len(players_data) != 2:
            return Response({'error': 'Exactly two players are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            starting_player = next(player for player in players_data
                                   if player['name'] == starting_player_name)
        except StopIteration:
            return Response({'error': 'Starting player not found in the \
                             players list.'},
                            status=status.HTTP_400_BAD_REQUEST)

        players = [Player.objects.create(**player, symbol='X'
                   if player == starting_player else 'O')
                   for player in players_data]

        game = Game.objects.create(starting_player=players[0],
                                   next_turn=players[0])

        game.players.set(players)

        game.board = [[None, None, None], [None, None, None],
                      [None, None, None]]
        game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SubmitPlayView(APIView):
    def post(self, request, format=None):
        serializer = SubmitPlaySerializer(data=request.data)
        if serializer.is_valid():
            game_id = serializer.validated_data['game_id']
            player_name = serializer.validated_data['player']
            row = serializer.validated_data['row']
            column = serializer.validated_data['column']

            try:
                game = Game.objects.get(pk=game_id)
            except Game.DoesNotExist:
                return Response({'error': 'Game not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            players = Player.objects.filter(name=player_name)

            if not players.exists():
                return Response({'error': 'Player not found.'},
                                status=status.HTTP_404_NOT_FOUND)

            player = players.first()

            if game.winner or game.movements_played >= 9:
                serializer = GameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if game.make_move(player, row, column):
                serializer = GameSerializer(game)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                error_message = 'Invalid move. ' \
                                'Check if it is the correct player\'s ' \
                                'turn or the cell is already occupied.'
                return Response({'error': error_message},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class GameListView(generics.ListAPIView):
    serializer_class = GameListSerializer

    def get_queryset(self):
        option = self.kwargs.get('option', 'all')
        limit = self.kwargs.get('limit', None)

        if option == 'all':
            queryset = Game.objects.all()
        elif option == 'finished':
            queryset = Game.objects.filter(winner__isnull=False) | \
                Game.objects.filter(movements_played=9)
        elif option == 'not_finished':
            queryset = Game.objects.filter(winner__isnull=True) & \
                Game.objects.filter(movements_played__lte=9)
        else:
            return Response({'error': 'Invalid option.'}, status=400)

        if limit:
            queryset = queryset[:limit]

        return queryset


class SingleGameView(APIView):
    def get(self, request, game_id, format=None):
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = SingleGameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteGameView(APIView):
    def delete(self, request, game_id, format=None):
        try:
            game = Game.objects.get(pk=game_id)
            game.delete()
            return Response({'message': 'Game deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found.'},
                            status=status.HTTP_404_NOT_FOUND)
