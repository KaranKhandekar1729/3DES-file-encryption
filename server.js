const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const cors = require('cors')

const app = express()
const upload = multer({ dest: "uploads/" })

app.use(express.static("."))
app.use(cors())

app.post("/process", upload.single("file"), (req, res) => {
    const { operation, key } = req.body
    const filePath = req.file.path

    const py = spawn("python", [
        "des.py", // python script
        operation, // encrypt/decrypt
        filePath,
        key
    ])

    py.on("close", (code) => {
        if (code !== 0) {
            return res.status(500).send("Python script error")
        }
        res.download(filePath, (err) => {
            fs.unlinkSync(filePath)
        })
    })
    py.stdout.on("data", (data) => {
        console.log(`PYTHON STDOUT: ${data}`);
    });

    py.stderr.on("data", (data) => {
        console.error(`PYTHON STDERR: ${data}`);
    });
})

app.listen(3000, () => console.log("Server running at PORT 3000"))