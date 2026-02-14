const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting Plant Disease Classification System...\n');

// Start FastAPI Backend
console.log('🔬 Starting FastAPI Backend on port 8000...');
const backend = spawn('python', ['-m', 'uvicorn', 'main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'], {
  cwd: path.join(__dirname, 'backend'),
  stdio: 'inherit',
  shell: true
});

// Wait a moment for backend to start
setTimeout(() => {
  console.log('⚛️  Starting React Frontend on port 5173...');

  // Start React Frontend
  const frontend = spawn('npm', ['run', 'dev'], {
    cwd: path.join(__dirname, 'frontend'),
    stdio: 'inherit',
    shell: true
  });

  console.log('\n✅ Both servers are running!');
  console.log('🌐 Frontend: http://localhost:5173');
  console.log('🔧 Backend:  http://localhost:8000');
  console.log('📚 API Docs: http://localhost:8000/docs');
  console.log('\n💡 Open http://localhost:5173 in your browser to use the app!');
  console.log('❌ Press Ctrl+C to stop both servers\n');

  // Handle process termination
  process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down servers...');
    backend.kill();
    frontend.kill();
    process.exit(0);
  });

}, 3000);