import subprocess
import os

def run_slither_analysis(source_code_path, recipient):
    CONTAINER_ID = os.getenv("CONTAINER_ID")
    corrected_path = source_code_path.replace("\\", "/")
    print(f"corrected_path: {corrected_path}")

    analysis_path = corrected_path + "/analysis.md"
    print(f"analysis_path: {analysis_path}")
    docker_command = (
        f'docker exec -it {CONTAINER_ID} /bin/bash -c "slither {corrected_path}/SourceCode.sol --checklist > {analysis_path}"'
    )
    
    try:
        # 不设置 check=True，让命令执行即使非零退出码也不会抛出异常
        result = subprocess.run(docker_command, shell=True, stdout=subprocess.DEVNULL)

        # 检查 Slither 是否生成了 analysis.md 文件
        if not os.path.exists(analysis_path):
            raise RuntimeError("Slither analysis failed: analysis.md not created.")
        
        # 检查文件内容是否为空
        with open(analysis_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                raise RuntimeError("Slither analysis failed: analysis.md is empty.")

    except Exception as e:
        raise RuntimeError(f"Slither analysis failed: {str(e)}")


    return analysis_path
