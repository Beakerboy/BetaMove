import re
from typing import TypeVar, Type


T = TypeVar('T', bound='Climb')


class Climb:

    # class default constructor
    def __init__(self: T) -> None:

        # Instance Attributes
        # The moonboard ID
        self._id = "0"

        # The problem name
        self._name = ""

        # The list of allowed holds with start and end
        self._holds = []

        # The grade
        # The JSON object has three grades; grade, info[2] and UserGrade
        self._grade = ""

        self._start_holds = 0
        self._finish_holds = 0

    # Setters and Getters
    def set_id(self: T, id: str) -> None:
        self._id = id
        # validate int as string

    def set_name(self: T, name: str) -> None:
        self._name = name

    def add_hold(self: T, hold: list) -> None:
        if hold[1] and hold[2]:
            raise exception
        if hold[1] and self._start_holds == 2:
            raise exception
        if hold[2] and self._finish_holds == 2:
            raise exception
        if self._moves.len() > 14:
            raise exception
        if re.match("[A-K]([1-9]|[1][0-8])", hold[0]) != hold[0]:
            raise exception
        self._moves.append(hold)
        if (hold[1]):
            self._start_holds += 1
        if (hold[2]):
            self._finish_holds += 1
        # Validate x and Y

    def set_grade(self: T, grade: str) -> None:
        self._grade = grade
        # Validate acceptible values

    def url(self: T) -> str:
        url = "https://moonboard.com/Problems/View/"
        return url + self._id + "/" + self._name.lower()
        
    @classmethod
    def from_json(cls: Type[T], id: int, data: dict) -> T:
        # parse data and set attributes
        climb = cls()
        climb._id = id
        climb._name = data["problem_name"]
        climb._grade = data["grade"]
        for hold in data["moves"]:
            climb._holds.append(
                [
                    hold["Description"],
                    hold["IsStart"],
                    hold["IsEnd"]
                ]
            )
        # Validate number of start, number of end, total holds.
        return climb
