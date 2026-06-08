from initial_info import races
from load_rds import insert_teams, insert_drivers, insert_races, insert_results


def test_insert_teams_uses_executemany(mock_cursor):
    insert_teams(mock_cursor)
    mock_cursor.executemany.assert_called_once()


def test_insert_teams_sql(mock_cursor):
    insert_teams(mock_cursor)
    sql, _ = mock_cursor.executemany.call_args[0]
    assert "INSERT INTO teams" in sql
    assert "ON CONFLICT" in sql


def test_insert_teams_row_count(mock_cursor):
    insert_teams(mock_cursor)
    _, rows = mock_cursor.executemany.call_args[0]
    assert len(rows) == 10


def test_insert_drivers_row_count(mock_cursor):
    insert_drivers(mock_cursor)
    _, rows = mock_cursor.executemany.call_args[0]
    assert len(rows) == 20


def test_insert_races_row_count(mock_cursor):
    insert_races(mock_cursor)
    _, rows = mock_cursor.executemany.call_args[0]
    assert len(rows) == len(races)


def test_insert_results_row_count(mock_cursor):
    insert_results(mock_cursor)
    _, rows = mock_cursor.executemany.call_args[0]
    expected = sum(len(r["results"]) for r in races)
    assert len(rows) == expected


def test_insert_results_sql(mock_cursor):
    insert_results(mock_cursor)
    sql, _ = mock_cursor.executemany.call_args[0]
    assert "INSERT INTO results" in sql
    assert "ON CONFLICT" in sql
