document.addEventListener("DOMContentLoaded", function () {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const fileListDisplay = document.getElementById("file-list");
    const chatBox = document.getElementById("chat-box");
    const warningMessage = document.getElementById("warning-message");
    const analyzeButton = document.getElementById("analyze-button");
    const clearFilesButton = document.getElementById("clear-files-button");

    // Prompt selector elements (optional, ensure these IDs exist in your HTML if used)
    const backendPromptSelect = document.getElementById('backend-prompt-select');
    const frontendPromptSelect = document.getElementById('frontend-prompt-select');
    const finalPromptSelect = document.getElementById('final-prompt-select');


    let uploadedFilesData = [];

    function displayMessage(text, type = "user", isHtml = false) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${type}`;
        if (isHtml) {
            messageDiv.innerHTML = text;
        } else {
            messageDiv.textContent = text;
        }
        chatBox.appendChild(messageDiv);
        // Scroll to bottom smoothly
        chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
        return messageDiv; // Return for potential updates (like the 'thinking' message)
    }


    function resetUploadedFiles() {
        uploadedFilesData = [];
        fileListDisplay.innerHTML = "";
        if (fileInput) fileInput.value = ""; // Clear the file input
        displayMessage("Cleared all selected files. Ready for a new analysis.", "system");
    }

    function handleFiles(newlySelectedFiles) {
        warningMessage.style.display = "none";
        if (newlySelectedFiles.length === 0) return;

        const maxFiles = 3;
        if (uploadedFilesData.length + newlySelectedFiles.length > maxFiles) {
            warningMessage.textContent = `⚠️ Cannot add more files. Maximum of ${maxFiles} files. Selected: ${uploadedFilesData.length}, Trying to add: ${newlySelectedFiles.length}.`;
            warningMessage.className = "warning type-warning"; // Assuming you have CSS for this
            warningMessage.style.display = "block";
            if (fileInput) fileInput.value = "";
            return;
        }

        Array.from(newlySelectedFiles).forEach(file => {
            if (uploadedFilesData.some(existingFile => existingFile.name === file.name)) {
                displayMessage(`⚠️ File "${file.name}" is already in the list and was not added again.`, "system");
                return;
            }

            const reader = new FileReader();
            const fileName = file.name;
            const fileExtension = fileName.split('.').pop().toLowerCase();
            let fileTypeForRequest = "frontend";

            if (fileExtension === "sol") {
                fileTypeForRequest = "backend";
            } else if (!["doc", "docx", "pdf", "html", "txt"].includes(fileExtension)) {
                displayMessage(`⚠️ File type ".${fileExtension}" for "${fileName}" is not supported and will be ignored.`, "system");
                return;
            }

            reader.onload = function (event) {
                uploadedFilesData.push({
                    name: fileName,
                    content: event.target.result,
                    type: fileTypeForRequest
                });
                const p = document.createElement('p');
                // Adding an icon to the file list item
                const iconClass = fileExtension === "sol" ? "fa-code" : "fa-file-alt";
                p.innerHTML = `<i class="fas ${iconClass}"></i> ${fileName} <em>(${fileTypeForRequest})</em>`;
                fileListDisplay.appendChild(p);
            };
            reader.onerror = function () {
                displayMessage(`⚠️ Error reading file: ${fileName}`, "system");
            };
            reader.readAsText(file); // Still reads binary files as text, backend needs to handle
        });
        if (fileInput) fileInput.value = ""; // Clear input after processing
    }

    // --- Event Listeners ---
    if (dropZone) {
        dropZone.addEventListener("dragover", (e) => { e.preventDefault(); e.stopPropagation(); dropZone.classList.add("dragover"); });
        dropZone.addEventListener("dragleave", (e) => { e.preventDefault(); e.stopPropagation(); dropZone.classList.remove("dragover"); });
        dropZone.addEventListener("drop", (e) => { e.preventDefault(); e.stopPropagation(); dropZone.classList.remove("dragover"); handleFiles(e.dataTransfer.files); });
    } else { console.warn("Drop zone element with ID 'drop-zone' not found."); }

    if (fileInput) {
        fileInput.addEventListener("change", (e) => { handleFiles(e.target.files); });
    } else { console.warn("File input element with ID 'file-input' not found."); }

    if (clearFilesButton) {
        clearFilesButton.addEventListener("click", resetUploadedFiles);
    } else { console.warn("Clear files button with ID 'clear-files-button' not found."); }

    if (analyzeButton) {
        analyzeButton.addEventListener("click", function () {
            if (uploadedFilesData.length === 0) {
                warningMessage.textContent = "⚠️ Please upload at least one file to start the analysis.";
                warningMessage.className = "warning type-warning";
                warningMessage.style.display = "block";
                return;
            }
            warningMessage.style.display = "none";
            analyzeButton.disabled = true;
            analyzeButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...'; // Loading state
            if (clearFilesButton) clearFilesButton.disabled = true;

            displayMessage(`🚀 Initiating analysis for ${uploadedFilesData.length} file(s)... This might take a moment.`, "system");
            let thinkingMessageContainer = displayMessage(" ", "ai"); // Create an empty AI message container
            thinkingMessageContainer.innerHTML = `<div class="thinking-indicator"><div></div><div></div><div></div> Thinking...</div>`;


            const backendPromptPref = backendPromptSelect ? backendPromptSelect.value : "structured";
            const frontendPromptPref = frontendPromptSelect ? frontendPromptSelect.value : "structured";
            const finalPromptNameFromUI = finalPromptSelect ? finalPromptSelect.value : "simple_prompt.txt";

            const requestData = {
                files: uploadedFilesData,
                backend_prompt_preference: backendPromptPref,
                frontend_prompt_preference: frontendPromptPref,
                final_prompt_name: finalPromptNameFromUI
            };

            fetch("/analyze_files", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestData),
            })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then(err => {
                        const errorMsg = err.reply || err.error || `Server error: ${response.status}`;
                        throw new Error(errorMsg);
                    });
                }
                return response.json();
            })
            .then((data) => {
                if (data.final_analysis_result) {
                    if (typeof marked === 'function') {
                        thinkingMessageContainer.innerHTML = marked.parse(data.final_analysis_result);
                    } else {
                        console.warn("marked.js is not loaded. Displaying raw Markdown.");
                        thinkingMessageContainer.textContent = data.final_analysis_result;
                    }
                } else {
                    thinkingMessageContainer.textContent = "Received an empty or incomplete response from the server.";
                }

                if (data.final_result_saved_to) {
                    displayMessage(`ℹ️ Final analysis report saved to: ${data.final_result_saved_to}`, "system");
                }
                if (data.intermediate_results_saved) {
                    displayMessage("ℹ️ Intermediate analysis files have been saved on the server.", "system");
                }
            })
            .catch((error) => {
                console.error("Error during analysis fetch:", error);
                thinkingMessageContainer.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Error: ${error.message}`;
                thinkingMessageContainer.classList.add("error-message"); // Add class for specific error styling if needed
                warningMessage.textContent = `❌ Analysis failed: ${error.message}`;
                warningMessage.className = "warning type-error";
                warningMessage.style.display = "block";

            })
            .finally(() => {
                analyzeButton.disabled = false;
                analyzeButton.innerHTML = '<i class="fas fa-magic"></i> Analyze Files'; // Reset button text
                if (clearFilesButton) clearFilesButton.disabled = false;
                resetUploadedFiles(); // Clears files for the next round
                // displayMessage("Analysis process finished. Ready for new files.", "system"); // Kept resetUploadedFiles's own message
            });
        });
    } else { console.warn("Analyze button with ID 'analyze-button' not found."); }
});