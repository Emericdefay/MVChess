from app.Models import Match


class MatchManager:
    def __init__(self):
        pass

    @staticmethod
    def create_match(id_match, player_a, player_b):
        Match(id_match, player_a, player_b)

    @staticmethod
    def set_winner(id_match, id_player):
        match = Match.get(id_match)
        if match.player_a_score == match.match_in_progress and match.player_b_score == match.match_in_progress:
            if match.player_a.id_player == id_player:
                match.player_a.set_points(1)
            elif match.player_b.id_player == id_player:
                match.player_b.set_points(1)
            else:
                match.player_a.set_points(0.5)
                match.player_b.set_points(0.5)
            id_tournament = id_match.split(":")[0]
            match.player_a.set_match_played(f"{id_tournament}:{match.player_b.id_player}")
            match.player_b.set_match_played(f"{id_tournament}:{match.player_a.id_player}")
        else:
            print("Can't edit score.")

    @staticmethod
    def match_done(id_match):
        match = Match.get(id_match)
        if (match.player_a_score and match.player_b_score) != match.match_in_progress:
            return True
        else:
            return False
