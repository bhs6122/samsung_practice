// /greet/:name 요청을 처리하는 라우터 모듈

import express from 'express';
const router = express.Router();

// 코드 작성 1) GET /:name 라우트 작성하기
// router.get('/:name', (req, res) => { ... })
// 함수 안에서 할 일:
//   - req.params.name으로 이름 꺼내기
//   - req.query.age로 나이 꺼내기 (age는 안 넘어오면 undefined)
//   - age가 있으면: `<h2>안녕하세요, ${name}님! ${age}살이시군요.</h2>` 응답
//   - age가 없으면: `<h2>안녕하세요, ${name}님!</h2>` 응답
//   - res.send(내용)으로 응답

export default router;