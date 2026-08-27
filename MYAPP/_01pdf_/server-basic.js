// import http from 'http';

// const server = http.createServer((req, res) => {
//     res.statusCode = 200; // 200 OK
//     res.setHeader('Content-Type', 'text/plain');
//     res.end('Hello, HTTP Server!');
// });

// server.listen(3000, () => {
//     console.log('서버 실행 중: http://localhost:3000');
// });


import http from 'http';

const server = http.createServer((req, res) => {
    res.statusCode = 200; // 200 OK
    res.setHeader('Content-Type', 'text/html');     // html로
    res.end('Hello, HTTP Server!');
});

server.listen(3000, () => {
    console.log('서버 실행 중: http://localhost:3000');
});

