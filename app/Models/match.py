from app.Views import Report
from tinydb import TinyDB, Query
import jsons
from .player import Player


class Match:
    matches = {}
    serialized_matches = {}
    data_base = TinyDB("data_base.json")
    matches_table = data_base.table("matches")
    serialized_matches = matches_table.all()[0] if matches_table else {}

    def __init__(self,
                 id_match: str,
                 player_a: object,
                 player_b: object,
                 **kwargs):
        self.id_match = id_match
        self.player_a = player_a
        self.player_b = player_b

        self.match_in_progress = "..."
        self.player_a_score = kwargs["player_a_score"] if len(kwargs) > 0 else self.match_in_progress
        self.player_b_score = kwargs["player_b_score"] if len(kwargs) > 1 else self.match_in_progress

        self.update()

    def __repr__(self):
        return f"Match : {self.id_match}\n" \
               f"P1 : {self.player_a} \t\t\t\t\t\t Score:{self.player_a_score}\n" \
               f"P2 : {self.player_b} \t\t\t\t\t\t Score:{self.player_b_score}\n"

    def update(self):
        match_dict = {key: value for key, value in vars(self).items()}
        self.matches[self.id_match] = match_dict

        #self.save_to_db()

    def save_to_db(self):
        self.serialize()
        # self.deserialize()

    def serialize(self):
        serial_id_match = self.id_match
        serial_player_a = self.player_a
        serial_player_b = self.player_b
        serial_match_in_progress = self.match_in_progress
        serial_player_a_score = self.player_a_score
        serial_player_b_score = self.player_b_score

        # serialize players
        serial_player_a = jsons.dump(serial_player_a)
        del serial_player_a["players_table"]
        del serial_player_a["players"]
        serial_player_b = jsons.dump(serial_player_b)
        del serial_player_b["players"]
        del serial_player_b["players_table"]

        serial_match = {
            'id_match': serial_id_match,
            'player_a': serial_player_a,
            'player_b': serial_player_b,
            'match_in_progress': serial_match_in_progress,
            'player_a_score': serial_player_a_score,
            'player_b_score': serial_player_b_score
        }
        self.serialized_matches[self.id_match] = serial_match

        self.matches_table.truncate()
        self.matches_table.insert(self.serialized_matches)

    def deserialize(self):
        # VALID ?
        match = self.serialized_matches[str(self.id_match)]
        if match:
            if match["player_a"]:
                # del match["player_a"]["players"]
                match["player_a"] = jsons.load(match["player_a"], Player)
            if match["player_b"]:
                # del match["player_b"]["players"]
                match["player_b"] = jsons.load(match["player_b"], Player)
        self.matches[str(self.id_match)] = match

    def set_player_a_score(self, score):
        self.player_a_score = score
        self.update()

    def set_player_b_score(self, score):
        self.player_b_score = score
        self.update()

    @classmethod
    def get(cls, id_match):
        db_match = cls.matches.get(id_match)
        if db_match:
            match = Match(**db_match)
            match.id_match = id_match
            return match
        return False

    @classmethod
    def get_all_from_tournament(cls, id_tournament):
        list_matches = []
        for id_match, db_match in cls.matches.items():
            if id_match.split(":")[0] == id_tournament:
                match = Match(**db_match)
                match.id_match = id_match
                list_matches.append(match)
        return list_matches
