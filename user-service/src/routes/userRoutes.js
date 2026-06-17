const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const { authenticate, adminOnly } = require('../middleware/authMiddleware');

/**
 * @swagger
 * tags:
 *   name: Users
 *   description: Gerenciamento de usuários
 */

/**
 * @swagger
 * /api/users:
 *   get:
 *     summary: Lista todos os usuários (admin)
 *     tags: [Users]
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
 *         name: search
 *         schema: { type: string }
 *         description: Filtra por nome (regex case-insensitive)
 *     responses:
 *       200:
 *         description: Lista paginada de usuários
 *       401:
 *         description: Não autorizado
 *       403:
 *         description: Acesso negado (apenas admin)
 */
router.get('/', authenticate, adminOnly, userController.getAllUsers);

/**
 * @swagger
 * /api/users/{id}:
 *   get:
 *     summary: Busca usuário por ID
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *         description: ID do usuário
 *     responses:
 *       200:
 *         description: Dados do usuário
 *       403:
 *         description: Acesso negado (usuário só acessa o próprio perfil)
 *       404:
 *         description: Usuário não encontrado
 */
router.get('/:id', authenticate, userController.getUserById);

/**
 * @swagger
 * /api/users/{id}:
 *   put:
 *     summary: Atualiza dados do usuário
 *     tags: [Users]
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
 *               name:
 *                 type: string
 *               bio:
 *                 type: string
 *               avatar:
 *                 type: string
 *               role:
 *                 type: string
 *                 enum: [admin, user]
 *                 description: Apenas admins podem alterar o role
 *     responses:
 *       200:
 *         description: Usuário atualizado com sucesso
 *       403:
 *         description: Acesso negado
 *       404:
 *         description: Usuário não encontrado
 */
router.put('/:id', authenticate, userController.updateUser);

/**
 * @swagger
 * /api/users/{id}:
 *   delete:
 *     summary: Soft delete do usuário (admin)
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200:
 *         description: Usuário desativado
 *       401:
 *         description: Não autorizado
 *       403:
 *         description: Acesso negado (apenas admin)
 *       404:
 *         description: Usuário não encontrado
 */
router.delete('/:id', authenticate, adminOnly, userController.deleteUser);

module.exports = router;
