![alt text](img/image.png)

## 1. Project Phase Breakdown (4 Stages)

1. **Dataset Refinement & Optimization**  
   - Complete and enhance our dataset during experiments.

2. **Front-End Upgrade**  
   - Integrate the web crawler, sharding, and other work you’ve already done.  
   - Explore processing strategies beyond the current Prompt.

3. **Back-End Upgrade**  
   - Build on the existing “PROMPT” logic in our GitHub repo, adding Slither analysis, transaction-risk checks, and blacklist-address interaction analysis.  
   - Investigate additional processing approaches beyond the current Prompt.

4. **Prototype Development & Experimental Validation**  
   - Create a simple front-end page for testers to:  
     - Select **Simple Prompt** or **Structured Prompt**  
     - Drag-and-drop files to trigger processing  
   - Verify that:  
     - **Structured Prompt** → generates and saves a JSON intermediate file  
     - **Simple Prompt** → generates and saves a Markdown intermediate file  
   - Evaluate the effectiveness of both usage scenarios

---

## 2. Overall Tool Workflow

1. **File Classification**  
   - When a user drops in files, the system detects each file’s type and routes it to the “front-end” or “back-end” channel.

2. **Invoke Prompt & Generate Intermediate Files**  
   - **Front-end files** → undergo front-end pre-processing, then call the front-end Prompt  
   - **Back-end files** → call the back-end Prompt  
   - Both paths issue a ChatGPT API request and output the corresponding JSON intermediate file

3. **Result Consolidation (optional, may skip to step 4)**  
   - Merge the front-end and back-end JSON outputs plus any Prompt-derived content into a unified “user result” dataset

4. **Comparative Analysis & Final Output**  
   - Call the ChatGPT API again to compare the two JSON results side-by-side  
   - Generate the final formatted output per the Prompt and display it in the UI  
   - All intermediate files and API call logs remain on the back-end; the front-end only shows the final result

---

## 3. Software Prototype & Two Modes

### A. Experimental Mode (Internal Testing)

- **UI Features:**  
  - Toggle between Simple and Structured Prompt  
  - Drag-and-drop upload area  
- **Outputs:**  
  - **Structured Prompt** → JSON files  
  - **Simple Prompt** → Markdown files  

### B. Production Mode (End User)

- **Two Input Options:**  
  1. **DApp Address / Website URL**  
     - User enters a smart-contract address or page URL  
     - System calls Etherscan (or similar) API to fetch source code, then pre-processes it  
  2. **Direct File Upload**  
     - User drags front-end or back-end source files into the interface  

- **View Differences:**  
  - **Developer View:** can switch prompts, inspect full JSON and logs  
  - **User View:** shows only the final report; all intermediate steps are hidden  
