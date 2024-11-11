"""Deterministic DAG scheduling under unlimited parallel capacity."""
import argparse
import heapq
import json
import math

def plan(jobs):
    if not isinstance(jobs, list):
        raise ValueError('Jobs must be a list')
    indexed = {}
    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError('Job must be an object')
        key = job.get('id')
        duration = job.get('duration')
        deps = job.get('depends_on', [])
        if not isinstance(key, str) or not key or key in indexed:
            raise ValueError('Unique nonempty job IDs required')
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
            raise ValueError('Durations must be finite and nonnegative')
        if not isinstance(deps, list) or any((not isinstance(d, str) for d in deps)) or len(set(deps)) != len(deps):
            raise ValueError('Dependencies must be unique strings')
        indexed[key] = {'duration': duration, 'deps': deps}
    children = {key: [] for key in indexed}
    remaining = {key: len(job['deps']) for (key, job) in indexed.items()}
    for (key, job) in indexed.items():
        for dependency in job['deps']:
            if dependency not in indexed or dependency == key:
                raise ValueError('Unknown or self dependency')
            children[dependency].append(key)
    ready = [key for (key, count) in remaining.items() if not count]
    heapq.heapify(ready)
    schedule = {}
    paths = {}
    while ready:
        key = heapq.heappop(ready)
        job = indexed[key]
        predecessor = min(job['deps'], key=lambda d: (-schedule[d]['finish'], d)) if job['deps'] else None
        start = schedule[predecessor]['finish'] if predecessor else 0
        finish = start + job['duration']
        if not math.isfinite(finish):
            raise ValueError('Schedule duration overflow')
        schedule[key] = {'start': start, 'finish': finish}
        paths[key] = (paths[predecessor] if predecessor else []) + [key]
        for child in sorted(children[key]):
            remaining[child] -= 1
            if not remaining[child]:
                heapq.heappush(ready, child)
    if len(schedule) != len(indexed):
        raise ValueError('Dependency cycle detected')
    final = min(schedule, key=lambda key: (-schedule[key]['finish'], key)) if schedule else None
    return {'schedule': schedule, 'total_duration': schedule[final]['finish'] if final else 0, 'critical_path': paths[final] if final else []}

def demo():
    return plan([{'id': 'ingest', 'duration': 2}, {'id': 'index', 'duration': 5, 'depends_on': ['ingest']}, {'id': 'validate', 'duration': 3, 'depends_on': ['ingest']}, {'id': 'publish', 'duration': 1, 'depends_on': ['index', 'validate']}])
if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(demo(), indent=2))
