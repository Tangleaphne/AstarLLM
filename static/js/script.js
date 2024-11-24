document.getElementById("send-button").addEventListener("click", function () {
    const userInput = document.getElementById("chat-input").value;
    const chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return; // 忽略空消息

    // 显示用户消息（靠右）
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = userInput;
    chatBox.appendChild(userMessage);

    // 清空输入框
    document.getElementById("chat-input").value = "";

    // 模拟 AI 回复
    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
    })
        .then((response) => response.json())
        .then((data) => {
            // 显示 AI 消息（靠左）
            const aiMessage = document.createElement("div");
            aiMessage.className = "message ai";
            aiMessage.innerText = data.reply;
            chatBox.appendChild(aiMessage);

            // 自动滚动到底部
            chatBox.scrollTop = chatBox.scrollHeight;
        });
});
