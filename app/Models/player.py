from tinydb import TinyDB


class Player:
    """
    Players Objects are structured without any objects inside.
    They are quite easy to manipulate. There are the steps that manipulate an instance :

        1. Initialize
    Player instance is created
        2. Update
    Player instance is pasted in a dictionary, for save purpose. ( dictionary : *players*)
        3. Ready to Work
    Player instance is already to be manipulate. When the program is launch, the serials are called from the
    data_base and transformed into objects.
    """

    players = {}
    data_base = TinyDB("data_base.json", sort_keys=True, indent=4, separators=(',', ': '))
    players_table = data_base.table("players")
    players = players_table.all()[0] if players_table else {}
    """
    Class parameters:
        * *players* (dict): Keep all players SERIALS in a dictionary. Ready to be transformed and used away
        * *data_base* (list): TinyDB list where serials are saved.
        * *players_table* (list): Specific TinyDB data_base region where players are saved.
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
        Initialize a player.

        Args:
            * *id_player* (str): ID of the player, unique. e.g: "20156"
            * *last_name* (str): Last name of the player
            * *first_name* (str): First name of the player
            * *birthday* (str): Birthday of the player. e.g: "01/01/2000"
            * *sex* (str): Gender of the player
            * *elo* (int): Elo of the player, positive number. e.g: 715

        Keyword Args:
            * *points* (dict): Points(b) won by the player during a tournament(a). e.g: {"1": 12.5}
            * *matches_played* (list): List of matches player by a player in a tournament. e.g: ["1:155"]
            * *score* (float) : Points won on the current tournament.
        """
        self.id_player = str(id_player)
        self.last_name = str(last_name)
        self.first_name = str(first_name)
        self.birthday = str(birthday)
        self.sex = str(sex)
        self.elo = int(elo)

        self.tournaments_played = kwargs["tournaments_played"] if len(kwargs) > 0 else []
        self.points = kwargs["points"] if len(kwargs) > 1 else {}
        self.matches_passed = kwargs["matches_passed"] if len(kwargs) > 2 else []
        self.score = int(kwargs["score"]) if len(kwargs) > 3 else 0

        self.update()

    def __str__(self):
        """
        Describe the player like this:
            >> print(player)
            Player : 15201 alias Smith
                Elo : 100
                Matches played : ["1:201","1:125"]
        """
        return f"Player {self.id_player} alias {self.last_name}\n" \
               f"\t\t\t\t   Elo : {self.elo}\n" \
               f"\t\tMatches played : {self.matches_passed}\n"

    def update(self):
        """
        The update function save the attributes of an instance in the class attribute : *players*.

        Steps:
            1. Make a dictionary with all attributes of the instance.
            2. Add this dictionary to the *players* dictionary at the key: *self.player*.
            3. Update the data_base.json file
        """
        player_dict = {key: value for key, value in vars(self).items()}
        if self.id_player in self.players.keys():
            self.players[self.id_player].update(player_dict)
        else:
            self.players[self.id_player] = player_dict

        self.players_table.truncate()
        self.players_table.insert(self.players)

    def set_points(self, id_tournament: str, points: float):
        """
        Add *points* to the player's points attribute for a *tournament*.

        Args:
            * *id_tournament* (str): Tournament where points need to be applied.
            * *points* (float): Points to add to this tournament.
        """
        if id_tournament in self.points.keys():
            self.points[id_tournament] += int(points)
        else:
            self.points[id_tournament] = 0
            self.points[id_tournament] += int(points)
        self.score = self.points[id_tournament]
        self.update()

    def set_elo(self, elo: int):
        """
        Set the player elo.

        Arg:
            * *elo* (int): The elo given to the player.
        """
        self.elo = int(elo)
        self.update()

    def set_match_played(self, id_tournament_player: str):
        """
        Add the match played in the *matches_played* list.

        Arg:
            * *id_tournament_player* (str): The match played. i.e: "1:125"
        """
        self.matches_passed.append(id_tournament_player)
        self.update()

    @classmethod
    def get(cls, id_got: str):
        """
        Get a specific player giving its unique ID.

        Arg:
            * *id_got* (str): ID of the player. i.e: "1654"
        """

        db_player = cls.players.get(id_got)
        if db_player:
            player = Player(**db_player)
            player.id_player = id_got
            return player
        return False

    @classmethod
    def get_serialized(cls, id_player: str):
        """
        Get a specific player serialized from it's ID.

        Arg:
            * *id_player* (str): ID of the player. i.e: "1654"
        """
        return cls.players.get(id_player)

    @classmethod
    def get_serialized_from_tournament(cls, id_tournament: str):
        """
        Get all players serialized from a specific tournament.

        Arg:
            * *id_tournament* (str): ID of the specific tournament. i.e: "10"
        """
        list_players = []
        for id_got, db_player in cls.players.items():
            if id_tournament in db_player["tournaments_played"]:
                list_players.append(db_player)
        return list_players

    @classmethod
    def get_all(cls):
        """
        Get all players register.
        """
        list_players = []
        for id_got, db_player in cls.players.items():
            player = Player(**db_player)
            player.id_player = id_got
            list_players.append(player)
        return list_players
