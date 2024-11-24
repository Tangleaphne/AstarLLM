document.getElementById("send-button").addEventListener("click", function () {
    const recipient = document.getElementById("recipient").value.trim();
    const token = document.getElementById("token").value.trim();
    const amount = document.getElementById("amount").value.trim();
    const intention = document.getElementById("intention").value.trim();
    const chatBox = document.getElementById("chat-box");

    // 检查输入框是否为空
    if (!recipient || !token || !amount || !intention) {
        const warningMessage = document.createElement("div");
        warningMessage.className = "message ai"; // 让提示也以气泡形式显示
        warningMessage.innerText = "All fields must be filled out before sending. Please complete the form.";
        chatBox.appendChild(warningMessage);

        // 自动滚动到底部
        chatBox.scrollTop = chatBox.scrollHeight;

        return; // 停止发送
    }

    // 显示用户输入
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = `Recipient: ${recipient}, Token: ${token}, Amount: ${amount}, Intention: ${intention}`;
    chatBox.appendChild(userMessage);

    // 清空输入框
    document.getElementById("recipient").value = "";
    document.getElementById("token").value = "";
    document.getElementById("amount").value = "";
    document.getElementById("intention").value = "";

    // 发送请求到后端
    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, token, amount, intention }),
    })
        .then((response) => response.json())
        .then((data) => {
            // 显示 AI 的反馈
            const aiMessage = document.createElement("div");
            aiMessage.className = "message ai";
            aiMessage.innerText = data.reply;
            chatBox.appendChild(aiMessage);

            // 自动滚动到底部
            chatBox.scrollTop = chatBox.scrollHeight;
        });
});
