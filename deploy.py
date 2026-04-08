import os
from huggingface_hub import HfApi

def deploy():
    api = HfApi()
    token = os.getenv("HF_TOKEN", "REMOVED_FOR_SECURITY")
    repo_id = "Teja5454/web_tutor_env"
    
    print(f"Creating/checking Space: {repo_id}...")
    try:
        api.create_repo(
            repo_id=repo_id, 
            repo_type="space", 
            space_sdk="docker", 
            token=token, 
            exist_ok=True
        )
        print("Space is ready.")
    except Exception as e:
        print(f"Warning on create_repo: {e}")
        
    print("Uploading project files securely...")
    try:
        api.upload_folder(
            folder_path="E:/web_tutor_env",
            repo_id=repo_id,
            repo_type="space",
            token=token,
            ignore_patterns=["*.venv*", "*.git*", "__pycache__*", "deploy.py", "deploy_log.txt"]
        )
        print(f"Deploy complete! Check your space at: https://huggingface.co/spaces/{repo_id}")
    except Exception as e:
        print(f"Deploy Error: {e}")

if __name__ == "__main__":
    deploy()
