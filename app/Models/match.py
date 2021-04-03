from tinydb import TinyDB
from .player import Player


class Match:
    """
    Matches Objects are structured with many objects inside.
    With the data_base, those objects need to be serialized.
    There are the steps that manipulate an instance :

        1. Initialize
    Match instance is created
        2. Update
    Match instance is pasted in a dictionary, for save purpose. ( dictionary : *matches*)
        3. Serialize
    Match instance is serialized in another dictionary, but this time, the objects inside the instance are also
    serialized.
        4. Ready to Work
    Match instance is ready to be manipulate. When the program is launch, the serials are called from the
    data_base and transformed into objects.
    """

    matches = {}
    serialized_matches = {}
    data_base = TinyDB("data_base.json", sort_keys=True, indent=4, separators=(',', ': '))
    matches_table = data_base.table("matches")
    serialized_matches = matches_table.all()[0] if matches_table else {}
    """
    Class parameters:
        * *matches* (dict): Keep all matches in a dictionary, allow them to be used away
        * *serialized_matches* (dict): Serials from all matches attributes, ready to be convert into objects.
        * *data_base* (list): TinyDB list where serials are saved.
        * *matches_table* (list): Specific TinyDB data_base region where serialized matches are saved.
    """

    def __init__(self,
                 id_match: str,
                 player_a: object,
                 player_b: object,
                 **kwargs):
        """
        Initialize a match.

        Args:
            * *id_match* (str): ID of the match, composed as "<ID_tournament>:<ID_round>:<ID_match>". e.g: "1:1:1"
            * *player_a* (object): First player object
            * *player_b* (object): Second player object

        Keyword Args:
            * *player_a_score* (float): Score of player_a for this match
            * *player_b_score* (float): Score of player_b for this match
        """
        self.id_match = id_match
        self.player_a = player_a
        self.player_b = player_b

        self.match_in_progress = "..."
        self.player_a_score = kwargs["player_a_score"] if len(kwargs) > 0 else self.match_in_progress
        self.player_b_score = kwargs["player_b_score"] if len(kwargs) > 1 else self.match_in_progress

        self.update()

    def __str__(self):
        """
        Describe the match like this:
            >> print(match)
            Match : 1:1:1
            P1 : *player_a* object Score : ...
            P2 : *player_b* object Score : ...
        """
        return f"\033[1mMatch : {self.id_match}\033[0m\n" \
               f"\tP1 : {self.player_a} \t\t\t\t Score : {self.player_a_score}\n" \
               f"\t\t\t\t\t\033[1m Versus \033[0m \n" \
               f"\tP2 : {self.player_b} \t\t\t\t Score : {self.player_b_score}\n"

    def update(self):
        """
        The update function save the attributes of an instance in the class attribute : *matches*.

        Steps:
            1. Make a dictionary with all attributes of the instance.
            2. Add this dictionary to the *matches* dictionary at the key: *self.id_match*.
        """
        match_dict = {key: value for key, value in vars(self).items()}
        if self.id_match in self.matches.keys():
            self.matches[self.id_match].update(match_dict)
        else:
            self.matches[self.id_match] = match_dict
        self.serialize()

    def serialize(self):
        """
        Serialize objects.
        """
        serial_id_match = self.id_match
        serial_match_in_progress = self.match_in_progress
        serial_player_a_score = self.player_a_score
        serial_player_b_score = self.player_b_score

        # serialize players
        id_player_a = self.player_a.id_player
        serial_player_a = Player.get_serialized(id_player_a)

        id_player_b = self.player_b.id_player
        serial_player_b = Player.get_serialized(id_player_b)

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

    def set_player_a_score(self, score: float):
        """
        Set the player_a score attribute

        Arg:
            * *score* (float): Score of player_b for this match. i.e: 0.5
        """
        self.player_a_score = score
        self.update()

    def set_player_b_score(self, score: float):
        """
        Set the player_b score attribute

        Args:
            * *score* (float): Score of player_b for this match. i.e: 0.5
        """
        self.player_b_score = score
        self.update()

    @classmethod
    def get(cls, id_match: str):
        """
        Get a specific match giving its unique ID.

        Arg:
            * *id_match* (str): ID of the match, composed as "<ID_tournament>:<ID_round>:<ID_match>". i.e: "1:1:1"
        """
        db_match = cls.matches.get(id_match)
        if db_match:
            match = Match(**db_match)
            return match
        return False

    @classmethod
    def get_from_round(cls, id_round: str):
        """
        Get all matches from a round of a tournament. Giving the Id of the round.

        Arg:
            * *id_round* (str) : ID of the round. i.e: "1:1"
        """
        list_matches = []
        tournament_number = id_round.split(":")[0]
        round_number = id_round.split(":")[1]

        for id_match, db_match in cls.serialized_matches.items():
            if id_match.split(":")[0] == tournament_number:
                if id_match.split(':')[1] == round_number:
                    list_matches.append(db_match)
        return list_matches

    @classmethod
    def get_all_from_tournament(cls, id_tournament: str):
        """
        Get all matches from a tournament, giving them tournament's ID.

        Arg:
            * *id_tournament* (str): ID of the tournament. i.e: "1"
        """
        list_matches = []
        for id_match, db_match in cls.matches.items():
            if id_match.split(":")[0] == id_tournament:
                match = Match(**db_match)
                list_matches.append(match)
        return list_matches

    @classmethod
    def deserialize_all(cls):
        """
        Deserialize all matches stocked in the matches_table.

        Steps:
            1. Players A & B are deserialized (using serials from serialized_matches)
            2. Compose match with its own attributes and players a & b
        """
        list_matches = []
        for id_match, db_match in cls.serialized_matches.items():
            # Get IDs
            player_a_id = db_match["player_a"]["id_player"]
            player_b_id = db_match["player_b"]["id_player"]
            # Get players
            player_a = Player.get(player_a_id)
            player_b = Player.get(player_b_id)

            kwargs = {"match_in_progress": db_match["match_in_progress"],
                      "player_a_score": db_match["player_a_score"],
                      "player_b_score": db_match["player_b_score"]
                      }
            match = Match(db_match["id_match"],
                          player_a,
                          player_b,
                          **kwargs)
            list_matches.append(match)
        return list_matches
