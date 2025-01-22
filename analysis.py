import subprocess
import os
from utils import extract_solidity_version


def update_solc_version_in_docker(container_id, version):
    """
    更新 Docker 容器中的 solc 版本。
    """
    if version == "Unknown":
        print("Solidity version not found, skipping update.")
        return

    try:
        # 安装指定版本的 solc
        # install_command = f'docker exec -it {container_id} solc-select install {version}'
        docker_command_install_solc = (f'docker exec -it {container_id} solc-select install {version}'  )
        subprocess.run(docker_command_install_solc, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 切换到指定版本的 solc
        # use_command = f'docker exec -it {container_id} solc-select use {version}'
        docker_command_use_solc = (f'docker exec -it {container_id} solc-select use {version}')
        subprocess.run(docker_command_use_solc, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Updated solc version in Docker to {version}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to update solc version in Docker: {e}")


# def run_slither_analysis(source_code_path, recipient):
#     CONTAINER_ID = os.getenv("CONTAINER_ID")
#     corrected_path = source_code_path.replace("\\", "/")
#     print(f"corrected_path: {corrected_path}")

#     analysis_path = corrected_path + "/analysis.md"
#     print(f"analysis_path: {analysis_path}")
#     docker_command = (
#         f'docker exec -it {CONTAINER_ID} /bin/bash -c "slither {corrected_path}/SourceCode.sol --checklist > {analysis_path}"'
#     )
    
#     try:
#         # 不设置 check=True，让命令执行即使非零退出码也不会抛出异常
#         result = subprocess.run(docker_command, shell=True, stdout=subprocess.DEVNULL)

#         # 检查 Slither 是否生成了 analysis.md 文件
#         if not os.path.exists(analysis_path):
#             raise RuntimeError("Slither analysis failed: analysis.md not created.")
        
#         # 检查文件内容是否为空
#         with open(analysis_path, "r", encoding="utf-8") as file:
#             content = file.read().strip()
#             if not content:
#                 raise RuntimeError("Slither analysis failed: analysis.md is empty.")

#     except Exception as e:
#         raise RuntimeError(f"Slither analysis failed: {str(e)}")


#     return analysis_path


def run_slither_analysis(source_code_path, recipient):
    """
    运行 Slither 分析，确保使用正确的 solc 版本。
    """
    CONTAINER_ID = os.getenv("CONTAINER_ID")
    corrected_path = source_code_path.replace("\\", "/")
    analysis_path = corrected_path + "/analysis.md"

    # 提取 Solidity 版本并更新 solc
    source_code_file = os.path.join(corrected_path, "SourceCode.sol")
    with open(source_code_file, "r", encoding="utf-8") as file:
        source_code = file.read()

    solidity_version = extract_solidity_version(source_code)
    update_solc_version_in_docker(CONTAINER_ID, solidity_version)

    # 运行 Slither 分析
    docker_command = (
        f'docker exec -it {CONTAINER_ID} /bin/bash -c "slither {corrected_path}/SourceCode.sol --checklist > {analysis_path}"'
    )

    try:
        result = subprocess.run(docker_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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