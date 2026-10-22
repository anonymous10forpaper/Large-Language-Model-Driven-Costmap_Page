#!/usr/bin/env python3
"""Recalculate released keepout metrics; does not launch ROS or Gazebo."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

def load(path):
    return json.loads(path.read_text())

def records(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def near(a, b):
    return abs(float(a) - float(b)) < 1e-9

def verify(root):
    protocol = load(root/'protocol.json')
    summary = load(root/'summary.json')
    audit = {r['trial']: r for r in load(root/'audit.json')['trials']}
    table = {r['trial']: r for r in records(root/'trial_results.csv')}
    release = load(root/'release_manifest.json')
    for artifact in release['files']:
        assert sha(root/artifact['path']) == artifact['public_sha256'], artifact['path']
    checked, hashes = [], set()
    for item in protocol['schedule']:
        trial = item['trial']
        folder = root/'runs'/trial
        r = load(folder/'result.json')
        raw = records(folder/'odometry.csv')
        start, end = r['first_motion_sim_time'], r['terminal_sim_time']
        selected = [v for v in raw if start <= float(v['sim_s']) <= end]
        distance = math.fsum(math.hypot(float(b['odom_x'])-float(a['odom_x']), float(b['odom_y'])-float(a['odom_y'])) for a,b in zip(selected, selected[1:]))
        duration = end-start
        first = next(float(v['sim_s']) for v in raw if float(v['sim_s']) >= r['goal_accepted_sim_time'] and abs(float(v['linear_x'])) > .01)
        assert near(first, start) and len(selected) == r['odom_samples'], trial
        for key, value in [('travel_distance_m',distance), ('travel_time_s',duration)]:
            assert near(value,r[key]) and near(value,table[trial][key]), (trial,key)
        value = sha(folder/'odometry.csv')
        assert value == audit[trial]['odometry_sha256'], trial
        hashes.add(value)
        checked.append(r)
    assert len(checked) == len(hashes) == 10
    stats = {}
    for condition in ('custom','native'):
        group = [r for r in checked if r['condition'] == condition]
        assert len(group) == 5
        stats[condition] = {}
        for metric in ('travel_distance_m','travel_time_s','accepted_to_terminal_s'):
            values = [r[metric] for r in group]
            output = {'mean':statistics.mean(values),'sd':statistics.stdev(values)}
            for key, value in output.items():
                assert near(value,summary['stats'][condition][metric][key]), (condition,metric,key)
            stats[condition][metric] = output
    print(json.dumps({'verified_trials':len(checked),'verified_public_files':len(release['files']),
        'sample_sd_ddof':1,'summary':stats,'scope':'Recorded metric and file-integrity checks only; experiment not rerun.'},indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1]/'data'/'keepout-comparison')
    verify(parser.parse_args().data)
