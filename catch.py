import datetime
from contestant import Contestant
from databasemanagement import DatabaseManagement
from fish import Fish
import sqlite3


class Catch:
    def __init__(self, id: int, fish: int, contestant: str, caught_at: datetime.datetime,
                 latitude: float, longitude: float, country_code: str, weight: float,
                 length: float) -> None:
        self.database: DatabaseManagement = DatabaseManagement()
        self.connection: sqlite3.Connection = self.database.connection
        self.cursor = sqlite3.Cursor = self.database.cursor

        self.id: int = id
        self.fish: int = fish
        self.contestant: str = contestant
        self.caught_at: datetime.datetime = caught_at
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.country_code: str = country_code
        self.weight: float = weight
        self.length: float = length

    def get_contestant(self) -> Contestant:
        contestant_info: tuple = self.cursor.execute('''SELECT *
                                                     FROM Contestants
                                                     JOIN Catches ON Contestants.id = Catches.contestant_id
                                                     AND Catches.id = ?''', (self.id,)).fetchone()
        return Contestant(*contestant_info[:5])

    def get_fish(self) -> Fish:
        fish_info: tuple = self.cursor.execute('''SELECT *
                                               FROM Fishes
                                               JOIN Catches ON Fishes.taxon_key = Catches.fish_id
                                               AND Catches.fish_id = ?''', (self.fish,)).fetchone()
        return Fish(*fish_info[:4])

    def get_weight_in_local_units(self) -> str:
        match self.country_code.upper():
            case "MM":
                return f"{self.weight / 453.592:.2f} Pound, {self.weight / 1600:.2f} Viss"
            case "GB":
                return f"{self.weight / 453.592:.2f} Pound, {self.weight / 6350.29:.2f} Stone"
            case "IN" | "KH" | "TZ" | "PH" | "LK":
                return f"{self.weight / 453.592:.2f} Pound, {self.weight / 1000:.2f} Kilogram"
            case "US" | "LR" | "CA" | "AU" | "BS" | "FJ" | "JM" | "PG" | "TO":
                return f"{self.weight / 453.592:.2f} Pound, {self.weight / 28.3495:.2f} Ounce"
            case _:
                return f"{self.weight:.2f} Gram, {self.weight / 1000:.2f} Kilogram"

    def get_day_part(self) -> str:
        hour = self.caught_at.hour
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        elif 18 <= hour < 24:
            return "Evening"
        else:
            return "Night"

    def get_season(self) -> str:
        if self.caught_at.month in [12, 1, 2]:
            return "Winter"
        elif self.caught_at.month in [3, 4, 5]:
            return "Spring"
        elif self.caught_at.month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    def get_weight_category(self) -> str:
        expected_weight: float = 0.0123 * self.length ** 3.1
        result: float = self.weight / expected_weight
        print(result)
        return "light" if result < 0.98 else "average" if 0.98 <= result <= 1.02 else "heavy"

    def __repr__(self) -> str:
        excluced_keys: list[str] = ['database', 'cursor', 'connection']
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()
                       if not any(key == excluced_key for excluced_key in excluced_keys)]),
        )
