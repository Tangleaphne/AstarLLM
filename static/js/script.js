document.getElementById("send-button").addEventListener("click", function () {
    const userInput = document.getElementById("chat-input").value;
    const chatBox = document.getElementById("chat-box");

    // 显示用户消息
    chatBox.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;
    document.getElementById("chat-input").value = "";

    // 发送请求到后端
    fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput }),
    })
        .then((response) => response.json())
        .then((data) => {
            // 显示 AI 回复
            chatBox.innerHTML += `<div><strong>AI:</strong> ${data.reply}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
});
