import chalk from "chalk";

console.log(chalk.red('안녕'));

import path from 'path'
import process from 'process'


// console.log(import.meta.dirname)
// console.log(import.meta.filename)
// console.log(path.resolve())     // path이거 많이 쓰임. 실행경로 확인할 때,
// console.log(process.cwd())



console.log(path.join('samsung', 'yourapp', 'abcd'))
console.log(path.resolve('samsung', 'yourapp', 'abcd'))
