from flask import Flask, render_template, request, jsonify
import requests
import os
import json
import re
import time
import logging # <--- 添加这行
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# --- Configuration ---
GPT_API_URL = os.getenv("GPT_API_URL", "https://api.openai.com/v1/chat/completions")
GPT_API_KEY = os.getenv("GPT_API_KEY")
if not GPT_API_KEY:
    app.logger.error("FATAL: GPT_API_KEY environment variable not set.")

# --- Result Storage Directories ---
BASE_RESULTS_DIR = "analysis_results"
BACKEND_RESULTS_DIR = os.path.join(BASE_RESULTS_DIR, "backend")
FRONTEND_RESULTS_DIR = os.path.join(BASE_RESULTS_DIR, "frontend")
FINAL_RESULTS_DIR = os.path.join(BASE_RESULTS_DIR, "final")

# Create directories if they don't exist
os.makedirs(BACKEND_RESULTS_DIR, exist_ok=True)
os.makedirs(FRONTEND_RESULTS_DIR, exist_ok=True)
os.makedirs(FINAL_RESULTS_DIR, exist_ok=True)

# --- File Type Definitions ---
BACKEND_FILE_EXTENSIONS = {".sol"}
FRONTEND_FILE_EXTENSIONS = {".doc", ".docx", ".pdf", ".html", ".txt"}
# IMPORTANT: Add logic here or in call_gpt_api to handle text extraction for .doc, .docx, .pdf
# For now, it assumes they are read as text by the frontend, which is incorrect for binary files.

# --- Helper Functions ---
def sanitize_filename(filename):
    if filename is None: return "unknown_file"
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename if filename else "untitled"

def load_prompt_content(category, preference="simple", custom_prompt_name=None):
    prompt_filename = ""
    if category == "final":
        prompt_filename = custom_prompt_name or "simple_prompt.txt"
        prompt_path = os.path.join("prompt", "final", prompt_filename)
    elif category in ["backend", "frontend"]:
        prompt_filename = f"{preference}_prompt.txt" # e.g., "structured_prompt.txt"
        prompt_path = os.path.join("prompt", category, prompt_filename)
    else:
        app.logger.error(f"Invalid prompt category: {category}")
        return None
    try:
        with open(prompt_path, "r", encoding="utf-8") as f: return f.read().strip()
    except FileNotFoundError:
        app.logger.error(f"Prompt file not found: {prompt_path}")
        return None
    except Exception as e:
        app.logger.error(f"Error loading prompt {prompt_path}: {str(e)}")
        return None

