
const express = require('express')
const sqlite3 = require('sqlite3').verbose()
const app = express()

const db = new sqlite3.Database('tt12_pro.db')

app.get('/work/:code',(req,res)=>{
 db.all('SELECT * FROM work_items WHERE code=?',[req.params.code],(e,r)=>res.json(r))
})

app.get('/search',(req,res)=>{
 db.all('SELECT code,description FROM work_items WHERE description LIKE ? LIMIT 20',
 ['%'+req.query.q+'%'],(e,r)=>res.json(r))
})

app.listen(3000,()=>console.log("TT12 API running"))
