const express = require('express');
const { body } = require('express-validator');
const router = express.Router();
const taskController = require('../controllers/taskController');
const { authenticate, authorize } = require('../middleware/authMiddleware');

const taskValidation = [
  body('title').trim().isLength({ min: 3, max: 100 }).withMessage('Título deve ter entre 3 e 100 caracteres'),
  body('status').optional().isIn(['pending', 'in_progress', 'done', 'cancelled']),
  body('priority').optional().isIn(['low', 'medium', 'high', 'critical']),
  body('dueDate').optional().isISO8601().withMessage('Data deve ser no formato ISO 8601')
];

/**
 * @swagger
 * tags:
 *   name: Tasks
 *   description: Gerenciamento de tarefas
 */

// ── Rotas ──────────────────────────────────────────────
/**
 * @swagger
 * /api/tasks:
 *   get:
 *     summary: Lista todas as tarefas com filtros e paginação
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: query
 *         name: page
 *         schema: { type: integer, default: 1 }
 *       - in: query
 *         name: limit
 *         schema: { type: integer, default: 10 }
 *       - in: query
 *         name: status
 *         schema: { type: string, enum: [pending, in_progress, done, cancelled] }
 *       - in: query
 *         name: priority
 *         schema: { type: string, enum: [low, medium, high, critical] }
 *       - in: query
 *         name: search
 *         schema: { type: string }
 *       - in: query
 *         name: sortBy
 *         schema: { type: string, default: createdAt }
 *       - in: query
 *         name: order
 *         schema: { type: string, enum: [asc, desc], default: desc }
 *     responses:
 *       200:
 *         description: Lista de tarefas com paginação
 */
router.get('/', authenticate, taskController.getAllTasks);

/**
 * @swagger
 * /api/tasks/name/{title}:
 *   get:
 *     summary: Busca tarefas por nome
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: title
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200:
 *         description: Tarefas encontradas
 */
router.get('/name/:title', authenticate, taskController.getTaskByTitle);

/**
 * @swagger
 * /api/tasks/{id}:
 *   get:
 *     summary: Busca tarefa por ID
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200:
 *         description: Tarefa encontrada
 *       404:
 *         description: Não encontrada
 */
router.get('/:id', authenticate, taskController.getTaskById);

/**
 * @swagger
 * /api/tasks:
 *   post:
 *     summary: Cria uma nova tarefa
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required: [title]
 *             properties:
 *               title: { type: string }
 *               description: { type: string }
 *               status: { type: string, enum: [pending, in_progress, done, cancelled] }
 *               priority: { type: string, enum: [low, medium, high, critical] }
 *               category: { type: string }
 *               dueDate: { type: string, format: date }
 *               tags: { type: array, items: { type: string } }
 *     responses:
 *       201:
 *         description: Tarefa criada
 */
router.post('/', authenticate, taskValidation, taskController.createTask);

/**
 * @swagger
 * /api/tasks/{id}:
 *   put:
 *     summary: Atualiza uma tarefa
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Tarefa atualizada
 */
router.put('/:id', authenticate, taskValidation, taskController.updateTask);

/**
 * @swagger
 * /api/tasks/{id}/status:
 *   patch:
 *     summary: Atualiza apenas o status da tarefa
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               status: { type: string, enum: [pending, in_progress, done, cancelled] }
 *     responses:
 *       200:
 *         description: Status atualizado
 */
router.patch('/:id/status', authenticate, taskController.updateStatus);

/**
 * @swagger
 * /api/tasks/{id}:
 *   delete:
 *     summary: Soft delete de uma tarefa
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200:
 *         description: Tarefa deletada (soft delete)
 */
router.delete('/:id', authenticate, taskController.deleteTask);

// Rotas admin
router.delete('/:id/hard', authenticate, authorize('admin'), taskController.hardDeleteTask);
router.post('/:id/restore', authenticate, authorize('admin'), taskController.restoreTask);

module.exports = router;
