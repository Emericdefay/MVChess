from app.Views import Report
from tinydb import TinyDB, Query


class Player:
    """

    """
    players = {}
    data_base = TinyDB("data_base.json")
    players_table = data_base.table("players")

    if players_table:
        players = players_table.all()[0]
    """
    """

    def __init__(self,
                 id_player: str,
                 last_name: str,
                 first_name: str,
                 birthday: str,
                 sex: str,
                 elo: int,
                 **kwargs):
        """

        :param id_player:
        :param last_name:
        :param first_name:
        :param birthday:
        :param sex:
        :param elo:
        :param args:
        """
        self.id_player = id_player
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday
        self.sex = sex
        self.elo = elo

        self.points = kwargs["points"] if len(kwargs) > 0 else 0
        self.matches_passed = kwargs["matches_passed"] if len(kwargs) > 1 else []

        self.update()

    def __repr__(self):
        return f"\tPlayer {self.id_player} alias {self.last_name}\n" \
               f"\t\tElo : {self.elo} | points : {self.points}\n" \
               f"\t\tMatches played : {self.matches_passed}\n"

    def update(self):
        """

        """
        player_dict = {key: value for key, value in vars(self).items()}
        self.players[self.id_player] = player_dict
        #self.serialize()

    def serialize(self):
        self.players_table.truncate()
        self.players_table.insert(self.players)

    def set_points(self, points):
        self.points += points
        self.update()

    def set_elo(self, elo):
        self.elo = elo
        self.update()

    def set_match_played(self, id_tournament_player):
        self.matches_passed.append(id_tournament_player)
        self.update()

    @classmethod
    def get(cls, id_got):
        """

        :param id_got:
        :return:
        """
        db_player = cls.players.get(id_got)
        if db_player:
            player = Player(**db_player)
            player.id_player = id_got
            return player
        return False

    @classmethod
    def get_all(cls):
        """

        :return:
        """
        list_players = []
        for id_got, db_player in cls.players.items():
            player = Player(**db_player)
            player.id_player = id_got
            list_players.append()
        return list_players
