import express from 'express';

// middleware 연습때만 사용
import {logger} from './middleware/logger.js';

const app = express();

app.use(logger)     // middleware 연습때만 사용

// route 함수
app.get('/', (req, res) => {
    res.status(200).type('html').send('<h1>Hello, Express!</h1>');
});

app.listen(3000, () => {
    console.log('http://localhost:3000 실행 중');
});