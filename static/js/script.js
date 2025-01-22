document.getElementById("send-button").addEventListener("click", function () {
    const recipient = document.getElementById("recipient").value.trim();
    const token = document.getElementById("token").value.trim();
    const amount = document.getElementById("amount").value.trim();
    const intention = document.getElementById("intention").value.trim();
    const warningMessage = document.getElementById("warning-message"); // 获取专门的警告信息区域
    const chatBox = document.getElementById("chat-box"); // 聊天记录框

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
    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = `Recipient: ${recipient}, Token: ${token}, Amount: ${amount}, Intention: ${intention}`;
    chatBox.appendChild(userMessage);

    // 调用后端新端点
    fetch("/analyze_and_advise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient, token, amount, intention }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                throw new Error(data.error);
            }

            // 显示安全性评估
            const securityMessage = document.createElement("div");
            securityMessage.className = "message ai";
            securityMessage.innerText = `Security Assessment: ${data.security_assessment}`;
            chatBox.appendChild(securityMessage);

            // 显示功能解析
            const functionalityMessage = document.createElement("div");
            functionalityMessage.className = "message ai";
            functionalityMessage.innerText = `Functionality Analysis: ${data.functionality_analysis}`;
            chatBox.appendChild(functionalityMessage);

            // 自动滚动到底部
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch((error) => {
            const errorMessage = document.createElement("div");
            errorMessage.className = "message ai";
            errorMessage.innerText = `Error: ${error.message}`;
            chatBox.appendChild(errorMessage);
        });
});
