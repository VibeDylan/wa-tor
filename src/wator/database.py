import sqlite3, datetime


def connect_database():
    connection = sqlite3.connect("database_wator.db")
    cursor = connection.cursor()
    return connection, cursor


def create_database():
    connection, cursor = connect_database()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            datetime TEXT NOT NULL,
            chronons INTEGER NOT NULL,
            fishes INTEGER NOT NULL,
            sharks INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def archive_simulation(nb_chronon: int, nb_fish: int, nb_sharks: int):
    connection, cursor = connect_database()
    
    date = datetime.datetime.now()
    formatted_date = date.strftime("%Y-%m-%d %H:%M")
    simulation_data = {"datetime": formatted_date, "chronons": nb_chronon, "fishes": nb_fish, "sharks": nb_sharks}
    
    cursor.execute("""
        INSERT INTO simulation(datetime, chronons, fishes, sharks) VALUES (:datetime, :chronons, :fishes, :sharks)
    """, simulation_data)

    connection.commit()
    connection.close()


def display_history():
    connexion, cursor = connect_database()
    
    cursor.execute("""SELECT * FROM simulation""")

    last_results = cursor.fetchall()[-5:]
    for row in last_results:
        print("Simulation n°{0} ({1}) lasted {2} chronons with {3} fishes left and {4} sharks left.".format(row[0], row[1], row[2], row[3], row[4]))
    
    connexion.close()