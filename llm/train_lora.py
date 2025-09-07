"""
LoRA fine-tune script (Trainer-based).
Requirements: transformers, datasets, accelerate, peft, bitsandbytes
Run: python train_lora.py --model_name_or_path <base_hf_model> --train_file train_examples.jsonl --output_dir ./lora_adapter
"""
import argparse
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", required=True)  # e.g. "meta-llama/Llama-2-7b-hf" or your HF-converted base
    parser.add_argument("--train_file", required=True)
    parser.add_argument("--output_dir", default="./lora_adapter")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=1)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        load_in_8bit=True,           # uses bitsandbytes
        device_map="auto"
    )

    # Prepare model for k-bit training (quantized training)
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # common for Llama-like
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)

    # dataset: expects fields instruction,input,output
    dataset = load_dataset("json", data_files=args.train_file, split="train")

    def concat_and_tokenize(example):
        # create single text from instruction + input + output for causal training
        prompt = example.get("instruction", "")
        if example.get("input"):
            prompt += "\n\nInput: " + example["input"]
        prompt += "\n\nOutput: " + example["output"]
        tokenized = tokenizer(prompt, truncation=True, max_length=1024)
        return {"input_ids": tokenized["input_ids"], "attention_mask": tokenized["attention_mask"]}

    dataset = dataset.map(concat_and_tokenize, remove_columns=dataset.column_names)

    data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        logging_steps=20,
        save_strategy="epoch",
        fp16=True,
        learning_rate=2e-4,
        remove_unused_columns=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=data_collator
    )

    trainer.train()

    # Save PEFT adapter (not merged)
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Saved LoRA adapter to", args.output_dir)

if __name__ == "__main__":
    main()
