from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class NLPService:
    def __init__(self, model_name="google/flan-t5-small"):
        print(f"Loading FLAN-T5 model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")
        print("FLAN-T5 model loaded.")

    def handle_instruction(self, text):
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=50)
        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return decoded
