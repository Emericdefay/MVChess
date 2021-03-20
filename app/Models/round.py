from app.Views import Report

from tinydb import TinyDB
import jsons


class Round:
    rounds = {}
    serialized_rounds = {}
    data_base = TinyDB("data_base.json")
    rounds_table = data_base.table("rounds")
    serialized_rounds = rounds_table.all()[0] if rounds_table else {}

    def __init__(self,
                 id_round: str,
                 name_round: str,
                 begin_time: str,
                 end_time: str,
                 **kwargs):
        self.id_round = id_round
        self.name_round = name_round
        self.begin_time = begin_time
        self.end_time = end_time

        self.matches = kwargs["matches"] if len(kwargs) > 0 else []

        self.update()

    def __repr__(self):
        return f"ID : {self.id_round} - {self.name_round}\n" \
               f"Time : {self.begin_time} until {self.end_time}\n" \
               f"{self.matches}"

    def update(self):
        round_dict = {key: value for key, value in vars(self).items()}
        self.rounds[self.id_round] = round_dict

        #self.serialize()

    def serialize(self):
        serial_id_round = self.id_round
        serial_name_round = self.name_round
        serial_begin_time = self.begin_time
        serial_end_time = self.end_time
        serial_matches = jsons.dump(self.matches)
        if serial_matches:
            print(serial_matches)

        serial_round = {
            'id_round': serial_id_round,
            'name_round': serial_name_round,
            'begin_time': serial_begin_time,
            'end_time': serial_end_time,
            'matches': serial_matches
        }
        self.serialized_rounds[self.id_round] = serial_round

        self.rounds_table.truncate()
        self.rounds_table.insert(self.serialized_rounds)

    def set_matches(self, matches):
        self.matches = matches
        self.update()

    @classmethod
    def get(cls, id_round):
        db_round = cls.rounds.get(id_round)
        if db_round:
            single_round = Round(**db_round)
            single_round.id_round = id_round
            return single_round
        return False

    @classmethod
    def get_all_from_tournament(cls, id_tournament):
        list_rounds = []
        for id_round, db_round in cls.rounds.items():
            if id_tournament == id_round.split(":")[0]:
                single_round = Round(*db_round)
                single_round.id_round = id_round
                list_rounds.append(single_round)
        return list_rounds
