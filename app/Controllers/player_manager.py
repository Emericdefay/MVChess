# Modules
from app.Models import Player


class PlayerManager:
    """
    Manage the Player Objects.
    """
    def __init__(self):
        """
        Initialize the PlayerManager
        """
        pass

    @staticmethod
    def give_points(id_player: str, id_tournament: str, points: float):
        """
        Give points to a player in a specific tournament.

        Args:
            * *id_player* (str): ID of the player
            * *points* (float): Points given to the player
        """
        player = Player.get(id_player)
        if player:
            player.set_points(id_tournament, points)

    @staticmethod
    def edit_elo(id_player: str, elo: int):
        """
        Edit the elo of a player.

        Args:
            * *id_player* (str): ID of the player
            * *elo* (int): New elo attributes to the player
        """
        player = Player.get(id_player)

        player.set_elo(int(elo))

    @staticmethod
    def create_player(id_player: str):
        """
        Create a new player

            * *id_player* (str): ID of the player created
        """
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