def call_gpt_api(prompt_content, file_content_for_api, model="gpt-4o-mini", is_json_expected=False):
    if not GPT_API_KEY: return "Error: GPT_API_KEY is not configured on the server."

    full_prompt = f"{prompt_content}\n\n--- Provided Content Start ---\n{file_content_for_api}\n--- Provided Content End ---"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GPT_API_KEY}"}
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a highly skilled DApp security and consistency auditing assistant. Analyze the provided information carefully, follow instructions precisely, and ensure your response is well-formatted (JSON or Markdown as requested by the user prompt)."},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.2, # Lower temperature for more deterministic structured output
        # "max_tokens": 3500, # Adjust as needed
    }

    # Add response_format if JSON is expected and model supports it
    # Check OpenAI documentation for latest models supporting JSON mode
    if is_json_expected and model in ["gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo-0125", "gpt-4-0125-preview"]: # Example models
        payload["response_format"] = {"type": "json_object"}
        app.logger.info(f"Attempting to use JSON mode for model {model} due to structured prompt.")

    try:
        response = requests.post(GPT_API_URL, headers=headers, json=payload, timeout=180)
        response.raise_for_status()
        response_data = response.json()
        if "error" in response_data:
            error_msg = response_data["error"].get("message", "Unknown API error")
            app.logger.error(f"OpenAI API Error: {error_msg}")
            return f"API Error: {error_msg}"
        
        # Log usage (optional)
        usage = response_data.get("usage")
        if usage:
            app.logger.info(f"API call usage for model {model}: Prompt tokens: {usage.get('prompt_tokens')}, Completion tokens: {usage.get('completion_tokens')}, Total tokens: {usage.get('total_tokens')}")

        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "No response from API.")
    except requests.exceptions.Timeout:
        app.logger.error(f"OpenAI API call timed out after 180 seconds for model {model}.")
        return "Error: The request to the language model timed out."
    except requests.exceptions.RequestException as e:
        app.logger.error(f"OpenAI API request error: {str(e)} - Response: {e.response.text if e.response else 'No response object'}")
        return f"Error during API call: {str(e)}"
    except Exception as e:
        app.logger.error(f"Unexpected error in call_gpt_api: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"


def save_analysis_result(content_to_save, original_filename_base, stage_or_category, prompt_type_used, is_json_format, target_sub_dir):
    sanitized_base = sanitize_filename(original_filename_base)
    file_extension = "json" if is_json_format else "md"
    
    # Consistent filename structure: {base}_{stage/category}_{prompt_type}.{ext}
    output_filename_leaf = f"{sanitized_base}_{stage_or_category}_{prompt_type_used}_analysis.{file_extension}"
    full_save_path = os.path.join(target_sub_dir, output_filename_leaf)

    try:
        with open(full_save_path, "w", encoding="utf-8") as f:
            if is_json_format:
                text_content = str(content_to_save).strip()
                # Enhanced cleaning for JSON wrapped in Markdown
                if text_content.startswith("```json"):
                    text_content = text_content[len("```json"):].strip()
                elif text_content.startswith("```"): # Handle cases where only ``` is present
                    text_content = text_content[len("```"):].strip()
                
                if text_content.endswith("```"):
                    text_content = text_content[:-len("```")].strip()
                
                try:
                    json_data = json.loads(text_content)
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                except json.JSONDecodeError as json_err:
                    app.logger.warning(f"Content for {full_save_path} was expected as JSON but failed to parse after cleaning. Error: {json_err}. Saving raw text. Raw content preview: {text_content[:300]}...")
                    f.write(str(content_to_save)) # Save original API reply if JSON parsing fails
            else: # Markdown or plain text
                f.write(str(content_to_save))
        app.logger.info(f"Analysis result saved to: {full_save_path}")
        return full_save_path
    except Exception as e_save:
        app.logger.error(f"Error saving analysis file {full_save_path}: {str(e_save)}")
        return None

# --- Main Route ---
@app.route("/")
def index_route():
    return render_template("index.html")

@app.route("/analyze_files", methods=["POST"])
def analyze_files_route():
    data = request.json
    if not data: return jsonify({"reply": "No JSON data received.", "error": "Bad Request"}), 400

    files_data = data.get("files", [])
    backend_prompt_pref = data.get("backend_prompt_preference", "simple")
    frontend_prompt_pref = data.get("frontend_prompt_preference", "simple")
    final_prompt_filename_full = data.get("final_prompt_name", "simple_prompt.txt")

    if not files_data: return jsonify({"reply": "No files provided for analysis."}), 400
    if not GPT_API_KEY: return jsonify({"reply": "API Key is not configured on the server. Please contact administrator."}), 500

    intermediate_results_saved_flag = False
    backend_analysis_summary_parts = []
    frontend_analysis_summary_parts = []

    # Determine a base name for the final report from the first uploaded file or a default
    first_file_base_name_for_report = "analysis_session" # Default
    if files_data and files_data[0].get("name"):
        first_file_base_name_for_report, _ = os.path.splitext(files_data[0].get("name"))


    # Stage 1 & 2: Backend and Frontend File Analysis
    for file_info in files_data:
        file_name = file_info.get("name", "unknown_file.tmp")
        file_content = file_info.get("content", "")
        file_category_type = file_info.get("type", "frontend") # From JS file type detection

        original_file_base, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        current_prompt_text = None
        current_prompt_pref = ""
        target_save_dir = ""
        is_json_expected_for_api = False

        if ext in BACKEND_FILE_EXTENSIONS and file_category_type == "backend":
            current_prompt_text = load_prompt_content("backend", backend_prompt_pref)
            current_prompt_pref = backend_prompt_pref
            target_save_dir = BACKEND_RESULTS_DIR
            stage_name_for_file = "backend"
            is_json_expected_for_api = (backend_prompt_pref == "structured")
        elif ext in FRONTEND_FILE_EXTENSIONS and file_category_type == "frontend":
            # REMINDER: Implement actual text extraction for .pdf, .doc, .docx here
            # For now, assuming file_content is usable text.
            if ext in [".pdf", ".doc", ".docx"]:
                 app.logger.warning(f"File {file_name} is a binary type ({ext}). Current setup reads it as text. Implement proper text extraction for accurate analysis.")
            current_prompt_text = load_prompt_content("frontend", frontend_prompt_pref)
            current_prompt_pref = frontend_prompt_pref
            target_save_dir = FRONTEND_RESULTS_DIR
            stage_name_for_file = "frontend"
            is_json_expected_for_api = (frontend_prompt_pref == "structured")
        else:
            app.logger.info(f"Skipping file {file_name} due to unrecognized type or category mismatch.")
            continue

        if current_prompt_text:
            app.logger.info(f"Processing {stage_name_for_file} file: {file_name} with '{current_prompt_pref}' prompt.")
            # Pass is_json_expected_for_api to call_gpt_api
            api_result = call_gpt_api(current_prompt_text, file_content, is_json_expected=is_json_expected_for_api)
            
            if "API Error:" not in api_result and "Error:" not in api_result : # Basic check for API success
                if stage_name_for_file == "backend":
                    backend_analysis_summary_parts.append(f"--- Analysis for {file_name} (Backend - {current_prompt_pref}) ---\n{api_result}\n")
                else:
                    frontend_analysis_summary_parts.append(f"--- Analysis for {file_name} (Frontend - {current_prompt_pref}) ---\n{api_result}\n")
                
                if save_analysis_result(api_result, original_file_base, stage_name_for_file, current_prompt_pref, is_json_expected_for_api, target_save_dir):
                    intermediate_results_saved_flag = True
            else:
                app.logger.error(f"API call failed for {file_name}. Result: {api_result}")
                # Optionally, add this error to the summary parts for the final report
                summary_list = backend_analysis_summary_parts if stage_name_for_file == "backend" else frontend_analysis_summary_parts
                summary_list.append(f"--- ERROR processing {file_name} ({stage_name_for_file} - {current_prompt_pref}) ---\n{api_result}\n")
        else:
            app.logger.warning(f"Could not load prompt for {stage_name_for_file} file {file_name} (preference: {current_prompt_pref}). Skipping.")

    # Stage 3: Final Consolidated Analysis
    final_prompt_type_for_filename, _ = os.path.splitext(final_prompt_filename_full)
    final_prompt_text = load_prompt_content("final", custom_prompt_name=final_prompt_filename_full)
    
    final_api_output = "Error: Final analysis prompt could not be loaded or an earlier error occurred."
    final_report_path = None

    if final_prompt_text:
        if not backend_analysis_summary_parts and not frontend_analysis_summary_parts:
            final_api_output = "No intermediate backend or frontend analysis results were generated. Cannot perform final analysis."
            app.logger.info(final_api_output)
        else:
            # Construct a more informative combined input for the final prompt
            combined_input_for_final_prompt = f"DApp Analysis Context:\n"
            combined_input_for_final_prompt += f"User has selected '{backend_prompt_pref}' prompt for backend files and '{frontend_prompt_pref}' for frontend files.\n"
            combined_input_for_final_prompt += "Please provide a consolidated report based on the following individual analyses:\n\n"
            combined_input_for_final_prompt += "== Backend Analysis Snippets ==\n" + ("\n".join(backend_analysis_summary_parts) if backend_analysis_summary_parts else "No backend files were analyzed or results available.\n")
            combined_input_for_final_prompt += "\n\n== Frontend Analysis Snippets ==\n" + ("\n".join(frontend_analysis_summary_parts) if frontend_analysis_summary_parts else "No frontend files were analyzed or results available.\n")

            app.logger.info(f"Performing final analysis using prompt: {final_prompt_filename_full} on combined results.")
            final_api_output = call_gpt_api(final_prompt_text, combined_input_for_final_prompt, model="gpt-4o-mini") # Consider a more capable model for final summary

            # Save the final Markdown report
            # Filename: {first_file_base}_{frontend_pref}_{backend_pref}_{final_prompt_type}_final_report_analysis.md
            final_report_filename_identifier = f"{sanitize_filename(first_file_base_name_for_report)}_{frontend_prompt_pref}_{backend_prompt_pref}"
            # stage_or_category = "final_summary", prompt_type_used = final_prompt_type_for_filename
            final_report_path = save_analysis_result(
                final_api_output,
                final_report_filename_identifier,
                "final_summary", 
                final_prompt_type_for_filename,
                is_json_format=False, # Final report is Markdown
                target_sub_dir=FINAL_RESULTS_DIR
            )
    else:
        app.logger.error(f"Final analysis prompt '{final_prompt_filename_full}' could not be loaded. Skipping final analysis.")

    return jsonify({
        "final_analysis_result": final_api_output,
        "intermediate_results_saved": intermediate_results_saved_flag,
        "final_result_saved_to": final_report_path
    })

if __name__ == "__main__":
    app.logger.info("DApp Insight Engine Flask application starting...")
    # Standard logging for development
    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
    else: # Basic production logging (consider more robust solutions like Gunicorn logging)
        if not os.path.exists('logs'): os.makedirs('logs')
        file_handler = logging.handlers.RotatingFileHandler('logs/app.log', maxBytes=102400, backupCount=5)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application started in production mode.')
    
    app.run(debug=True, port=os.getenv("PORT", 5000))