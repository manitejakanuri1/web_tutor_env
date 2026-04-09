import os
import getpass
from huggingface_hub import HfApi

def sync():
    print("="*60)
    print("    HUGGING FACE DEPLOYMENT SYNC")
    print("="*60)
    print("Because your previous Hugging Face token was revoked for")
    print("your safety, we need a brand new one to upload the fixes.")
    print("")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Click 'Create new token' (Make sure to select 'Write' permission)")
    print("3. Copy the token and paste it here.")
    
    token = getpass.getpass("\nPaste New Hugging Face Token (typing is hidden): ").strip()
    
    if not token.startswith("hf_"):
        print("\nFailure: Invalid token format! It must start with 'hf_'")
        return
        
    print("\nSyncing local fixes to Hugging Face...")
    api = HfApi()
    try:
        api.upload_folder(
            folder_path="E:/web_tutor_env",
            repo_id="Teja5454/web_tutor_env",
            repo_type="space",
            token=token,
            ignore_patterns=["*.venv*", ".git*", "__pycache__*", "*log*.txt", "agent_test*"]
        )
        print("\nSUCCESS! Your files are now perfectly synced to Hugging Face!")
        print("Wait 60 seconds, then hit 'Update Submission' on the Hackathon portal!")
    except Exception as e:
        print(f"\nUpload Failed: {e}")

if __name__ == "__main__":
    sync()
