import sys
import os
from operator import attrgetter

from app.Controllers import TournamentManager
from app.Controllers import RoundManager
from app.Controllers import MatchManager
from app.Controllers import PlayerManager
from app.Views import Report
from app.Models import Tournament
from app.Models import Round
from app.Models import Match
from app.Models import Player


def start():
    commands = {"new tournament": new_tournament,
                "new round": new_round,
                "new player": new_player,

                "set round": set_round,
                "set player": set_player,

                "get players -all -alpha": get_all_players_alpha,
                "get players -all -rank": get_all_players_rank,
                "get players -alpha": get_players_alpha,
                "get players -rank": get_players_rank,

                "get tournament -all": get_all_tournaments,
                "get tournament": get_tournament,

                "get round -all": get_all_rounds,
                "get round": get_round,

                "get match -all": get_all_matches,
                "get match": get_match,

                "get flake-report": get_flake_report,
                "commands": list_commands,
                "test": test,
                "exit": close_app
                }
    while True:

        command = input("ChessManager >> ")
        debug = True
        if debug:
            commands[command]()
        else:
            try:
                commands[command]()
            except KeyError:
                print("Wrong command.")

    pass


def new_tournament():
    id_tournament = input("Give ID of tournament :")
    TournamentManager().create_tournament(id_tournament)
    TournamentManager().add_players(id_tournament)
    RoundManager().create_round(f"{id_tournament}:1")


def new_round():
    id_tournament = input("Give ID of the tournament :")
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


def new_player():
    id_player = input("Give an unique ID for the new player :")
    PlayerManager().create_player(id_player)


def set_round():
    id_tournament = input("Give ID of the tournament :")
    print((Tournament.get(id_tournament).rounds))
    id_round = Tournament.get(id_tournament).rounds[-1].id_round
    round_done = False
    for match in Round.get(id_round).matches:
        if (match.player_a_score or match.player_b_score) == match.match_in_progress:
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


def set_player():
    id_player = input("Give ID of the player :")
    elo = input(f"Give the modified elo for {id_player}")
    PlayerManager().edit_elo(id_player, elo)


def get_all_players_alpha():
    players = Player.get_all()
    players = sorted(players, key=attrgetter("first_name"))
    players = sorted(players, key=attrgetter("last_name"))
    Report(players)


def get_all_players_rank():
    players = [player for player in Player.get_all()]
    players = sorted(players, key=attrgetter("points"), reverse=True)
    players = sorted(players, key=attrgetter("elo"), reverse=True)
    Report(players)


def get_players_alpha(id_tournament=None):
    id_tournament = input("Give ID of the tournament :") if id_tournament is None else id_tournament
    players = Tournament.get(id_tournament).players
    players = sorted(players, key=attrgetter("first_name"))
    players = sorted(players, key=attrgetter("last_name"))
    Report(players)


def get_players_rank(id_tournament=None):
    id_tournament = input("Give ID of the tournament :") if id_tournament is None else id_tournament
    players = Tournament.get(id_tournament).players
    players = sorted(players, key=attrgetter("elo"), reverse=True)
    players = sorted(players, key=attrgetter("points"), reverse=True)
    Report(players)


def get_all_tournaments():
    Report(Tournament.get_all())


def get_tournament(id_tournament=None):
    id_tournament = input("Give ID of the tournament :") if id_tournament is None else id_tournament
    Report(Tournament.get(id_tournament))


def get_all_rounds(id_tournament=None):
    id_tournament = input("Give ID of the tournament :") if id_tournament is None else id_tournament
    Report(Round.get_all_from_tournament(id_tournament))


def get_round(id_round=None):
    id_round = input("Give ID of the round :") if id_round is None else id_round
    Report(Round.get(id_round))


def get_all_matches(id_tournament=None):
    id_tournament = input("Give ID of the tournament :") if id_tournament is None else id_tournament
    Report(Match.get_all_from_tournament(id_tournament))


def get_match(id_match=None):
    id_match = input("Give ID of the match :") if id_match is None else id_match
    Report(Match.get(id_match))


def get_flake_report():
    os.system("cd ..")
    os.system("flake8 --format=html --htmldir=flake8_report")


def list_commands():
    pass


def test():
    pass


def close_app():
    sys.exit()
