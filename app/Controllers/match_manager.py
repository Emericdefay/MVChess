# Modules
from app.Models import Match


class MatchManager:
    """
    Manage the Match Objects.
    """
    def __init__(self):
        """
        Initialize the MatchManager
        """
        pass

    @staticmethod
    def create_match(id_match: str, player_a: object, player_b: object):
        """
        Create a match between player A & B.

        Args:
            * *id_match* (str): ID of the match
            * *player_a* (object): First player involved
            * *player_b* (object): Second player involved
        """
        Match(id_match, player_a, player_b)

    @staticmethod
    def set_winner(id_match: str, id_player: str):
        """
        Set the winner of a match.

        Args:
            * *id_match* (str): ID of the match
            * *id_player* (str): ID of the player
        """
        match = Match.get(id_match)
        id_tournament = id_match.split(":")[0]

        if match.player_a_score == match.match_in_progress and match.player_b_score == match.match_in_progress:
            if match.player_a.id_player == id_player:
                match.player_a.set_points(id_tournament, 1)
            elif match.player_b.id_player == id_player:
                match.player_b.set_points(id_tournament, 1)
            else:
                match.player_a.set_points(id_tournament, 0.5)
                match.player_b.set_points(id_tournament, 0.5)

            match.player_a.set_match_played(f"{id_tournament}:{match.player_b.id_player}")
            match.player_b.set_match_played(f"{id_tournament}:{match.player_a.id_player}")
        else:
            print("Can't edit score.")

    @staticmethod
    def match_done(id_match: str):
        """
        Set the match done

        Arg:
            * *id_match* (str): ID of the match
        """
        match = Match.get(id_match)
        if (match.player_a_score and match.player_b_score) != match.match_in_progress:
            return True
        else:
            return False
