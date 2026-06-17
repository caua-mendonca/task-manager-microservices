const UserProfile = require('../models/UserProfile');

exports.getAllUsers = async (req, res) => {
  try {
    const { page = 1, limit = 10, search } = req.query;
    const filter = { deletedAt: null };
    if (search) filter.name = { $regex: search, $options: 'i' };

    const [users, total] = await Promise.all([
      UserProfile.find(filter).skip((page - 1) * limit).limit(Number(limit)),
      UserProfile.countDocuments(filter)
    ]);

    res.json({ data: users, pagination: { total, page: Number(page), limit: Number(limit) } });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao listar usuários' });
  }
};

exports.getUserById = async (req, res) => {
  try {
    const user = await UserProfile.findOne({ _id: req.params.id, deletedAt: null });
    if (!user) return res.status(404).json({ error: 'Usuário não encontrado' });
    if (req.user.role !== 'admin' && req.user.id !== req.params.id) {
      return res.status(403).json({ error: 'Acesso negado' });
    }
    res.json({ data: user });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar usuário' });
  }
};

exports.updateUser = async (req, res) => {
  try {
    if (req.user.role !== 'admin' && req.user.id !== req.params.id) {
      return res.status(403).json({ error: 'Acesso negado' });
    }
    const { password, role, ...allowedFields } = req.body;
    if (req.user.role === 'admin') {
      allowedFields.role = role;
    }
    const user = await UserProfile.findByIdAndUpdate(
      req.params.id,
      { $set: allowedFields },
      { new: true, runValidators: true }
    );
    if (!user) return res.status(404).json({ error: 'Usuário não encontrado' });
    res.json({ message: 'Usuário atualizado', data: user });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao atualizar usuário' });
  }
};

exports.deleteUser = async (req, res) => {
  try {
    const user = await UserProfile.findOneAndUpdate(
      { _id: req.params.id, deletedAt: null },
      { deletedAt: new Date(), isActive: false },
      { new: true }
    );
    if (!user) return res.status(404).json({ error: 'Usuário não encontrado' });
    res.json({ message: 'Usuário desativado (soft delete)' });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao deletar usuário' });
  }
};
