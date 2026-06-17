require('dotenv').config();
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const client = require('prom-client');
const connectDB = require('./config/db');
const userRoutes = require('./routes/userRoutes');

const app = express();

connectDB();
app.use(express.json());

// ── Swagger ───────────────────────────────────────────
const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Task Manager — User Service API',
      version: '1.0.0',
      description: 'Serviço de gerenciamento de perfis de usuário'
    },
    components: {
      securitySchemes: {
        bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }
      }
    },
    servers: [{ url: 'http://localhost:3000' }]
  },
  apis: ['./src/routes/*.js']
});
app.use('/api/users/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ── Prometheus ────────────────────────────────────────
client.collectDefaultMetrics();
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

// ── Rotas ─────────────────────────────────────────────
app.use('/api/users', userRoutes);

// ── Health Check ──────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'user-service', timestamp: new Date().toISOString() });
});

const PORT = process.env.USER_SERVICE_PORT || 3003;
app.listen(PORT, () => {
  console.log(`👤 User Service rodando na porta ${PORT}`);
  console.log(`📘 Swagger: http://localhost:${PORT}/api/users/docs`);
});
