import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.environ['RDS_HOST'],
    port=os.environ['RDS_PORT'],
    user=os.environ['RDS_USER'],
    password=os.environ['RDS_PASSWORD'],
    database=os.environ['RDS_DB'],
)
conn.autocommit = True
cur = conn.cursor()


def create_tables():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pilots (
            rank INT,
            driver VARCHAR(100) PRIMARY KEY,
            nationality VARCHAR(50),
            wins INT,
            championships INT,
            years_active VARCHAR(50),
            team_most_wins_with VARCHAR(100)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS races (
            race_id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            circuit VARCHAR(100),
            date DATE,
            laps INT,
            total_distance_km INT
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            result_id VARCHAR(10) PRIMARY KEY,
            race_id VARCHAR(10) REFERENCES races(race_id),
            driver VARCHAR(100) REFERENCES pilots(driver),
            position INT,
            points INT,
            status VARCHAR(20)
        );
    """)
    print("Tablas creadas.")


def insert_data():
    pilots = [
        (1, "Lewis Hamilton", "British", 103, 7, "2007-present", "Mercedes"),
        (2, "Michael Schumacher", "German", 91, 7, "1991-2006 / 2010-2012", "Ferrari"),
        (3, "Max Verstappen", "Dutch", 63, 4, "2015-present", "Red Bull"),
        (4, "Sebastian Vettel", "German", 53, 4, "2007-2022", "Red Bull"),
        (5, "Alain Prost", "French", 51, 4, "1980-1993", "McLaren"),
        (6, "Ayrton Senna", "Brazilian", 41, 3, "1984-1994", "McLaren"),
        (7, "Fernando Alonso", "Spanish", 32, 2, "2001-present", "Renault"),
        (8, "Nigel Mansell", "British", 31, 1, "1980-1995", "Williams"),
        (9, "Jackie Stewart", "British", 27, 3, "1965-1973", "Tyrrell"),
        (10, "Jim Clark", "British", 25, 2, "1960-1968", "Lotus"),
        (11, "Niki Lauda", "Austrian", 25, 3, "1971-1985", "Ferrari"),
        (12, "Juan Manuel Fangio", "Argentine", 24, 5, "1950-1958", "Mercedes"),
        (13, "Nelson Piquet", "Brazilian", 23, 3, "1978-1991", "Brabham"),
        (14, "Damon Hill", "British", 22, 1, "1992-1999", "Williams"),
        (15, "Kimi Raikkonen", "Finnish", 21, 1, "2001-2021", "Ferrari"),
        (16, "Mika Hakkinen", "Finnish", 20, 2, "1991-2001", "McLaren"),
        (17, "Stirling Moss", "British", 16, 0, "1951-1961", "Maserati"),
        (18, "Jenson Button", "British", 15, 1, "2000-2017", "Brawn GP"),
        (19, "Jack Brabham", "Australian", 14, 3, "1955-1970", "Cooper"),
        (20, "Emerson Fittipaldi", "Brazilian", 14, 2, "1970-1980", "Lotus"),
        (21, "Graham Hill", "British", 14, 2, "1958-1975", "Lotus"),
        (22, "Alberto Ascari", "Italian", 13, 2, "1950-1955", "Ferrari"),
        (23, "David Coulthard", "British", 13, 0, "1994-2008", "McLaren"),
        (24, "Mario Andretti", "American", 12, 1, "1968-1982", "Lotus"),
        (25, "Carlos Reutemann", "Argentine", 12, 0, "1972-1982", "Williams"),
        (26, "Alan Jones", "Australian", 12, 1, "1975-1986", "Williams"),
        (27, "Rubens Barrichello", "Brazilian", 11, 0, "1993-2011", "Ferrari"),
        (28, "Felipe Massa", "Brazilian", 11, 0, "2002-2017", "Ferrari"),
        (29, "Jody Scheckter", "South African", 10, 1, "1972-1980", "Ferrari"),
        (30, "Gerhard Berger", "Austrian", 10, 0, "1984-1997", "Ferrari"),
    ]
    races = [
        ("R-001", "Gran Premio de Bahrein", "Sakhir", "2025-03-02", 57, 308),
        ("R-002", "Gran Premio de Arabia Saudi", "Jeddah", "2025-03-09", 50, 308),
        ("R-003", "Gran Premio de Australia", "Melbourne", "2025-03-23", 58, 307),
        ("R-004", "Gran Premio de Japon", "Suzuka", "2025-06-06", 53, 307),
        ("R-005", "Gran Premio de China", "Shanghai", "2025-04-20", 56, 305),
        ("R-006", "Gran Premio de Miami", "Miami", "2025-05-04", 57, 308),
        ("R-007", "Gran Premio de Monaco", "Monaco", "2025-05-25", 78, 260),
        ("R-008", "Gran Premio de Canada", "Montreal", "2025-06-15", 70, 305),
        ("R-009", "Gran Premio de Espana", "Barcelona", "2025-06-29", 66, 307),
        ("R-010", "Gran Premio de Gran Bretana", "Silverstone", "2025-07-06", 52, 306),
    ]
    results = [
        ("RES-001", "R-001", "Max Verstappen", 1, 25, "Finished"),
        ("RES-002", "R-001", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-003", "R-001", "Fernando Alonso", 3, 15, "Finished"),
        ("RES-004", "R-001", "Kimi Raikkonen", 0, 0, "DNF"),
        ("RES-005", "R-002", "Max Verstappen", 1, 25, "Finished"),
        ("RES-006", "R-002", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-007", "R-002", "Sebastian Vettel", 3, 15, "Finished"),
        ("RES-008", "R-002", "Fernando Alonso", 0, 0, "DNF"),
        ("RES-009", "R-003", "Lewis Hamilton", 1, 25, "Finished"),
        ("RES-010", "R-003", "Max Verstappen", 2, 18, "Finished"),
        ("RES-011", "R-003", "Nigel Mansell", 3, 15, "Finished"),
        ("RES-012", "R-003", "Damon Hill", 0, 0, "DNF"),
        ("RES-013", "R-004", "Max Verstappen", 1, 25, "Finished"),
        ("RES-014", "R-004", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-015", "R-004", "Fernando Alonso", 3, 15, "Finished"),
        ("RES-016", "R-004", "Sebastian Vettel", 0, 0, "DNF"),
        ("RES-017", "R-005", "Max Verstappen", 1, 25, "Finished"),
        ("RES-018", "R-005", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-019", "R-005", "Alain Prost", 3, 15, "Finished"),
        ("RES-020", "R-005", "Ayrton Senna", 0, 0, "DNF"),
        ("RES-021", "R-006", "Lewis Hamilton", 1, 25, "Finished"),
        ("RES-022", "R-006", "Max Verstappen", 2, 18, "Finished"),
        ("RES-023", "R-006", "Fernando Alonso", 3, 15, "Finished"),
        ("RES-024", "R-006", "Nigel Mansell", 0, 0, "DNF"),
        ("RES-025", "R-007", "Max Verstappen", 1, 25, "Finished"),
        ("RES-026", "R-007", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-027", "R-007", "Ayrton Senna", 3, 15, "Finished"),
        ("RES-028", "R-007", "Alain Prost", 0, 0, "DNF"),
        ("RES-029", "R-008", "Lewis Hamilton", 1, 25, "Finished"),
        ("RES-030", "R-008", "Max Verstappen", 2, 18, "Finished"),
        ("RES-031", "R-008", "Sebastian Vettel", 3, 15, "Finished"),
        ("RES-032", "R-008", "Fernando Alonso", 0, 0, "DNF"),
        ("RES-033", "R-009", "Max Verstappen", 1, 25, "Finished"),
        ("RES-034", "R-009", "Lewis Hamilton", 2, 18, "Finished"),
        ("RES-035", "R-009", "Fernando Alonso", 3, 15, "Finished"),
        ("RES-036", "R-009", "Damon Hill", 0, 0, "DNF"),
        ("RES-037", "R-010", "Lewis Hamilton", 1, 25, "Finished"),
        ("RES-038", "R-010", "Max Verstappen", 2, 18, "Finished"),
        ("RES-039", "R-010", "Nigel Mansell", 3, 15, "Finished"),
        ("RES-040", "R-010", "Kimi Raikkonen", 0, 0, "DNF"),
    ]

    cur.executemany("INSERT INTO pilots VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (driver) DO NOTHING;", pilots)
    print(f"Pilotos insertados: {len(pilots)}")

    cur.executemany("INSERT INTO races VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (race_id) DO NOTHING;", races)
    print(f"Carreras insertadas: {len(races)}")

    cur.executemany("INSERT INTO results VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (result_id) DO NOTHING;", results)
    print(f"Resultados insertados: {len(results)}")


if __name__ == "__main__":
    create_tables()
    insert_data()
    print("\nDatos iniciales cargados en RDS correctamente.")
    conn.close()
