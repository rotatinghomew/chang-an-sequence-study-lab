"""交换资料受理接口与基础关系的测试。"""

import tempfile
import unittest
from pathlib import Path

from catalog import read_packet


class PacketTest(unittest.TestCase):
    def setUp(self):
        self.data = read_packet(Path(__file__).resolve().parents[1] / "data")

    def test_relationship_keys(self):
        relations = (
            ('assignment', 'id', 'classes'),
            ('learners', 'class_id', 'classes'),
            ('visits', 'learner', 'learners'),
            ('visits', 'class_id', 'classes'),
            ('marks', 'learner', 'learners'),
            ('shared', 'a', 'classes'),
            ('shared', 'b', 'classes'),
            ('rollout', 'class_id', 'classes'),
            ('rollout', 'paired', 'classes'),

        )
        for table, field, destination in relations:
            existing = {record["id"] for record in self.data[destination]}
            for row in self.data[table]:
                value = row[field]
                identifiers = value if isinstance(value, list) else [value]
                for item in identifiers:
                    if item is not None:
                        self.assertIn(item, existing, (table, field, row["id"]))

    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            table = Path(directory) / "records.json"
            table.write_text('[{"id": "A"}, {"id": "A"}]', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "重复记录"):
                read_packet(directory)

    def test_numeric_dependencies(self):
        from importlib.metadata import version

        self.assertEqual(version("numpy"), "1.26.4")
        self.assertEqual(version("scipy"), "1.13.1")
