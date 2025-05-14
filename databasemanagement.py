import datetime
import json
import sqlite3
import sys
import os


class DatabaseManagement:
    def __init__(self, database_path: str = 'catches.db', json_path: str = 'catches.json') -> None:
        self.database_path: str = database_path
        self.json_path: str = json_path

        self.connection: sqlite3.Connection = sqlite3.connect(database=os.path.join(sys.path[0], database_path))
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def restore_state(self) -> None:
        try:
            with open(file=os.path.join(sys.path[0], self.json_path), mode='r') as json_file:
                self.catches: list[dict] = json.load(json_file)

        except FileNotFoundError:
            print(f'{self.json_path} was not found')

        else:
            if self.cursor.execute('''SELECT count(*) FROM Catches''').fetchone()[0] == 0:
                for catch in self.catches:
                    # » Fishes
                    taxon_key: int = catch.get("fish").get("taxon_key")
                    species: str = catch.get("fish").get("species")
                    scientific_name: str = catch.get("fish").get("scientific_name")
                    kingdom: str = catch.get("fish").get("kingdom")

                    # » Catches
                    table_catches_id: int = catch.get("id")
                    fish_id: int = taxon_key
                    contestant_id: str = catch.get("candidate").get("id")
                    caught_at: datetime.datetime = datetime.datetime.strptime(catch.get("datetime"), '%Y-%m-%d %H:%M:%S')
                    coordinate: list[str] = catch.get("coordinate").split(", ")
                    latitude: float = float(coordinate[0])
                    longitude: float = float(coordinate[1])
                    country_code: str = catch.get("country_code")
                    weight: float = catch.get("weight")
                    length: float = catch.get("length")

                    # » Contestants
                    table_contestant_id: str = contestant_id
                    first_name: str = catch.get("candidate").get("first_name")
                    last_name: str = catch.get("candidate").get("last_name")
                    classification: str = catch.get("candidate").get("classification")

                    d_o_b: list[str] = catch.get("candidate").get("date_of_birth").split("-")
                    date_of_birth_date: datetime.date = datetime.date(year=int(d_o_b[0]), month=int(d_o_b[1]), day=int(d_o_b[2]))

                    self.cursor.execute('''INSERT OR IGNORE INTO Fishes (taxon_key, species, scientific_name, kingdom)
                                        VALUES (?, ?, ?, ?)
                                        ''', (taxon_key, species, scientific_name, kingdom))

                    self.cursor.execute('''INSERT OR IGNORE INTO Catches
                                        (id, fish_id, contestant_id, caught_at, latitude, longitude, country_code, weight, length)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                        ''', (table_catches_id, fish_id, contestant_id,
                                              caught_at, latitude, longitude, country_code, weight, length))

                    self.cursor.execute('''INSERT OR IGNORE INTO Contestants
                                        (id, first_name, last_name, classification, date_of_birth)
                                        VALUES (?, ?, ?, ?, ?)
                                        ''', (table_contestant_id, first_name, last_name, classification, date_of_birth_date))

                self.connection.commit()
                self.connection.close()
