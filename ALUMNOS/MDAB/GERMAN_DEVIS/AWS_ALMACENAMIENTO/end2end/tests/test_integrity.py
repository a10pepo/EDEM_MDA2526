from initial_info import teams, drivers, races


def test_team_count():
    assert len(teams) == 10


def test_driver_count():
    assert len(drivers) == 20


def test_race_count():
    assert len(races) >= 1


def test_no_empty_races():
    assert all(len(r["results"]) >= 1 for r in races)


def test_all_driver_team_ids_exist():
    team_ids = {t["teamId"] for t in teams}
    for driver in drivers:
        assert driver["teamId"] in team_ids, f"{driver['code']} has unknown teamId {driver['teamId']}"


def test_driver_codes_are_unique():
    codes = [d["code"] for d in drivers]
    assert len(codes) == len(set(codes))


def test_race_ids_are_unique():
    race_ids = [r["raceId"] for r in races]
    assert len(race_ids) == len(set(race_ids))


def test_result_driver_ids_exist():
    driver_ids = {d["driverId"] for d in drivers}
    for race in races:
        for driver_id, *_ in race["results"]:
            assert driver_id in driver_ids, f"Unknown driver {driver_id} in race {race['raceId']}"
