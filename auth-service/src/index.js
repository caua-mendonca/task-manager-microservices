require('dotenv').config();
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const client = require('prom-client');
const connectDB = require('./config/db');
const authRoutes = require('./routes/authRoutes');

const app = express();

// ── Conexão DB ────────────────────────────────────────
connectDB();

// ── Middlewares ───────────────────────────────────────
app.use(express.json());

// ── Swagger ───────────────────────────────────────────
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Task Manager — Auth Service API',
      version: '1.0.0',
      description: 'Serviço de autenticação com JWT'
    },
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      }
    },
    servers: [{ url: 'http://localhost:3000' }]
  },
  apis: ['./src/routes/*.js']
};

const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use('/api/auth/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ── Prometheus ────────────────────────────────────────
client.collectDefaultMetrics();
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// ── Rotas ─────────────────────────────────────────────
app.use('/api/auth', authRoutes);

// ── Health Check ──────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'auth-service', timestamp: new Date().toISOString() });
});

// ── Start ─────────────────────────────────────────────
const PORT = process.env.AUTH_SERVICE_PORT || 3001;
app.listen(PORT, () => {
  console.log(`🔐 Auth Service rodando na porta ${PORT}`);
  console.log(`📘 Swagger: http://localhost:${PORT}/api/auth/docs`);
});
