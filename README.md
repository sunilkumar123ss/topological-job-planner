# Topological job planner

Calculate dependency-safe earliest schedules and a critical path for a job DAG.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

A deterministic topological traversal schedules each job after its latest prerequisite. The report includes earliest start and finish times, a critical path, and total duration assuming unlimited workers. Cycles, unknown dependencies, duplicate IDs, and invalid durations are rejected.

## Use in Python

```python
from main import plan

result = plan([
    {'id': 'ingest', 'duration': 2},
    {'id': 'index', 'duration': 5, 'depends_on': ['ingest']},
])
assert result['total_duration'] == 7
```

## Design limits

This is an offline planner with fixed supplied durations, not a job executor. It does not model resource contention, worker limits, retries, transfer costs, or uncertain runtime. The synthetic durations demonstrate arithmetic only.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
