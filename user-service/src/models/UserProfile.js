const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userProfileSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true, select: false },
  role: { type: String, enum: ['admin', 'user'], default: 'user' },
  bio: { type: String, maxlength: 500 },
  avatar: { type: String },
  isActive: { type: Boolean, default: true },
  deletedAt: { type: Date, default: null }
}, { timestamps: true });

userProfileSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Usa a mesma coleção 'users' do auth-service para compartilhar dados
module.exports = mongoose.model('UserProfile', userProfileSchema, 'users');
