// greet.js 라우터를 불러와서 /greet 요청을 처리하는 서버

import express from 'express';
// 코드 작성 2) greet.js에서 라우터 불러오기
// import 이름 from './파일명.js'

const app = express();

// 코드 작성 3) '/greet' 경로로 들어오는 요청을 greetRouter에게 위임하기
// app.use('/경로', 라우터)

app.listen(3000, () => {
    console.log('http://localhost:3000 서버 실행 중');
});