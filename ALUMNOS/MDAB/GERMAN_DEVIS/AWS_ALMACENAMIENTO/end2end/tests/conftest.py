import sys
import os
from unittest.mock import MagicMock
import pytest

# Set stub env vars before any module-level boto3.client() or os.environ[] calls
_defaults = {
    "AWS_ACCESS_KEY_ID": "test",
    "AWS_SECRET_ACCESS_KEY": "test",
    "AWS_REGION": "eu-north-1",
    "S3_BUCKET": "test-bucket",
    "GLUE_DATABASE": "test-db",
    "PGHOST": "localhost",
    "PGPORT": "5432",
    "PGUSER": "test",
    "PGPASSWORD": "test",
    "PGDATABASE": "test",
}
for key, val in _defaults.items():
    os.environ.setdefault(key, val)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def mock_cursor():
    return MagicMock()
