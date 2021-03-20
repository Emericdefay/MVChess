from random import randint
from app.Models import Player


class PlayerManager:
    def __init__(self):
        self.test = True
        pass

    @staticmethod
    def give_points(id_player, points):
        player = Player.get(id_player)
        if player:
            player.set_points(points)

    @staticmethod
    def edit_elo(id_player, elo):
        player = Player.get(id_player)
        player.set_elo(elo)

    def create_player(self, id_player):
        if self.test:
            random_id = id_player
            id_player = f"{random_id}"
            last_name = f"Last{random_id}"
            first_name = f"First{random_id}"
            birthday = f"B{random_id}"
            sex = "Male"
            elo = randint(0, 1000)
        else:
            id_player = id_player
            last_name = input("Last name of the player :")
            first_name = input("First name of the player :")
            birthday = input("Birthday of the player :")
            sex = input("Sex of the player :")
            elo = input("Elo of the player")

        if not Player.get(id_player):
            Player(id_player, last_name, first_name, birthday, sex, elo)
        else:
            raise Exception(f"The ID {id_player} already exists : {Player.get(id_player)}")
