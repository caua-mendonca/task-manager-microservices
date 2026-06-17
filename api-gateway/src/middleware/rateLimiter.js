const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 20000,                // máximo 20000 requisições por janela
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    status: 429,
    error: 'Muitas requisições. Tente novamente em 15 minutos.'
  }
});

module.exports = limiter;
