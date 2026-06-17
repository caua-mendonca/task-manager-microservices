import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const loginDuration = new Trend('login_duration');

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 0 },
  ],
  setupTimeout: '120s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    errors: ['rate<0.1'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://api-gateway:3000';
const AUTH_BASE = __ENV.AUTH_BASE || BASE_URL;
const TASK_BASE = __ENV.TASK_BASE || BASE_URL;

export function setup() {
  const registerRes = http.post(`${AUTH_BASE}/api/auth/register`, JSON.stringify({
    name: 'K6 Test User',
    email: `k6test_${Date.now()}@test.com`,
    password: 'senha123'
  }), {
    headers: { 'Content-Type': 'application/json' },
    timeout: '60s'
  });

  if (registerRes.status !== 201) {
    return { token: null, setupStatus: registerRes.status };
  }

  const token = registerRes.json('token');
  return { token, setupStatus: registerRes.status };
}

export default function (data) {
  if (!data?.token) {
    errorRate.add(true);
    sleep(1);
    return;
  }

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${data.token}`
  };

  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health: status 200': (r) => r.status === 200,
    'health: body ok': (r) => r.json('status') === 'ok'
  });
  errorRate.add(healthRes.status !== 200);

  sleep(0.5);

  const createRes = http.post(`${TASK_BASE}/api/tasks`, JSON.stringify({
    title: `Tarefa k6 ${Date.now()}`,
    description: 'Criada pelo teste de carga',
    priority: 'medium',
    status: 'pending'
  }), { headers });

  check(createRes, {
    'create task: status 201': (r) => r.status === 201,
    'create task: tem id': (r) => r.json('data._id') !== undefined
  });
  errorRate.add(createRes.status !== 201);

  const taskId = createRes.json('data._id');
  sleep(0.5);

  const listRes = http.get(`${TASK_BASE}/api/tasks?page=1&limit=10`, { headers });
  check(listRes, {
    'list tasks: status 200': (r) => r.status === 200,
    'list tasks: tem data': (r) => Array.isArray(r.json('data'))
  });
  errorRate.add(listRes.status !== 200);

  sleep(0.5);

  if (taskId) {
    const getRes = http.get(`${TASK_BASE}/api/tasks/${taskId}`, { headers });
    check(getRes, {
      'get task by id: status 200': (r) => r.status === 200
    });
    errorRate.add(getRes.status !== 200);

    sleep(0.3);

    const patchRes = http.patch(`${TASK_BASE}/api/tasks/${taskId}/status`,
      JSON.stringify({ status: 'in_progress' }),
      { headers }
    );
    check(patchRes, {
      'patch status: status 200': (r) => r.status === 200
    });

    sleep(0.3);

    const deleteRes = http.del(`${TASK_BASE}/api/tasks/${taskId}`, null, { headers });
    check(deleteRes, {
      'soft delete: status 200': (r) => r.status === 200
    });
  }

  sleep(1);
}

export function handleSummary(data) {
  const totalRequests = data?.metrics?.http_reqs?.values?.count ?? 0;
  const errorRateValue = data?.metrics?.errors?.values?.rate ?? 0;
  const avgDuration = data?.metrics?.http_req_duration?.values?.avg ?? 0;
  const p95Duration = data?.metrics?.http_req_duration?.values?.['p(95)'] ?? 0;
  const setupStatus = data?.setup_data?.setupStatus ?? null;

  const summary = {
    totalRequests,
    errorRate: errorRateValue,
    avgDuration,
    p95Duration,
    setupStatus
  };

  return {
    'stdout': JSON.stringify(summary, null, 2),
    'summary.json': JSON.stringify(summary, null, 2)
  };
}
