import load_glue

SAMPLE_DATA = {
    "teams":   [{"team_id": "T-01", "name": "Red Bull", "base": "UK", "team_principal": "C.H.", "power_unit": "Honda", "founded_year": 2005, "championships": 6}],
    "drivers": [{"driver_id": "D-01", "team_id": "T-01", "code": "VER", "name": "Verstappen", "nationality": "Dutch", "date_of_birth": "1997-09-30", "permanent_number": 1}],
    "races":   [{"race_id": "R-2024-01", "name": "Bahrain GP", "circuit": "BIC", "country": "Bahrain", "date": "2024-03-02", "season": 2024, "round": 1, "laps": 57}],
    "results": [{"race_id": "R-2024-01", "driver_id": "D-01", "grid_position": 1, "final_position": 1, "points": 26.0, "status": "Finished"}],
}


def _patch_all(mocker):
    mocker.patch("load_glue.get_rds_connection", return_value=mocker.MagicMock())
    mocker.patch("load_glue.fetch_table", side_effect=lambda conn, table: SAMPLE_DATA[table])
    mocker.patch.object(load_glue.s3, "head_bucket")
    mock_put = mocker.patch.object(load_glue.s3, "put_object")
    mock_create = mocker.patch.object(load_glue.glue, "create_table")
    return mock_put, mock_create


def test_main_uploads_four_parquets(mocker):
    mock_put, _ = _patch_all(mocker)
    load_glue.main()
    assert mock_put.call_count == 4


def test_main_correct_s3_keys(mocker):
    mock_put, _ = _patch_all(mocker)
    load_glue.main()
    keys = {c.kwargs["Key"] for c in mock_put.call_args_list}
    assert keys == {
        "f1/teams/data.parquet",
        "f1/drivers/data.parquet",
        "f1/races/data.parquet",
        "f1/results/data.parquet",
    }


def test_main_registers_four_glue_tables(mocker):
    _, mock_create = _patch_all(mocker)
    load_glue.main()
    assert mock_create.call_count == 4


def test_main_glue_database_name(mocker):
    _, mock_create = _patch_all(mocker)
    load_glue.main()
    for call in mock_create.call_args_list:
        assert call.kwargs["DatabaseName"] == load_glue.GLUE_DATABASE


def test_main_glue_table_names(mocker):
    _, mock_create = _patch_all(mocker)
    load_glue.main()
    names = {c.kwargs["TableInput"]["Name"] for c in mock_create.call_args_list}
    assert names == {"teams", "drivers", "races", "results"}


def test_glue_tables_use_parquet_format(mocker):
    _, mock_create = _patch_all(mocker)
    load_glue.main()
    for call in mock_create.call_args_list:
        sd = call.kwargs["TableInput"]["StorageDescriptor"]
        assert "parquet" in sd["InputFormat"].lower()
