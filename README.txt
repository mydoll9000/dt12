
TT12 PRO SYSTEM

Contents
- tt12_pro.db : database
- api_fastapi.py : Python FastAPI server
- api_node.js : NodeJS API
- web_index.html : simple search interface

Run Python API
pip install fastapi uvicorn
uvicorn api_fastapi:app --reload

Run Node API
npm install express sqlite3
node api_node.js
