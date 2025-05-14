from datetime import date
from catch import Catch
from fish import Fish
from contestant import Contestant
from databasemanagement import DatabaseManagement
import sqlite3
import csv
import os
import sys


class Reporter:
    def __init__(self) -> None:
        self.database: DatabaseManagement = DatabaseManagement(database_path='catches.db', json_path='catches.json')
        self.connection: sqlite3.Connection = self.database.connection
        self.cursor: sqlite3.Cursor = self.database.cursor

    def csv_writer(self, file_path: str = None, csv_lines: list[dict] = [], headers: list[str] = []) -> None:
        try:
            with open(os.path.join(sys.path[0], file_path), "w", newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.DictWriter(f=csvfile, fieldnames=headers)
                csv_writer.writeheader()
                for csv_line in csv_lines:
                    csv_writer.writerow(csv_line)
        except Exception as e:
            print(e)

    def total_amount_of_fish(self) -> int:
        """
        Returns the total number of fish recorded in the database.
        """
        return self.cursor.execute('''SELECT count(*) FROM Fishes''').fetchone()[0]

    def biggest_catch(self) -> Catch:
        """
        Returns the catch with the highest weight recorded in the database.
        """
        result: tuple = self.cursor.execute('''SELECT * FROM Catches
                                            WHERE weight = (SELECT MAX(weight) FROM Catches)''').fetchone()
        return Catch(*result)

    def longest_and_shortest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the longest and shortest catches recorded in the database.
        """
        longest_catch: tuple = self.cursor.execute('''SELECT * FROM Catches
                                                   WHERE length = (SELECT MAX(length) FROM Catches)''').fetchone()
        shortest_catch: tuple = self.cursor.execute('''SELECT * FROM Catches
                                                    WHERE length = (SELECT MIN(length) FROM Catches)''').fetchone()
        return Catch(*longest_catch), Catch(*shortest_catch)

    def heaviest_and_lightest_catch(self) -> tuple[Catch, Catch]:
        """
        Returns a tuple containing the heaviest and lightest catches by weight recorded in the database.
        """
        heaviest_catch: tuple = self.cursor.execute('''SELECT * FROM Catches
                                                    WHERE weight = (SELECT MAX(weight) FROM Catches)''').fetchone()
        lightest_catch: tuple = self.cursor.execute('''SELECT * FROM Catches
                                                    WHERE weight = (SELECT MIN(weight) FROM Catches)''').fetchone()
        return Catch(*heaviest_catch), Catch(*lightest_catch)

    def contestant_with_most_catches(self) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the most catches recorded in the database.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Contestants
                                                   WHERE id = (SELECT contestant_id
                                                   FROM Catches
                                                   GROUP BY contestant_id
                                                   ORDER BY COUNT(*) DESC)''').fetchall()
        return tuple(Contestant(*result) for result in results)

    def fish_with_most_catches(self) -> tuple[Fish, ...]:
        """
        Returns a tuple containing the fish species with the most catches recorded in the database.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Fishes
                                                   WHERE taxon_key = (SELECT fish_id
                                                   FROM Catches
                                                   GROUP BY fish_id
                                                   ORDER BY COUNT(*) DESC)''').fetchall()
        return tuple(Fish(*result) for result in results)

    def contestant_with_first_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the first catch of a specified fish type.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Contestants
                                                   WHERE id = (SELECT contestant_id
                                                   FROM Catches
                                                   WHERE fish_id = (SELECT taxon_key
                                                   FROM Fishes
                                                   WHERE species = ?)
                                                   GROUP BY contestant_id
                                                   ORDER BY caught_at ASC)''', (species,)).fetchall()
        return tuple(Contestant(*result) for result in results)

    def contestant_with_last_catch(self, species: str) -> tuple[Contestant, ...]:
        """
        Returns a tuple containing the contestant(s) with the last catch of a specified fish type.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Contestants
                                                   WHERE id = (SELECT contestant_id
                                                   FROM Catches
                                                   WHERE fish_id = (SELECT taxon_key
                                                   FROM Fishes
                                                   WHERE species = ?)
                                                   GROUP BY contestant_id
                                                   ORDER BY caught_at DESC)''', (species,)).fetchall()
        return tuple(Contestant(*result) for result in results)
    def contestants_fished_between(
        self, fish: Fish, start: date, end: date, to_csv: bool = False
    ) -> tuple[Contestant, ...] | None:
        """
        If to_csv is False, returns a tuple containing the contestants who fished a specified fish species between two dates.
        If to_csv is True, the results are written to a CSV file.
        """
        results = self.cursor.execute('''SELECT * FROM Contestants
                                      JOIN Catches ON Contestants.id = Catches.contestant_id
                                      WHERE Catches.fish_id = ?
                                      AND DATE(Catches.caught_at) BETWEEN ? AND ?
                                      GROUP BY Contestants.id
                                      ORDER BY Contestants.id ASC''', (fish.taxon_key, start, end)).fetchall()

        if not to_csv:
            return tuple(Contestant(*result) for result in results)
        else:
            to_write: list[dict] = [{
                "id": Contestant(*result).id, "first_name": Contestant(*result).first_name,
                "last_name": Contestant(*result).last_name, "date_of_birth": Contestant(*result).date_of_birth,
                "classification": Contestant(*result).classification
            } for result in results]

            file_path: str = f"Contestant fishing between {start} and {end}.csv"
            headers: list[str] = ["id", "first_name", "last_name", "date_of_birth", "classification"]
            self.csv_writer(file_path=file_path, csv_lines=to_write, headers=headers)
            return None

    def fish_caught_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Fish, ...] | None:
        """
        If to_csv is False, returns a tuple containing the fish species caught in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Fishes
                                                   JOIN Catches ON Catches.fish_id = Fishes.taxon_key
                                                   WHERE Catches.country_code = ?
                                                   GROUP BY Fishes.taxon_key
                                                   ORDER BY Fishes.taxon_key ASC''', (country_code,)).fetchall()

        if not to_csv:
            return tuple(Fish(*result) for result in results)
        else:
            to_write: list[dict] = [{
                "taxon_key": Fish(*result).taxon_key, "species": Fish(*result).species,
                "kingdom": Fish(*result).kingdom, "scientific_name": Fish(*result).scientific_name
            } for result in results]

            file_path: str = f"Fishes in country {country_code}.csv"
            headers: list[str] = ["taxon_key", "species", "kingdom", "scientific_name"]
            self.csv_writer(file_path=file_path, csv_lines=to_write, headers=headers)
            return None

    def contestants_fished_in_country(
        self, country_code: str, to_csv: bool = False
    ) -> tuple[Contestant, ...] | None:
        """
        If to_csv is False, returns a tuple containing the contestants who fished in a specified country.
        If to_csv is True, the results are written to a CSV file.
        """
        results: list[tuple] = self.cursor.execute('''SELECT * FROM Contestants
                                                   JOIN Catches ON Catches.contestant_id = Contestants.id
                                                   WHERE Catches.country_code = ?
                                                   GROUP BY Contestants.id
                                                   ORDER BY Contestants.id ASC''', (country_code,))

        if not to_csv:
            return tuple(Contestant(*result) for result in results)
        else:
            to_write: list[dict] = [{
                "id": Contestant(*result).id, "first_name": Contestant(*result).first_name,
                "last_name": Contestant(*result).last_name, "date_of_birth": Contestant(*result).date_of_birth,
                "classification": Contestant(*result).classification
            } for result in results]

            file_path: str = f"Contestants fished in country {country_code}.csv"
            headers: list[str] = ["id", "first_name", "last_name", "date_of_birth", "classification"]
            self.csv_writer(file_path=file_path, csv_lines=to_write, headers=headers)
            return None
