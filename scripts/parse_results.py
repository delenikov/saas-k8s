import json
import glob
import csv
import os
import re

rows = []

for f in glob.glob('results/*.json'):

    with open(f) as fh:
        data = json.load(fh)

    name = os.path.basename(f)

    m = re.match(r'(eks|aks|local)_size(\d+)_users(\d+)\.json', name)

    if not m:
        continue

    platform, size, users = m.groups()

    metrics = data['metrics']

    rows.append({
        'platform': platform.upper(),

        'matrix_size': int(size),

        'users': int(users),

        'avg_response_ms':
            round(metrics['http_req_duration']['avg'], 2),

        'p95_response_ms':
            round(metrics['http_req_duration']['p(95)'], 2),

        'min_response_ms':
            round(metrics['http_req_duration']['min'], 2),

        'max_response_ms':
            round(metrics['http_req_duration']['max'], 2),

        'requests_per_second':
            round(metrics['http_reqs']['rate'], 2),

        'total_requests':
            metrics['http_reqs']['count'],

        'data_sent_MB':
            round(metrics['data_sent']['count'] / 1024 / 1024, 4),

        'data_received_MB':
            round(metrics['data_received']['count'] / 1024 / 1024, 4),

        'error_rate':
            round(metrics['http_req_failed']['value'], 4),
    })

rows.sort(
    key=lambda r: (
        r['matrix_size'],
        r['users'],
        r['platform']
    )
)

if rows:

    with open('results/summary.csv', 'w', newline='') as fh:

        writer = csv.DictWriter(
            fh,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    print('Wrote results/summary.csv')

else:
    print('No result files found.')