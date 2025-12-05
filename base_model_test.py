import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model_id = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
system_prompt = "You are an expert Python programmer. Please read the problem carefully before writing any Python code."

#config for 3050 Mobile GPU(4GB VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0 ##best practice to use 6.0. So this means dont shrink down important big numbers to keep model's intelligence
)

tokenizer = AutoTokenizer.from_pretrained(model_id) ##to turn text to binaries

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config, 
    device_map="auto" ##find and use on pc GPU
)

test_questions = [
    "Write a Python function that checks if a number is prime",
    "Write a Python function that checks if a given string is a palindrome"
]

print("### Base Model Test ###")

for i, question in enumerate(test_questions, 1):
    print(f"Question: {i}: {question}")
    print("\n" + "="*50)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    print(response)
    print("\n" + "="*50 + "\n")

print("Base Model Test has been completed")