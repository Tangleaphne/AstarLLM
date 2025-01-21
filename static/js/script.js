document.getElementById("send-button").addEventListener("click", function () {
    const recipient = document.getElementById("recipient").value.trim();
    const token = document.getElementById("token").value.trim();
    const amount = document.getElementById("amount").value.trim();
    const intention = document.getElementById("intention").value.trim();
    const warningMessage = document.getElementById("warning-message");
    const chatBox = document.getElementById("chat-box");

    if (!recipient || !token || !amount || !intention) {
        warningMessage.innerText = "All fields must be filled out before sending. Please complete the form.";
        warningMessage.style.display = "block";
        return;
    }

    if (!/^0x[a-fA-F0-9]{40}$/.test(recipient)) {
        warningMessage.innerText = "Recipient must be a valid Ethereum address.";
        warningMessage.style.display = "block";
        return;
    }

    if (isNaN(amount) || Number(amount) <= 0) {
        warningMessage.innerText = "Amount must be a positive number.";
        warningMessage.style.display = "block";
        return;
    }

    warningMessage.style.display = "none";

    const userMessage = document.createElement("div");
    userMessage.className = "message user";
    userMessage.innerText = `Recipient: ${recipient}, Token: ${token}, Amount: ${amount}, Intention: ${intention}`;
    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    const sendButton = document.getElementById("send-button");
    sendButton.disabled = true;
    sendButton.innerText = "Loading...";

    // Promise.all([
    //     fetch("/get_contract_bytecode", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ recipient }),
    //     }),
    //     fetch("/get_contract_abi", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ recipient }),
    //     }),
    //     fetch("/analyze_transaction", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ recipient, token, amount, intention }),
    //     }),
    // ])
    //     .then(([contractResponse, abiResponse, analysisResponse]) => {
    //         if (!contractResponse.ok || !abiResponse.ok || !analysisResponse.ok) {
    //             throw new Error("One of the requests failed.");
    //         }
    //         return Promise.all([contractResponse.json(), abiResponse.json(), analysisResponse.json()]);
    //     })
    //     .then(([contractData, abiData, analysisData]) => {
    //         const contractMessage = document.createElement("div");
    //         contractMessage.className = "message ai";
    //         if (contractData.bytecode) {
    //             contractMessage.innerText = `Contract Bytecode:\n${contractData.bytecode}`;
    //         } else {
    //             contractMessage.innerText = `Error fetching bytecode: ${contractData.error}`;
    //         }
    //         chatBox.appendChild(contractMessage);

    //         // 显示合约 ABI
    //         const abiMessage = document.createElement("div");
    //         abiMessage.className = "message ai";
    //         if (abiData.abi) {
    //             abiMessage.innerText = `Contract ABI:\n${abiData.abi}`;
    //         } else {
    //             abiMessage.innerText = `Error fetching ABI: ${abiData.error}`;
    //         }
    //         chatBox.appendChild(abiMessage);
            
    //         // const aiMessage = document.createElement("ReactMarkdown");
    //         const aiMessage = document.createElement("div");
    //         aiMessage.className = "message ai";
    //         if (analysisData.analysis) {
    //             aiMessage.innerText = `Analysis:\n${analysisData.analysis}`;
    //         } else {
    //             aiMessage.innerText = `Error analyzing transaction: ${analysisData.error}`;
    //         }
    //         chatBox.appendChild(aiMessage);
    //     })
    //     .catch((error) => {
    //         const errorMessage = document.createElement("div");
    //         errorMessage.className = "message ai";
    //         errorMessage.innerText = `Error: ${error.message}`;
    //         chatBox.appendChild(errorMessage);
    //     })
    //     .finally(() => {
    //         sendButton.disabled = false;
    //         sendButton.innerText = "Send";
    //         chatBox.scrollTop = chatBox.scrollHeight;
    //     });

    // 检测地址是否在黑名单中
    fetch("/check_blacklist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient }),
    })
    .then((response) => response.json())
    .then((blacklistData) => {
        const blacklistMessage = document.createElement("div");
        blacklistMessage.className = "message ai";
        if (blacklistData.status === "unsafe") { // 修改为与后端保持一致
            blacklistMessage.innerText = `Warning: The address is blacklisted. Message: ${blacklistData.message}`;
            chatBox.appendChild(blacklistMessage);
            throw new Error("Blacklisted address detected."); // 阻止进一步操作
        } else {
            blacklistMessage.innerText = "The address is safe. Proceeding with analysis.";
            chatBox.appendChild(blacklistMessage);
        }
    })

    .then(() => {
        // 并行调用获取字节码、ABI 和分析交易的 API
        return Promise.all([
            fetch("/get_contract_bytecode", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ recipient }),
            }),
            fetch("/get_contract_abi", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ recipient }),
            }),
            fetch("/analyze_transaction", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ recipient, token, amount, intention }),
            }),
        ]);
    })
    .then(([bytecodeResponse, abiResponse, analysisResponse]) => {
        if (!bytecodeResponse.ok || !abiResponse.ok || !analysisResponse.ok) {
            throw new Error("One of the API calls failed.");
        }
        return Promise.all([bytecodeResponse.json(), abiResponse.json(), analysisResponse.json()]);
    })
    .then(([bytecodeData, abiData, analysisData]) => {
        // 显示字节码
        const contractMessage = document.createElement("div");
        contractMessage.className = "message ai";
        if (bytecodeData.bytecode) {
            contractMessage.innerText = `Contract Bytecode:\n${bytecodeData.bytecode}`;
        } else {
            contractMessage.innerText = `Error fetching bytecode: ${bytecodeData.error}`;
        }
        chatBox.appendChild(contractMessage);

        // 显示合约 ABI
        const abiMessage = document.createElement("div");
        abiMessage.className = "message ai";
        if (abiData.abi) {
            abiMessage.innerText = `Contract ABI:\n${abiData.abi}`;
        } else {
            abiMessage.innerText = `Error fetching ABI: ${abiData.error}`;
        }
        chatBox.appendChild(abiMessage);

        // 显示分析结果
        const aiMessage = document.createElement("div");
        aiMessage.className = "message ai";
        if (analysisData.analysis) {
            aiMessage.innerText = `Analysis:\n${analysisData.analysis}`;
        } else {
            aiMessage.innerText = `Error analyzing transaction: ${analysisData.error}`;
        }
        chatBox.appendChild(aiMessage);
    })
    .catch((error) => {
    console.error("Error:", error);
    const errorMessage = document.createElement("div");
    errorMessage.className = "message ai error";
    errorMessage.innerText = `An error occurred: ${error.message}`;
    chatBox.appendChild(errorMessage);
    })
    .finally(() => {
        sendButton.disabled = false;
        sendButton.innerText = "Send";
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});
