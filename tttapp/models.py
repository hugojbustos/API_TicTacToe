from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=1)

    def __str__(self) -> str:
        return self.name


class Game(models.Model):
    players = models.ManyToManyField(Player, related_name='games_played')
    starting_player = models.ForeignKey(Player, on_delete=models.CASCADE,
                                        related_name='games_started')
    movements_played = models.IntegerField(default=0)
    next_turn = models.ForeignKey(Player, on_delete=models.CASCADE,
                                  related_name='next_turn')
    board = models.JSONField(default=list)
    winner = models.ForeignKey(Player, null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='games_won')

    def __str__(self) -> str:
        return f'Game number #{self.id}'

    def make_move(self, player, row, column):
        if self.winner or self.movements_played >= 9 or not \
                       (0 <= row < 3 and 0 <= column < 3) or \
                       self.board[row][column] is not None or \
                       player != self.next_turn:
            return False

        self.board[row][column] = player.symbol
        self.movements_played += 1

        if self.check_winner(player):
            self.winner = player
        elif self.movements_played == 9:
            self.winner = None

        self.next_turn = self.players.exclude(id=player.id).first()
        self.save()
        return True

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player.symbol for j in range(3)):
                return True
            if all(self.board[j][i] == player.symbol for j in range(3)):
                return True

        if all(self.board[i][i] == player.symbol for i in range(3)) or \
           all(self.board[i][2 - i] == player.symbol for i in range(3)):
            return True

        return False
