require('dotenv').config();
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const client = require('prom-client');
const connectDB = require('./config/db');
const taskRoutes = require('./routes/taskRoutes');

const app = express();

connectDB();
app.use(express.json());

const swaggerSpec = swaggerJsdoc({
  definition: {
    openapi: '3.0.0',
    info: { title: 'Task Manager — Task Service', version: '1.0.0' },
    components: {
      securitySchemes: { bearerAuth: { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' } }
    },
    servers: [{ url: 'http://localhost:3000' }]
  },
  apis: ['./src/routes/*.js']
});
app.use('/api/tasks/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));

client.collectDefaultMetrics();
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

app.use('/api/tasks', taskRoutes);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'task-service', timestamp: new Date().toISOString() });
});

const PORT = process.env.TASK_SERVICE_PORT || 3002;
app.listen(PORT, () => {
  console.log(`📋 Task Service rodando na porta ${PORT}`);
});
