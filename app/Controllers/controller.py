import sys
import os
from operator import attrgetter

from app.Controllers import TournamentManager
from app.Controllers import RoundManager
from app.Controllers import PlayerManager
from app.Views import Report
from app.Models import Tournament
from app.Models import Round
from app.Models import Player


class Controller:
    """
    Manage the full application by simple commands.
    """

    def __init__(self):
        """
        Initialize the Controller
        """
        pass

    @staticmethod
    def new_tournament():
        """
        Create a new tournament.
        """
        id_tournament = input("Give ID of tournament : ")
        TournamentManager().create_tournament(id_tournament)
        TournamentManager().add_players(id_tournament)
        RoundManager().create_round(f"{id_tournament}:1")
        Tournament.load_from_db()

    @staticmethod
    def new_round():
        """
        Create a new round for a tournament.
        """
        id_tournament = input("Give ID of the tournament : ")
        last_round = Tournament.get(id_tournament).rounds[-1].id_round
        last_round_done = True

        if Tournament.get(id_tournament).tournament_open:
            for match in Round.get(last_round).matches:
                if (match.player_a_score or match.player_b_score) == match.match_in_progress:
                    last_round_done = False
                    break
            if last_round_done:
                next_round = int(last_round.split(":")[-1]) + 1
                next_round = f"{id_tournament}:{next_round}"
                RoundManager().create_round(next_round)
            else:
                print(f"The round {last_round} is not finished yet, you can't create the next round.")
        else:
            print(f"The tournament {id_tournament} is already finished. You cannot create another round.")
        Tournament.load_from_db()

    @staticmethod
    def new_player():
        """
        Create a new player.
        """
        id_player = input("Give an unique ID for the new player : ")
        PlayerManager().create_player(id_player)
        Tournament.load_from_db()

    @staticmethod
    def set_round():
        """
        Set the winners of a round.
        """
        id_tournament = input("Give ID of the tournament : ")
        Report.show_all_rounds(id_tournament)
        id_round = Tournament.get(id_tournament).rounds[-1].id_round
        round_done = False
        for match in Round.get(id_round).matches:
            if (match.player_a_score and match.player_b_score) != match.match_in_progress:
                round_done = True
                break
        if not round_done:
            RoundManager().set_results(id_round)
            RoundManager().round_done(id_round)
            if len(Tournament.get(id_tournament).rounds) == Tournament.get(id_tournament).number_rounds:
                Tournament.get(id_tournament).set_tournament_finished()
        elif round_done and Tournament.get(id_tournament).tournament_open:
            print(f"The round {id_round} is already set, you have to create another round.")
        else:
            print(f"The tournament {id_tournament} is already set and clear. You have to create another tournament.")
        Tournament.load_from_db()

    @staticmethod
    def set_player():
        """
        Edit the elo of a player
        """
        id_player = input("Give ID of the player : ")
        elo = int(input(f"Give the modified elo for {id_player} : "))
        PlayerManager.edit_elo(id_player, elo)
        Tournament.load_from_db()

    @staticmethod
    def get_all_players_alpha():
        """
        Get a sorted list of all players. Sorted by Alpha.
        """
        players = Player.get_all()
        players = sorted(players, key=attrgetter("first_name"))
        players = sorted(players, key=attrgetter("last_name"))
        Report.show_players(players)

    @staticmethod
    def get_all_players_rank():
        """
        Get a sorted list of all players. Sorted by rank.
        """

        players = Player.get_all()
        players = sorted(players, key=attrgetter("elo"), reverse=True)
        Report.show_players(players)

    @staticmethod
    def get_players_alpha(id_tournament=None):
        """
        Get a sorted list of players of a tournament. Sorted by Alpha.

        Arg:
            * *id_tournament* (str): Optional - ID of the tournament
        """
        id_tournament = input("Give ID of the tournament : ") if id_tournament is None else id_tournament
        Report.show_players_alpha(id_tournament)

    @staticmethod
    def get_players_rank(id_tournament=None):
        """
        Get a sorted list of players of a tournament. Sorted by rank.

        Arg:
            * *id_tournament* (str): Optional - ID of the tournament
        """
        id_tournament = input("Give ID of the tournament : ") if id_tournament is None else id_tournament
        Report.show_players_ranked(id_tournament)

    @staticmethod
    def get_all_tournaments():
        """
        Get all tournaments information
        """
        Report.show_all_tournaments()

    @staticmethod
    def get_tournament(id_tournament=None):
        """
        Get specific tournament information

        Arg:
            * *id_tournament* (str): Optional - ID of the tournament
        """
        id_tournament = input("Give ID of the tournament : ") if id_tournament is None else id_tournament
        Report.show_tournament(id_tournament)

    @staticmethod
    def get_all_rounds(id_tournament=None):
        """
        Get all rounds from a tournament

        Arg:
            * *id_tournament* (str): Optional - ID of the tournament
        """
        id_tournament = input("Give ID of the tournament : ") if id_tournament is None else id_tournament
        Report.show_all_rounds(id_tournament)

    @staticmethod
    def get_round(id_round=None):
        """
        Get specific round information

        Arg:
            * *id_round* (str): Optional - ID of the round
        """
        id_round = input("Give ID of the round : ") if id_round is None else id_round
        Report.show_round(id_round)

    @staticmethod
    def get_all_matches(id_tournament=None):
        """
        Get all matches information from a tournament

        Arg:
            * *id_tournament* (str): Optional - ID of the tournament
        """
        id_tournament = input("Give ID of the tournament : ") if id_tournament is None else id_tournament
        Report.show_all_matches(id_tournament)

    @staticmethod
    def get_match(id_match=None):
        """
        Get specific match information

        Arg:
            * *id_match* (str): Optional - ID of the match
        """
        id_match = input("Give ID of the match : ") if id_match is None else id_match
        Report.show_match(id_match)

    @staticmethod
    def load():
        """
        Load data from data_base.json
        Needed to get data from previous sessions.
        """
        Tournament.load_from_db()

    @staticmethod
    def get_flake_report():
        """
        Create a flake8 report at the root of the program.
        """
        os.system("cd ..")
        os.system("flake8 --format=html --htmldir=flake8_report --max-line-length=119")

    @staticmethod
    def list_commands():
        """
        Show all commands with a description.
        """
        commands = {"new tournament": Controller.new_tournament,
                    "new round": Controller.new_round,
                    "new player": Controller.new_player,

                    "set round": Controller.set_round,
                    "set player": Controller.set_player,

                    "get players -all -alpha": Controller.get_all_players_alpha,
                    "get players -all -rank": Controller.get_all_players_rank,
                    "get players -alpha": Controller.get_players_alpha,
                    "get players -rank": Controller.get_players_rank,

                    "get tournament -all": Controller.get_all_tournaments,
                    "get tournament": Controller.get_tournament,

                    "get round -all": Controller.get_all_rounds,
                    "get round": Controller.get_round,

                    "get match -all": Controller.get_all_matches,
                    "get match": Controller.get_match,

                    "load": Controller.load,

                    "get flake-report": Controller.get_flake_report,
                    "commands": Controller.list_commands,
                    "exit": Controller.close_app
                    }

        for key, value in commands.items():
            print(f"{key}{value.__doc__}")

    @staticmethod
    def close_app():
        """
        Close the application.
        """
        Tournament.load_from_db()
        sys.exit()
