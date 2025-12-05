import torch #pytorch
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

x = torch.rand(5, 3)
print(x)

print("is CUDA available?:", torch.cuda.is_available())
print("Device count:", torch.cuda.device_count())

if torch.cuda.is_available():
    print("GPU Model:", torch.cuda.get_device_name(0))
else:
    print("[ERROR]: Could not find GPU")

dataset_deep = load_dataset("Naholav/CodeGen-Deep-5K")
dataset_diverse = load_dataset("Naholav/CodeGen-Diverse-5K")

model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
system_prompt = "You are an expert Python programmer. Please read the problem carefully before writing any Python code."
output_log = "./qwen-deep-lora"

#config for 3050 Mobile GPU(4GB VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0 ##best practice to use 6.0. So this means dont shrink down important big numbers to keep model's intelligencec
)