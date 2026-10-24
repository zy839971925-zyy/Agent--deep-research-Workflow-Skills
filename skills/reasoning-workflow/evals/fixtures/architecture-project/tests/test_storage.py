"""Small synthetic tests; these do not validate any proposed remote design."""

import unittest
from src.storage import LocalScheduleStore


class LocalScheduleStoreTests(unittest.TestCase):
    def test_lookup_is_local(self):
        self.assertEqual(LocalScheduleStore("schedule.db").load_schedule("a")["source"], "local")


if __name__ == "__main__":
    unittest.main()
