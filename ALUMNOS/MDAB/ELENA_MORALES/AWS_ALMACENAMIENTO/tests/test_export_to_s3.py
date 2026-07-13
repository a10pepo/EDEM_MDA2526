import tempfile
import unittest
from pathlib import Path

from scripts.export_to_s3 import rows_to_csv_bytes, upload_directory_to_s3


class FakeS3Client:
    def __init__(self):
        self.uploads = []

    def upload_file(self, source, bucket, key):
        self.uploads.append({"source": source, "bucket": bucket, "key": key})


class ExportToS3Tests(unittest.TestCase):
    def test_rows_to_csv_bytes_formats_rows(self):
        rows = [
            {"id": 1, "name": "Ana"},
            {"id": 2, "name": "Luis"},
        ]

        csv_bytes = rows_to_csv_bytes(rows)

        self.assertIn(b"id,name", csv_bytes)
        self.assertIn(b"1,Ana", csv_bytes)
        self.assertIn(b"2,Luis", csv_bytes)

    def test_upload_directory_to_s3_uses_bucket_and_prefix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "products.csv"
            file_path.write_text("id,name\n1,Ana\n", encoding="utf-8")

            client = FakeS3Client()
            uploaded = upload_directory_to_s3(tmpdir, "demo-bucket", prefix="landing", client=client)

            self.assertEqual(len(uploaded), 1)
            self.assertEqual(uploaded[0]["key"], "landing/products.csv")
            self.assertEqual(client.uploads[0]["bucket"], "demo-bucket")


if __name__ == "__main__":
    unittest.main()
