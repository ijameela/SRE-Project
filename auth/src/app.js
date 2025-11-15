const http = require('http');

const server = http.createServer((req, res) => {
  res.end('Hello from AUTH service!');
});

server.listen(4000, () => {
  console.log('Auth service running on port 4000');
});
