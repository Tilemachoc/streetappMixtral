from transformers import BitsAndBytesConfig
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model_id7x8 = "mistralai/Mixtral-8x7B-Instruct-v0.1"

tokenizer7x8 = AutoTokenizer.from_pretrained(
    model_id7x8,
    cache_dir="cache_dir",
    trust_remote_code=True,)

model7x8 = AutoModelForCausalLM.from_pretrained(
    model_id7x8,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
    attn_implementation="flash_attention_2",
    cache_dir="cache_dir",
)


model_id7 = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer7 = AutoTokenizer.from_pretrained(
    model_id7,
    cache_dir="cache_dir",
    trust_remote_code=True,)

model7 = AutoModelForCausalLM.from_pretrained(
    model_id7,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
    attn_implementation="flash_attention_2",
    cache_dir="cache_dir",
)