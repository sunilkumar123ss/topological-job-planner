import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)

class PlannerTests(unittest.TestCase):

    def test_parallel_jobs_do_not_sum(self):
        r = m.plan([{'id': 'a', 'duration': 3}, {'id': 'b', 'duration': 5}])
        self.assertEqual(r['total_duration'], 5)

    def test_diamond_uses_longest_predecessor(self):
        r = m.demo()
        self.assertEqual(r['total_duration'], 8)
        self.assertEqual(r['critical_path'], ['ingest', 'index', 'publish'])
        self.assertEqual(r['schedule']['publish']['start'], 7)

    def test_cycle_rejected(self):
        with self.assertRaises(ValueError):
            m.plan([{'id': 'a', 'duration': 1, 'depends_on': ['b']}, {'id': 'b', 'duration': 1, 'depends_on': ['a']}])

    def test_unknown_and_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            m.plan([{'id': 'a', 'duration': 1, 'depends_on': ['x']}])
        with self.assertRaises(ValueError):
            m.plan([{'id': 'a', 'duration': 1}, {'id': 'a', 'duration': 2}])

    def test_empty_and_zero_duration(self):
        self.assertEqual(m.plan([])['total_duration'], 0)
        r = m.plan([{'id': 'a', 'duration': 0}, {'id': 'b', 'duration': 0, 'depends_on': ['a']}])
        self.assertEqual(r['schedule']['b']['start'], 0)

if __name__ == '__main__':
    unittest.main()
