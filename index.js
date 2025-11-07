import express from "express";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = 3000;

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/top50", (req, res) => {
  const python = spawn("python", ["scraper.py"]);
  let data = "";

  python.stdout.on("data", (chunk) => {
    data += chunk.toString();
  });

  python.on("close", () => {
    try {
      const json = JSON.parse(data.trim());
      res.json(json);
    } catch (err) {
      console.error("Erro ao converter JSON:", err);
      console.log("Saída recebida:", data);
      res.status(500).json({ error: "JSON inválido" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`✅ Servidor rodando em http://localhost:${PORT}`);
});
