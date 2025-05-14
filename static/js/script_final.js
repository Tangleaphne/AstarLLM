document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("drop-zone"); // 全屏热区
    const chatBox = document.getElementById("chat-box");
    const warningMessage = document.getElementById("warning-message");
    const analyzeButton = document.getElementById("analyze-button");
    const textInput = document.getElementById("text-input");

    let fileTexts = {}; // 记录每个文件类型的内容

    // 让整个页面都支持拖拽
    ["dragover", "dragleave", "drop"].forEach(eventName => {
        document.body.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (eventName === "dragover") {
                dropZone.classList.add("dragover");
            } else {
                dropZone.classList.remove("dragover");
            }
        });
    });

    // 处理文件拖拽
    document.body.addEventListener("drop", (e) => {
        const files = Array.from(e.dataTransfer.files);
        if (!files.length) return;
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

    // 分析按钮点击事件
    analyzeButton.addEventListener("click", function () {
        const combinedText =
            (textInput.value || "") +
            "\n\n" +
            (fileTexts["doc"] || "") +
            "\n\n" +
            (fileTexts["sol"] || "");

        if (!combinedText.trim()) {
            warningMessage.innerText = "⚠️ Please input some text or drag at least one .doc or .sol file.";
            warningMessage.style.display = "block";
            return;
        }
        warningMessage.style.display = "none";

        // 显示用户输入
        if (textInput.value.trim()) {
            const userMessage = document.createElement("div");
            userMessage.className = "message user";
            userMessage.innerText = "📝 " + textInput.value.trim();
            chatBox.appendChild(userMessage);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // 显示"分析中"提示
        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai";
        aiMessage.innerText = "🤖 Analyzing, please wait...";
        chatBox.appendChild(aiMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        fetch("/analyze_text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: combinedText }),
        })
            .then((response) => response.json())
            .then((data) => {
                aiMessage.innerText = data.reply;
                chatBox.scrollTop = chatBox.scrollHeight;
            })
            .catch((error) => {
                aiMessage.innerText = `Error: ${error.message}`;
            });
    });
});
