from random import randint

from app.Models import Tournament
from app.Models import Round
from app.Models import Player
from .player_manager import PlayerManager
from .round_manager import RoundManager


class TournamentManager:
    def __init__(self):
        self.test = True
        self.iter = 1
        pass

    def create_tournament(self, id_tournament: str):
        """

        :param id_tournament:
        :return:
        """
        if not Tournament.get(id_tournament):
            if self.test:
                name_tournament = f"Tournament {id_tournament}"
                number_day_tournament = randint(1, 3)
                dates_tournaments = []
                for i in range(number_day_tournament):
                    day = f"{randint(1, 31)}/{randint(1, 12)}/2021"
                    dates_tournaments.append(day)
                dates_tournaments = " - ".join(map(str, dates_tournaments))
                number_players = 8
                number_rounds = 4
                time_control = 20
                description = "B.T.T.E. : Best tournament's test ever."

            else:
                name_tournament = input("Name the tournament : ")
                number_day_tournament = int(input("How many days will last the tournament : "))
                dates_tournaments = []
                for i in range(number_day_tournament):
                    day = input(f"Date n°{i} : ")
                    dates_tournaments.append(day)
                dates_tournaments = " - ".join(map(str, dates_tournaments))
                number_players = input("How many players : ")
                advised_round = 4
                number_rounds = input(f"How many rounds (by default: {advised_round}) : ")
                number_rounds = number_rounds if number_rounds != "" else advised_round
                time_control = input("How long will last matches (in minutes) : ")
                description = input("Enter the description of the tournament : ")

            Tournament(id_tournament,
                       name_tournament,
                       dates_tournaments,
                       number_players,
                       number_rounds,
                       time_control,
                       description)
        else:
            print("The ID given is already taken, please retry.")

    def add_players(self, id_tournament):
        if Tournament.get(id_tournament):
            if self.test:
                tournament = Tournament.get(id_tournament)
                list_players = []
                for i in range(tournament.number_players):
                    id_player = str(randint(0, 10000))
                    if Player.get(id_player):
                        list_players.append(Player.get(id_player))
                    else:
                        PlayerManager().create_player(id_player)
                        list_players.append(Player.get(id_player))
                tournament.set_players(list_players)
            else:
                tournament = Tournament.get(id_tournament)
                list_players = []
                id_player = None
                for i in range(tournament.number_players):
                    id_player = input(f"Tournament : {tournament.name_tournament}, player {i}/{tournament.number_players}\n"
                                      f"Give the ID of the player that'll play. If it's a new player, please give an unique"
                                      f"ID to register him : ")
                    if Player.get(id_player):
                        list_players.append(Player.get(id_player))
                    else:
                        PlayerManager().create_player(id_player)
                        list_players.append(Player.get(id_player))
                tournament.set_players(Player.get(id_player))
        else:
            raise Exception(f"Tournament ID : {id_tournament} doesn't exist.")

    @staticmethod
    def add_round(id_tournament):
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
    def end_tournament(id_tournament):
        tournament = Tournament.get(id_tournament)
        if tournament:
            tournament.tournament_open = False

