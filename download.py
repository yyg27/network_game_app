from huggingface_hub import snapshot_download

##could not download normally on arch-linux so i wrote this cli-like python script
print("### 1/3 Downloading Model... ###")
snapshot_download(repo_id="Qwen/Qwen2.5-Coder-1.5B-Instruct")

print("\n ### 2/3 Downloading Dataset DEEP... ###")
snapshot_download(repo_id="Naholav/CodeGen-Deep-5K", repo_type="dataset")

print("\n ### 3/3 Downloading Dataset DIVERSE... ###")
snapshot_download(repo_id="Naholav/CodeGen-Diverse-5K", repo_type="dataset")

print("\nAll done...");