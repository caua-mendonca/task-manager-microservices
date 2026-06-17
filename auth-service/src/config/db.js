const mongoose = require('mongoose');

const connectDB = async (retries = 5, delay = 3000) => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      await mongoose.connect(process.env.MONGO_URI, { dbName: 'taskmanager' });
      console.log('✅ MongoDB conectado (auth-service)');
      return;
    } catch (err) {
      if (attempt === retries) {
        console.error('❌ MongoDB falhou após todas as tentativas:', err.message);
        process.exit(1);
      }
      console.warn(`⚠️  Tentativa ${attempt}/${retries} falhou. Aguardando ${delay / 1000}s...`);
      await new Promise((r) => setTimeout(r, delay));
    }
  }
};

module.exports = connectDB;
