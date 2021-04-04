# Libraries
import datetime
from operator import itemgetter
# Modules
from app.Models import Tournament
from app.Models import Round
from app.Models import Match
from app.Models import Player
from .match_manager import MatchManager


class RoundManager:
    """
    Manage the Rounds Objects.)
    """

    def __init__(self):
        """
        Initialize the RoundManager
        """
        pass

    def create_round(self, id_round: str):
        """
        Create a new round for a tournament.

        Arg:
            * *id_round* (str): ID of the round
        """
        id_tournament = id_round.split(":")[0]
        tournament = Tournament.get(id_tournament)

        if tournament.tournament_open or len(tournament.rounds) >= tournament.number_rounds:
            if not Round.get(id_round):
                times = self.get_times(id_tournament)

                name_round = f"Round {id_round.split(':')[1]}"
                begin_time = times[0]
                end_time = times[1]

                Round(id_round, name_round, begin_time, end_time)
                if tournament.players:
                    pairs = self.create_pairs(id_tournament)
                    matches = []
                    for index, (player_a, player_b) in enumerate(pairs):
                        id_match = f"{id_round}:{index + 1}"
                        match = Match(id_match, player_a, player_b)
                        matches.append(match)
                    Round.get(id_round).set_matches(matches)
                    tournament.add_round(Round.get(id_round))
                    if len(tournament.rounds) >= tournament.number_rounds:
                        tournament.tournament_open = False
            else:
                raise Exception(f"Round {id_round} already exists.")
        else:
            print("The tournament has already reach his maximum rounds number.")

    def create_pairs(self, id_tournament: str, offset=0):
        """
        Create pairs of players that'll play against each other for the next round.

        Args:
            * *id_tournament* (str): ID of the tournament
            * *offset* (int): An offset used when players already played together
        """
        tournament = Tournament.get(id_tournament)

        players = self.sort_players_by_score(id_tournament)
        number_matches = len(players) // 2

        pairs = []

        if self.check_first_round(tournament):
            for i in range(number_matches):
                player_a = players[i]
                player_b = players[i + number_matches]

                pairs.append([player_a, player_b])
            return pairs
        else:
            target = offset
            for i in range(number_matches):
                player_a = players.pop(0)
                player_b = None
                for j in range(target, len(players)):
                    if f"{id_tournament}:{player_a.id_player}" in players[j].matches_passed:
                        if len(players) >= 2:
                            offset += 1
                            return self.create_pairs(id_tournament, offset)
                        if offset > len(players):
                            player_b = players.pop()
                    else:
                        player_b = players.pop(j)
                        break
                target = 0
                pairs.append([player_a, player_b])
        return pairs

    @staticmethod
    def set_results(id_round: str):
        """
        Set the results of the round

        Arg:
            * *id_round* (str): ID of the round to set
        """
        single_round = Round.get(id_round)
        for match in single_round.matches:
            id_match = match.id_match
            dict_result = {"0": -1, "1": match.player_a.id_player, "2": match.player_b.id_player}
            winner = input(f"Match {id_match} | Winner is P1 or P2? (Type 1 for P1, 2 for P2 and 0 if equality) : ")

            if match.player_a_score == match.match_in_progress and match.player_b_score == match.match_in_progress:
                MatchManager().set_winner(id_match, dict_result[winner])
                if match.player_a.id_player == dict_result[winner]:
                    match.set_player_a_score(1.)
                    match.set_player_b_score(0.)
                elif match.player_b.id_player == dict_result[winner]:
                    match.set_player_a_score(0.)
                    match.set_player_b_score(1.)
                else:
                    match.set_player_a_score(0.5)
                    match.set_player_b_score(0.5)
            else:
                print("You cannot edit previous matches.")

    @staticmethod
    def round_done(id_round: str):
        """
        Check if the round is already set

        Arg:
            * *id_round* (str): ID of the round.
        """
        single_round = Round.get(id_round)
        for match in single_round.matches:
            if not MatchManager.match_done(match.id_match):
                return False
        return True

    @staticmethod
    def check_first_round(tournament: object):
        """
        Check if the first round is already set.

        Arg:
            * *tournament* (object): a Tournament instance.
        """
        if not tournament.rounds:
            return True
        else:
            return False

    @staticmethod
    def sort_players_by_score(id_tournament: str):
        """
        Sort the players by score, including also the elo.
            score > elo

        Arg:
            * *id_tournament* (str): ID of the tournament
        """
        players = Tournament.get(id_tournament).players

        list_stats = []
        for player in players:
            list_stats.append({"id_player": player.id_player,
                               "elo": int(player.elo),
                               "score": player.points[id_tournament] if id_tournament in player.points.keys() else 0
                               })
        list_stats = sorted(list_stats, key=itemgetter("elo"), reverse=True)
        list_stats = sorted(list_stats, key=itemgetter("score"), reverse=True)

        list_players = []
        for item in list_stats:
            list_players.append(Player.get(item["id_player"]))

        return list_players

    @staticmethod
    def get_times(id_tournament: str):
        """
        Return list of two elements : time_round_begin, time_round_end
        The format is : Hour:Minute:Second - Day/Month/Year
        """
        time_a = datetime.datetime.now()
        time_a_strf = time_a.strftime("%H:%M:%S - %d/%b/%Y")

        time_added = Tournament.get(id_tournament).time_control
        minutes_added = datetime.timedelta(minutes=time_added)

        time_b = time_a + minutes_added
        time_b_strf = time_b.strftime("%H:%M:%S - %d/%b/%Y")
        return time_a_strf, time_b_strf
