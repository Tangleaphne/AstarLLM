// static/js/script.js
document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("drop-zone");
    const chatBox = document.getElementById("chat-box");
    const warningMessage = document.getElementById("warning-message");
    const analyzeButton = document.getElementById("analyze-button");

    let fileTexts = {}; // 记录每个文件的内容（键为扩展名）

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        const files = Array.from(e.dataTransfer.files);
        fileTexts = {}; // 清空旧内容

        files.forEach(file => {
            const ext = file.name.split(".").pop().toLowerCase();
            const reader = new FileReader();
            reader.onload = function (event) {
                fileTexts[ext] = event.target.result;

                const userMessage = document.createElement("div");
                userMessage.className = "message user";
                userMessage.innerText = `📄 Loaded file: ${file.name}`;
                chatBox.appendChild(userMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            };
            reader.readAsText(file);
        });
    });

    analyzeButton.addEventListener("click", function () {
        const combinedText = (fileTexts["doc"] || "") + "\n\n" + (fileTexts["sol"] || "");

        if (!combinedText.trim()) {
            warningMessage.innerText = "⚠️ Please drag at least one .doc or .sol file.";
            warningMessage.style.display = "block";
            return;
        }

        warningMessage.style.display = "none";

        fetch("/analyze_text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: combinedText }),
        })
            .then((response) => response.json())
            .then((data) => {
                const aiMessage = document.createElement("div");
                aiMessage.className = "message ai";
                aiMessage.innerText = data.reply;
                chatBox.appendChild(aiMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch((error) => {
                const errorMessage = document.createElement("div");
                errorMessage.className = "message ai";
                errorMessage.innerText = `Error: ${error.message}`;
                chatBox.appendChild(errorMessage);
            });
    });
});
