const mongoose = require('mongoose');

const taskSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'Título é obrigatório'],
    trim: true,
    minlength: [3, 'Título deve ter pelo menos 3 caracteres'],
    maxlength: [100, 'Título deve ter no máximo 100 caracteres']
  },
  description: {
    type: String,
    trim: true,
    maxlength: [1000, 'Descrição deve ter no máximo 1000 caracteres']
  },
  status: {
    type: String,
    enum: ['pending', 'in_progress', 'done', 'cancelled'],
    default: 'pending'
  },
  priority: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    default: 'medium'
  },
  category: {
    type: String,
    trim: true,
    default: 'general'
  },
  assignedTo: {
    type: String,
    default: null
  },
  createdBy: {
    type: String,
    required: true
  },
  dueDate: {
    type: Date,
    default: null
  },
  tags: [{
    type: String,
    trim: true
  }],
  isActive: {
    type: Boolean,
    default: true
  },
  deletedAt: {
    type: Date,
    default: null
  }
}, {
  timestamps: true
});

taskSchema.index({ status: 1 });
taskSchema.index({ priority: 1 });
taskSchema.index({ createdBy: 1 });
taskSchema.index({ deletedAt: 1 });
taskSchema.index({ title: 'text', description: 'text' });

module.exports = mongoose.model('Task', taskSchema);
