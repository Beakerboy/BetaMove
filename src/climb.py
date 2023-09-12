from typing import TypeVar


T = TypeVar('T', bound='Climb')


class Climb:

    # class default constructor
    def __init__(self: T):

        # Instance Attributes
        # The moonboard ID
        def self._id = 0

        # The problem name
        def self._name = ""

        # The list of allowed holds with start and end
        def self._holds = []

        # The grade
        # The JSON object has three grades; grade, info[2] and UserGrade
        def self._grade = ""

    # Setters and Getters
    def set_id(self: T, id: int) -> None:
        self._id = id

    def set_name(self: T, name: str) -> None:
        self._name = name

    def add_move(self: T, move: dict) -> None:
        self._moves.append(move)

    def set_grade(self: T, grade: str) -> None:
        self._grade = grade

    @classmethod
    def from_json(cls: Type[T], id: int, data: dict) -> T:
        # parse data and set attributes
        climb = cls()
        climb._id = id
        climb._name = data.problem_name
        climb._grade = data.grade
        for hold in data.moves:
            self._holds.append(list(hold["Description"], hold["IsStart"], hold["IsEnd"]))
        return climb
