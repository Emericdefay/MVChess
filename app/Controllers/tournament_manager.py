# Libraries
from random import randint
# Modules
from app.Models import Tournament
from app.Models import Player
from .player_manager import PlayerManager
from .round_manager import RoundManager


class TournamentManager:
    """
    Manage the Tournament Object.
    """

    def __init__(self):
        """
        Initialize an instance of Tournament.
        """
        pass

    @staticmethod
    def create_tournament(id_tournament: str):
        """
        Create a new tournament.

        Arg:
            * *id_tournament* (str): ID of the **new** tournament
        """
        if not Tournament.get(id_tournament):
            name_tournament = input("Name the tournament : ")
            place_tournament = str(input("Where does the tournament happen : "))
            number_day_tournament = int(input("How many days will last the tournament : "))
            dates_tournaments = []
            for i in range(number_day_tournament):
                day = input(f"Date n°{i} : ")
                dates_tournaments.append(day)
            dates_tournaments = " - ".join(map(str, dates_tournaments))
            number_players = int(input("How many players : "))
            advised_round = 4
            number_rounds = input(f"How many rounds (by default: {advised_round}) : ")
            number_rounds = number_rounds if number_rounds != "" else advised_round
            time_control = int(input("How long will last matches (in minutes) : "))
            description = input("Enter the description of the tournament : ")

            Tournament(id_tournament,
                       name_tournament,
                       place_tournament,
                       dates_tournaments,
                       number_players,
                       number_rounds,
                       time_control,
                       description)
            return True
        else:
            print("The ID given is already taken.")
            return False

    @staticmethod
    def add_players(id_tournament: str):
        """
        Add players (new or not) to the tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        tournament = Tournament.get(id_tournament)
        if tournament and not tournament.rounds:
            tournament = Tournament.get(id_tournament)
            list_players = []
            for i in range(tournament.number_players):
                id_player = input(f"Tournament : {tournament.name_tournament},"
                                  f" player {i + 1}/{tournament.number_players}\n"
                                  f"Give the ID of the player that'll play. "
                                  f"If it's a new player, please give an unique"
                                  f"ID to register him : ")
                if Player.get(id_player) in list_players:
                    print("This player is already playing this tournament! Please retry : ")
                    id_player = input(f"Tournament : {tournament.name_tournament},"
                                      f" player {i + 1}/{tournament.number_players}\n"
                                      f"Give the ID of the player that'll play. "
                                      f"If it's a new player, please give an unique"
                                      f"ID to register him : ")
                if Player.get(id_player) and Player.get(id_player) not in list_players:
                    list_players.append(Player.get(id_player))
                elif Player.get(id_player) in list_players:
                    raise ("A player has been recorded twice for the same tournament two time in a raw."
                           "Please recreate the same tournament and add 8 different players; ")
                else:
                    PlayerManager().create_player(id_player)
                    list_players.append(Player.get(id_player))
            tournament.set_players(list_players)
            for player in list_players:
                player.tournaments_played.append(id_tournament)
        else:
            raise Exception(f"Tournament ID : {id_tournament} does not exist.")

    @staticmethod
    def add_round(id_tournament: str):
        """
        Add a round on the tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        tournament = Tournament.get(id_tournament)
        if tournament:
            if tournament.tournament_open:
                if len(tournament.rounds) < tournament.number_rounds:
                    id_round = f"{len(tournament.rounds)}"
                    RoundManager().create_round(id_round)
                else:
                    raise Exception("Maximum rounds for this tournament is already reached")
            else:
                raise Exception("The Tournament is already finished")
        else:
            raise Exception(f"There is no tournament : {id_tournament}")

    @staticmethod
    def end_tournament(id_tournament: str):
        """
        Set the tournament closed.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        tournament = Tournament.get(id_tournament)
        if tournament:
            tournament.tournament_open = False
