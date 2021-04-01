from random import randint
from app.Models import Player


class PlayerManager:
    """
    Manage the Player Objects.
    """
    def __init__(self):
        """
        Initialize the PlayerManager
        """
        self.test = False
        pass

    @staticmethod
    def give_points(id_player, id_tournament, points):
        """
        Give points to a player

        Args:
            * *id_player* (str): ID of the player
            * *points* (float):
        """
        player = Player.get(id_player)
        if player:
            player.set_points(id_tournament, points)

    @staticmethod
    def edit_elo(id_player, elo):
        """
        Edit the elo of a player.

        Args:
            * *id_player* (str): ID of the player
            * *elo* (int): New elo attributes to the player
        """
        player = Player.get(id_player)

        player.set_elo(int(elo))

    def create_player(self, id_player):
        """
        Create a new player

            * *id_player* (str): ID of the player created
        """
        if self.test:
            random_id = id_player
            id_player = f"{random_id}"
            last_name = f"Last{random_id}"
            first_name = f"First{random_id}"
            birthday = f"B{random_id}"
            sex = "Male"
            elo = randint(0, 1000)
        else:
            id_player = str(id_player)
            last_name = input("Last name of the player : ")
            first_name = input("First name of the player : ")
            birthday = input("Birthday of the player : ")
            sex = input("Sex of the player : ")
            elo = int(input("Elo of the player: "))

        if not Player.get(id_player):
            Player(id_player, last_name, first_name, birthday, sex, elo)
        else:
            raise Exception(f"The ID {id_player} already exists : {Player.get(id_player)}")
