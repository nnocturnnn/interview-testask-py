import csv
import sqlite3
from typing import Any, Dict, Iterator, List, Optional, Tuple


def read_csv_iterator(file_path: str) -> Iterator[Dict[str, str]]:
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def create_user_table(database_path: str = "users.db") -> None:
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            create_table_query = (
                "CREATE TABLE IF NOT EXISTS users ("
                "category TEXT, "
                "firstname TEXT, "
                "lastname TEXT, "
                "email TEXT, "
                "gender TEXT, "
                "dob DATETIME"
                ");"
            )
            cursor.execute(create_table_query)
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)


def populate_user_table(
    data_iterator: Iterator[Dict[str, str]], database_path: str = "users.db"
) -> None:
    try:
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            for row in data_iterator:
                insert_query = (
                    "INSERT INTO users (category, firstname, lastname, email, gender, dob) "
                    "VALUES (:category, :firstname, :lastname, :email, :gender, :birthDate);"
                )
                cursor.execute(insert_query, row)
            conn.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)


def build_filter_query(filters: Optional[Dict[str, str]]) -> Tuple[str, List[Any]]:
    query = "SELECT * FROM users WHERE 1"
    params = []

    if filters:
        if "category" in filters:
            query += " AND category = ?"
            params.append(filters["category"])
        if "gender" in filters:
            query += " AND gender = ?"
            params.append(filters["gender"])
        if "dob" in filters:
            query += " AND dob = ?"
            params.append(filters["dob"])
        if "min_age" in filters and "max_age" in filters:
            query += " AND DATE('now') BETWEEN DATE(dob, '+{0} years') AND DATE(dob, '+{1} years')".format(
                filters["min_age"], filters["max_age"]
            )
        elif "min_age" in filters:
            query += " AND DATE('now') >= DATE(dob, '+{0} years')".format(
                filters["min_age"]
            )
        elif "max_age" in filters:
            query += " AND DATE('now') <= DATE(dob, '+{0} years')".format(
                filters["max_age"]
            )

    return query, params


def execute_query(
    query: str, params: List[Any], per_page: int, page: int
) -> List[Dict[str, str]]:
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])

    try:
        with sqlite3.connect("users.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []


def get_filtered_data(
    per_page: int, page: int, filters: Optional[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    query, params = build_filter_query(filters)
    return execute_query(query, params, per_page, page)
