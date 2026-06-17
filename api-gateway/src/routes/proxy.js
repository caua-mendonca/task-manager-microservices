const { createProxyMiddleware } = require('http-proxy-middleware');

const restreamBody = (proxyReq, req) => {
  if (!req.body || Object.keys(req.body).length === 0) return;

  const bodyData = JSON.stringify(req.body);
  proxyReq.setHeader('Content-Type', 'application/json');
  proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
  proxyReq.write(bodyData);
};

module.exports = (app) => {
  // Auth Service
  app.use('/api/auth', createProxyMiddleware({
    target: process.env.AUTH_SERVICE_URL,
    changeOrigin: true,
    onProxyReq: restreamBody,
    on: {
      error: (err, req, res) => {
        res.status(503).json({ error: 'Auth Service indisponível' });
      }
    }
  }));

  // Task Service
  app.use('/api/tasks', createProxyMiddleware({
    target: process.env.TASK_SERVICE_URL,
    changeOrigin: true,
    onProxyReq: restreamBody,
    on: {
      error: (err, req, res) => {
        res.status(503).json({ error: 'Task Service indisponível' });
      }
    }
  }));

  // User Service
  app.use('/api/users', createProxyMiddleware({
    target: process.env.USER_SERVICE_URL,
    changeOrigin: true,
    onProxyReq: restreamBody,
    on: {
      error: (err, req, res) => {
        res.status(503).json({ error: 'User Service indisponível' });
      }
    }
  }));
};
