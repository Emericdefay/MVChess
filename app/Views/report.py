from operator import itemgetter

from app.Models import Player
from app.Models import Match
from app.Models import Round
from app.Models import Tournament


class Report:
    """

    """
    def __init__(self):
        """
        Initialize the Report
        """
        pass

    @staticmethod
    def show_players(players):
        """
        Show the list of players involved.

        Arg:
            * *players* (list): List of Player objects
        """
        for player in players:
            print(player)

    @staticmethod
    def show_players_alpha(id_tournament):
        """
        Show players sorted by alpha in a tournament

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        players = Tournament.get(id_tournament).players

        sort_list = []
        for player in players:
            sort_list.append({"id_player": player.id_player,
                              "last_name": player.last_name,
                              "first_name": player.first_name})

        sort_list = sorted(sort_list, key=itemgetter("first_name"), reverse=True)
        sort_list = sorted(sort_list, key=itemgetter("last_name"), reverse=True)

        sorted_players = []

        for stats in sort_list:
            id_player = stats["id_player"]
            sorted_players.append(Player.get(id_player))

        for player in sorted_players:
            print(player, end="")
            score = player.points[id_tournament] if id_tournament in player.points.keys() else 0
            print(f"\t\t\t\t Score : {score}")

    @staticmethod
    def show_players_ranked(id_tournament):
        """
        Show players sorted by rank in a tournament

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        players = Tournament.get(id_tournament).players

        sort_list = []
        for player in players:
            sort_list.append({"id_player": player.id_player,
                              "points": player.points[id_tournament] if id_tournament in player.points.keys() else 0,
                              "elo": int(player.elo)})

        sort_list = sorted(sort_list, key=itemgetter("elo"), reverse=True)
        sort_list = sorted(sort_list, key=itemgetter("points"), reverse=True)

        sorted_players = []

        for stats in sort_list:
            id_player = stats["id_player"]
            sorted_players.append(Player.get(id_player))

        for player in sorted_players:
            print(player, end="")
            score = player.points[id_tournament] if id_tournament in player.points.keys() else 0
            print(f"\t\t\t\t Score : {score}")

    @staticmethod
    def show_all_tournaments():
        """
        Show all tournaments created.
        """
        all_tournaments = Tournament.get_all()
        for tournament in all_tournaments:
            print(tournament)

    @staticmethod
    def show_tournament(id_tournament):
        """
        Show a specific tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        tournament = Tournament.get(id_tournament)
        print(tournament)

    @staticmethod
    def show_all_rounds(id_tournament):
        """
        Show all rounds from a tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        all_rounds = Round.get_all_from_tournament(id_tournament)
        for single_round in all_rounds:
            print(single_round)

    @staticmethod
    def show_round(id_round):
        """
        Show a specific round from a tournament.

        Arg:
            * *id_round* (str): ID of the round
        """
        single_round = Round.get(id_round)
        print(single_round)

    @staticmethod
    def show_all_matches(id_tournament):
        """
        Show all matches from a tournament.

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        all_matches = Match.get_all_from_tournament(id_tournament)
        for match in all_matches:
            print(match)

    @staticmethod
    def show_match(id_match):
        """
        Show a specific match from a tournament

        Arg:
            * *id_match* (str): ID of the match
        """
        match = Match.get(id_match)
        print(match)
