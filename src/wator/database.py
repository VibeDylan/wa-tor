import sqlite3, datetime


def connect_database():
    connection = sqlite3.connect("database_wator.db")
    return connection


def create_database():
    connection = connect_database()
    
    with connection:
        connection.execute("""
    CREATE TABLE IF NOT EXISTS simulation(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            datetime TEXT NOT NULL,
            chronons INTEGER NOT NULL,
            fishes INTEGER NOT NULL,
            sharks INTEGER NOT NULL
        )
    """)

    connection.close()


def archive_simulation(nb_chronon: int, nb_fish: int, nb_sharks: int):
    connection = connect_database()
    
    date = datetime.datetime.now()
    formatted_date = date.strftime("%Y-%m-%d %H:%M")
    simulation_data = {"datetime": formatted_date, "chronons": nb_chronon, "fishes": nb_fish, "sharks": nb_sharks}
    
    with connection:
        connection.execute("""
            INSERT INTO simulation(datetime, chronons, fishes, sharks) VALUES (:datetime, :chronons, :fishes, :sharks)
        """, simulation_data)

    connection.close()


def display_history():

    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM simulation")
    last_results = cursor.fetchall()[-5:]
    connection.close()
    
    text_lines = []
    for row in last_results:
        line = f"Chronons: {row[2]} | Poissons: {row[3]} | Requins: {row[4]}"
        text_lines.append(line)
    
    return "\n".join(text_lines)