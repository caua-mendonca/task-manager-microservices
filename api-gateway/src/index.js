require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const client = require('prom-client');
const rateLimiter = require('./middleware/rateLimiter');
const logger = require('./middleware/logger');
const setupProxy = require('./routes/proxy');

const app = express();

// ── Segurança ─────────────────────────────────────────
app.use(helmet());
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(rateLimiter);
app.use(logger);
app.use(express.json());

// ── Prometheus Metrics ────────────────────────────────
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics();

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total de requisições HTTP',
  labelNames: ['method', 'route', 'status']
});

app.use((req, res, next) => {
  res.on('finish', () => {
    httpRequestsTotal.inc({
      method: req.method,
      route: req.path,
      status: res.statusCode
    });
  });
  next();
});

// ── Health Check ──────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'api-gateway', timestamp: new Date().toISOString() });
});

// ── Métricas Prometheus ───────────────────────────────
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// ── Proxy para Microserviços ──────────────────────────
setupProxy(app);

// ── Start ─────────────────────────────────────────────
const PORT = process.env.API_GATEWAY_PORT || 3000;
app.listen(PORT, () => {
  console.log(`🚀 API Gateway rodando na porta ${PORT}`);
});
