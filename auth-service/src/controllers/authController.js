const jwt = require('jsonwebtoken');
const { validationResult } = require('express-validator');
const User = require('../models/User');

// Gera JWT
const generateToken = (user) => {
  return jwt.sign(
    { id: user._id, email: user.email, role: user.role, name: user.name },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
  );
};

// POST /api/auth/register
exports.register = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { name, email, password, role } = req.body;

    const existingUser = await User.findOne({ email, deletedAt: null });
    if (existingUser) {
      return res.status(409).json({ error: 'Email já cadastrado' });
    }

    const user = await User.create({ name, email, password, role });
    const token = generateToken(user);

    res.status(201).json({
      message: 'Usuário criado com sucesso',
      token,
      user: { id: user._id, name: user.name, email: user.email, role: user.role }
    });
  } catch (err) {
    res.status(500).json({ error: 'Erro interno do servidor', details: err.message });
  }
};

// POST /api/auth/login
exports.login = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email, deletedAt: null }).select('+password');
    if (!user || !(await user.comparePassword(password))) {
      return res.status(401).json({ error: 'Email ou senha inválidos' });
    }

    if (!user.isActive) {
      return res.status(403).json({ error: 'Conta desativada' });
    }

    const token = generateToken(user);

    res.json({
      message: 'Login realizado com sucesso',
      token,
      user: { id: user._id, name: user.name, email: user.email, role: user.role }
    });
  } catch (err) {
    res.status(500).json({ error: 'Erro interno do servidor', details: err.message });
  }
};

// GET /api/auth/me
exports.getMe = async (req, res) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user || user.deletedAt) {
      return res.status(404).json({ error: 'Usuário não encontrado' });
    }
    res.json({ user: { id: user._id, name: user.name, email: user.email, role: user.role } });
  } catch (err) {
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
};

// POST /api/auth/refresh
exports.refreshToken = async (req, res) => {
  try {
    const user = await User.findById(req.user.id);
    if (!user || user.deletedAt) {
      return res.status(404).json({ error: 'Usuário não encontrado' });
    }
    const token = generateToken(user);
    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: 'Erro interno do servidor' });
  }
};
