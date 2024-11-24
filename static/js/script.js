document.getElementById("send-button").addEventListener("click", function () {
    const recipient = document.getElementById("recipient").value.trim();
    const token = document.getElementById("token").value.trim();
    const amount = document.getElementById("amount").value.trim();
    const intention = document.getElementById("intention").value.trim();
    const warningMessage = document.getElementById("warning-message"); // 获取专门的警告信息区域

    // 检查输入框是否为空
    if (!recipient || !token || !amount || !intention) {
        // 显示警告信息，而非使用聊天气泡
        warningMessage.innerText = "All fields must be filled out before sending. Please complete the form.";
        warningMessage.style.display = "block"; // 显示警告信息
        return; // 停止后续逻辑
    }

    // 隐藏警告信息（当所有字段都填写时）
    warningMessage.style.display = "none";

    // 显示用户输入（聊天气泡形式）
    const chatBox = document.getElementById("chat-box");
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = `Recipient: ${recipient}, Token: ${token}, Amount: ${amount}, Intention: ${intention}`;
    chatBox.appendChild(userMessage);

    // 清空输入框
    document.getElementById("recipient").value = "";
    document.getElementById("token").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("intention").value = "";

    // 模拟发送请求到后端
    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, token, amount, intention }),
    })
        .then((response) => response.json())
        .then((data) => {
            // 显示 AI 的反馈（聊天气泡形式）
            const aiMessage = document.createElement("div");
            aiMessage.className = "message ai";
            aiMessage.innerText = data.reply;
            chatBox.appendChild(aiMessage);

            // 自动滚动到底部
            chatBox.scrollTop = chatBox.scrollHeight;
        });
});
