import sqlite3
import os

DATABASE_PATH = "database/crime_records.db"


def create_database():
    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crime_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            state TEXT,
            city TEXT,
            crime_type TEXT,
            description TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_crime_record(
    date,
    state,
    city,
    crime_type,
    description,
    status
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO crime_records
        (date, state, city, crime_type, description, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        state,
        city,
        crime_type,
        description,
        status
    ))

    connection.commit()
    connection.close()


def get_all_records():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM crime_records
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records


def update_crime_record(
    record_id,
    date,
    state,
    city,
    crime_type,
    description,
    status
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE crime_records
        SET date = ?,
            state = ?,
            city = ?,
            crime_type = ?,
            description = ?,
            status = ?
        WHERE id = ?
    """, (
        date,
        state,
        city,
        crime_type,
        description,
        status,
        record_id
    ))

    connection.commit()
    connection.close()


def delete_record(record_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM crime_records WHERE id = ?",
        (record_id,)
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":

    create_database()

    print("\n======================================")
    print("CRIME RECORD DATABASE")
    print("======================================")
    print("Database created successfully!")
    print("Crime records table is ready.")