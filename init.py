import os

project_name = "AstarLLM"
folders = [
    f"{project_name}/static/css",
    f"{project_name}/static/js",
    f"{project_name}/templates"
]
files = {
    f"{project_name}/app.py": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello, Flask Skeleton!'\n\nif __name__ == '__main__':\n    app.run(debug=True)",
    f"{project_name}/static/css/style.css": "/* Add your styles here */",
    f"{project_name}/static/js/script.js": "// Add your scripts here",
    f"{project_name}/templates/index.html": "<!DOCTYPE html>\n<html>\n<head>\n<title>Flask Skeleton</title>\n</head>\n<body>\n<h1>Hello, Flask Skeleton!</h1>\n</body>\n</html>"
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file_path, content in files.items():
    with open(file_path, "w") as file:
        file.write(content)

print(f"Flask project '{project_name}' created successfully!")
