import datetime
from operator import attrgetter

from app.Models import Round
from app.Models import Tournament
from app.Models import Match
from .match_manager import MatchManager


class RoundManager:
    def __init__(self):
        pass

    def create_round(self, id_round):
        if not Round.get(id_round):
            id_tournament = id_round.split(":")[0]
            times = self.get_times(id_tournament)

            name_round = f"Round {id_round}"
            begin_time = times[0]
            end_time = times[1]

            Round(id_round, name_round, begin_time, end_time)
            if Tournament.get(id_tournament).players:
                pairs = self.create_pairs(id_tournament)
                matches = []
                for index, (player_a, player_b) in enumerate(pairs):
                    id_match = f"{id_round}:{index+1}"
                    match = Match(id_match, player_a, player_b)
                    matches.append(match)
                Round.get(id_round).set_matches(matches)
                Tournament.get(id_tournament).add_round(Round.get(id_round))
        else:
            raise Exception(f"Round {id_round} already exists.")

    def create_pairs(self, id_tournament, offset=0):
        tournament = Tournament.get(id_tournament)
        players = tournament.players

        players = self.sort_players_by_score(players)
        number_matches = len(players)//2

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
                            raise Exception("Must redefine algo:")
                    else:
                        player_b = players.pop(j)
                        break
                target = 0
                pairs.append([player_a, player_b])
        return pairs

    @staticmethod
    def set_results(id_round):
        single_round = Round.get(id_round)
        for match in single_round.matches:
            id_match = match.id_match
            id_player = input(f"Match {id_match} | Give ID of the winner (if equality: -1) :")
            if match.player_a_score == match.match_in_progress and match.player_b_score == match.match_in_progress:
                MatchManager().set_winner(id_match, id_player)
                if match.player_a.id_player == id_player:
                    match.set_player_a_score(1)
                    match.set_player_b_score(0)
                elif match.player_b.id_player == id_player:
                    match.set_player_a_score(0)
                    match.set_player_b_score(1)
                else:
                    match.set_player_a_score(0.5)
                    match.set_player_b_score(0.5)
            else:
                print("You cannot edit previous matches.")

    @staticmethod
    def round_done(id_round):
        single_round = Round.get(id_round)
        for match in single_round.matches:
            if not MatchManager.match_done(match.id_match):
                return False
        return True

    @staticmethod
    def check_first_round(tournament):
        if not tournament.rounds:
            return True
        else:
            return False

    @staticmethod
    def sort_players_by_score(players):
        players = sorted(players, key=attrgetter("elo"))
        players = sorted(players, key=attrgetter("points"))
        return players

    @staticmethod
    def get_times(id_tournament):
        """
        :return: return list of two elements : time_round_begin, time_round_end
        """
        time_a = datetime.datetime.now()
        time_a_strf = time_a.strftime("%H:%M:%S - %d/%b/%Y")

        time_added = Tournament.get(id_tournament).time_control
        minutes_added = datetime.timedelta(minutes=time_added)

        time_b = time_a + minutes_added
        time_b_strf = time_b.strftime("%H:%M:%S - %d/%b/%Y")
        return time_a_strf, time_b_strf
