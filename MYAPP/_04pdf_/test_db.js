import mysql from 'mysql2/promise';

const pool = mysql.createPool({     
    host: 'svc.sel3.cloudtype.app', user: 'root', password: '1234', database: 'BANG',
    port: 31776, waitForConnections: true, connectionLimit: 10,
})

const result = pool.query('select * from emp')
// 여기까지는 공식.

result.then((res) => {
    console.log(res);
    pool.end()
})
