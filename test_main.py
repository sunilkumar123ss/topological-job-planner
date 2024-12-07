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





if __name__ == '__main__':
    unittest.main()
