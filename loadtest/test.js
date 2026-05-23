import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';
const SIZE = parseInt(__ENV.SIZE || '1000');
const USERS = parseInt(__ENV.USERS || '10');
const DURATION = __ENV.DURATION || '1m';

export const options = {
  vus: USERS,
  duration: DURATION,

  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<60000'],
  },
};

export default function () {
  const url = `${BASE_URL}/compute?size=${SIZE}`;

  const res = http.post(url);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(1);
}