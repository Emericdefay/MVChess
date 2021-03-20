from tinydb import TinyDB, Query
import jsons

from .player import Player
from .round import Round


class Tournament:
    """

    """
    tournaments = {}
    serialized_tournaments = {}
    data_base = TinyDB("data_base.json")
    tournaments_table = data_base.table("tournaments")
    serialized_tournaments = tournaments_table.all()[0] if tournaments_table else {}
    """ tournaments encompass every tournament ever made.
    """

    def __init__(self,
                 id_tournament: str,
                 name_tournament: str,
                 date: str,
                 number_players: int,
                 number_rounds: int,
                 time_control: int,
                 description: str,
                 **kwargs):

        # Shared variables:
        self.id_tournament = id_tournament
        self.name_tournament = name_tournament
        self.date = date
        self.number_players = number_players
        self.number_rounds = number_rounds
        self.time_control = time_control
        self.description = description

        # Own variables:
        self.players = kwargs["players"] if len(kwargs) > 0 else False
        self.rounds = kwargs["rounds"] if len(kwargs) > 1 else []
        self.tournament_open = kwargs["tournament_open"] if len(kwargs) > 2 else True

        self.update()

    def __repr__(self):
        return f"ID : {self.id_tournament} ," \
               f"Name : {self.name_tournament}\n" \
               f"Date(s) : {self.date}\n" \
               f"nb. players : {self.number_players}\n" \
               f"nb. rounds : {self.number_rounds}\n" \
               f"Duration of matches : {self.time_control}\n" \
               f"\t{self.description}\n" \
               f"{self.players}\n" \
               f"{self.rounds}\n" \
               f"{self.tournament_open}"

    def update(self):

        tournament_dict = {key: value for key, value in vars(self).items()}
        self.tournaments[self.id_tournament] = tournament_dict

        #self.save_to_db()

    def save_to_db(self):
        self.serialize()
        #self.deserialize()

    def load_from_db(self):
        data_base = TinyDB("data_base.json")
        tournaments_table = data_base.table("tournaments")
        self.tournaments = tournaments_table.all()[0] if tournaments_table else {}
        self.deserialize()
        # return self.tournaments

    def deserialize(self):
        # VALID ?
        tournament = self.serialized_tournaments.get(str(self.id_tournament))
        if tournament:
            if tournament["players"]:
                for index, player in enumerate(tournament["players"]):
                    tournament["players"][index] = jsons.load(player, Player)
            if tournament["rounds"]:
                for index, single_round in enumerate(tournament["rounds"]):
                    tournament["rounds"][index] = jsons.load(single_round, Round)
        self.tournaments[str(self.id_tournament)] = tournament

    def serialize(self):

        serial_id_tournament = self.id_tournament
        serial_name_tournament = self.name_tournament
        serial_date = self.date
        serial_number_players = self.number_players
        serial_number_rounds = self.number_rounds
        serial_time_control = self.time_control
        serial_description = self.description
        serialized_players = jsons.dump(self.tournaments.get(self.id_tournament)["players"])
        serialized_rounds = jsons.dump(self.tournaments.get(self.id_tournament)["rounds"])
        serial_open = self.tournament_open

        serial_tournament = {
            'id_tournament': serial_id_tournament,
            'name_tournament': serial_name_tournament,
            'date': serial_date,
            'number_players': serial_number_players,
            'number_rounds': serial_number_rounds,
            'time_control': serial_time_control,
            'description': serial_description,
            'players': serialized_players,
            'rounds': serialized_rounds,
            'tournament_open': serial_open
        }
        self.serialized_tournaments[self.id_tournament] = serial_tournament

        self.tournaments_table.truncate()
        self.tournaments_table.insert(self.serialized_tournaments)

    def set_players(self, players):
        self.players = players
        self.update()

    def add_round(self, single_round):
        self.rounds.append(single_round)
        self.update()

    def set_tournament_finished(self):
        self.tournament_open = False
        self.update()

    @classmethod
    def get(cls, id_got: str):
        """
        Get a specific tournament regarding its <id_tournament>.

        :param id_got:
        :rtype id_got:

        :return:
        """
        db_tournament = cls.tournaments.get(id_got)
        if db_tournament:
            tournament = Tournament(**db_tournament)
            tournament.id_tournament = id_got
            return tournament
        return False

    @classmethod
    def get_all(cls):
        """
        :return: Return list of all tournaments
        """
        list_tournament = []
        for id_got, db_tournament in cls.tournaments.items():
            tournament = Tournament(**db_tournament)
            tournament.id_tournament = id_got
            list_tournament.append(tournament)
        return list_tournament
