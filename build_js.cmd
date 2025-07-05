mkdir tmp
call npx frida-compile -S src\script\native\index.ts -o tmp\native.js
call npx frida-compile -S src\script\java\index.ts -o tmp\java.js
call npx frida-compile -S src\script\extra\index.ts -o tmp\extra.js
call npx frida-compile -S src\script\trainer\index.ts -o tmp\trainer.js
pause
