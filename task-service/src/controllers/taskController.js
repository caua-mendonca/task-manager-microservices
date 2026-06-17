const { validationResult } = require('express-validator');
const Task = require('../models/Task');

exports.getAllTasks = async (req, res) => {
  try {
    const {
      page = 1, limit = 10,
      status, priority, category,
      search, sortBy = 'createdAt', order = 'desc',
      assignedTo
    } = req.query;

    const filter = { deletedAt: null };

    if (status) filter.status = status;
    if (priority) filter.priority = priority;
    if (category) filter.category = category;
    if (assignedTo) filter.assignedTo = assignedTo;
    if (search) filter.$text = { $search: search };

    if (req.user.role !== 'admin') {
      filter.createdBy = req.user.id;
    }

    const sortOrder = order === 'asc' ? 1 : -1;
    const skip = (Number(page) - 1) * Number(limit);

    const [tasks, total] = await Promise.all([
      Task.find(filter)
        .sort({ [sortBy]: sortOrder })
        .skip(skip)
        .limit(Number(limit)),
      Task.countDocuments(filter)
    ]);

    res.json({
      data: tasks,
      pagination: {
        total,
        page: Number(page),
        limit: Number(limit),
        totalPages: Math.ceil(total / Number(limit))
      }
    });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao listar tarefas', details: err.message });
  }
};

exports.getTaskById = async (req, res) => {
  try {
    const task = await Task.findOne({ _id: req.params.id, deletedAt: null });
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada' });

    if (req.user.role !== 'admin' && task.createdBy !== req.user.id) {
      return res.status(403).json({ error: 'Acesso negado' });
    }

    res.json({ data: task });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar tarefa' });
  }
};

exports.getTaskByTitle = async (req, res) => {
  try {
    const filter = {
      title: { $regex: req.params.title, $options: 'i' },
      deletedAt: null
    };
    if (req.user.role !== 'admin') filter.createdBy = req.user.id;

    const tasks = await Task.find(filter);
    res.json({ data: tasks });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar tarefa por nome' });
  }
};

exports.createTask = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

  try {
    const task = await Task.create({
      ...req.body,
      createdBy: req.user.id
    });
    res.status(201).json({ message: 'Tarefa criada com sucesso', data: task });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao criar tarefa', details: err.message });
  }
};

exports.updateTask = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) return res.status(400).json({ errors: errors.array() });

  try {
    const task = await Task.findOne({ _id: req.params.id, deletedAt: null });
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada' });

    if (req.user.role !== 'admin' && task.createdBy !== req.user.id) {
      return res.status(403).json({ error: 'Acesso negado' });
    }

    const updated = await Task.findByIdAndUpdate(
      req.params.id,
      { $set: req.body },
      { new: true, runValidators: true }
    );

    res.json({ message: 'Tarefa atualizada', data: updated });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao atualizar tarefa', details: err.message });
  }
};

exports.updateStatus = async (req, res) => {
  try {
    const { status } = req.body;
    const validStatuses = ['pending', 'in_progress', 'done', 'cancelled'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Status inválido' });
    }

    const task = await Task.findOneAndUpdate(
      { _id: req.params.id, deletedAt: null },
      { status },
      { new: true }
    );
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada' });

    res.json({ message: 'Status atualizado', data: task });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao atualizar status' });
  }
};

exports.deleteTask = async (req, res) => {
  try {
    const task = await Task.findOne({ _id: req.params.id, deletedAt: null });
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada' });

    if (req.user.role !== 'admin' && task.createdBy !== req.user.id) {
      return res.status(403).json({ error: 'Acesso negado' });
    }

    await Task.findByIdAndUpdate(req.params.id, { deletedAt: new Date(), isActive: false });
    res.json({ message: 'Tarefa deletada com sucesso (soft delete)' });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao deletar tarefa' });
  }
};

exports.hardDeleteTask = async (req, res) => {
  try {
    const task = await Task.findByIdAndDelete(req.params.id);
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada' });
    res.json({ message: 'Tarefa permanentemente deletada' });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao deletar tarefa permanentemente' });
  }
};

exports.restoreTask = async (req, res) => {
  try {
    const task = await Task.findOneAndUpdate(
      { _id: req.params.id, deletedAt: { $ne: null } },
      { deletedAt: null, isActive: true },
      { new: true }
    );
    if (!task) return res.status(404).json({ error: 'Tarefa não encontrada ou não deletada' });
    res.json({ message: 'Tarefa restaurada', data: task });
  } catch (err) {
    res.status(500).json({ error: 'Erro ao restaurar tarefa' });
  }
};
