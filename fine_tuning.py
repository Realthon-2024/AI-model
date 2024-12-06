import google.generativeai as genai
import time
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

base_model = "models/gemini-1.5-flash-001-tuning"

data_path = "data/legal_data.json"

try:
    with open(data_path, "r") as file:
        raw_data = json.load(file)
        training_data = [
            {
                "text_input": item["question"],  
                "output": item["answer"]         
            }
            for item in raw_data
        ]
except FileNotFoundError:
    print(f"Error: File not found at {data_path}")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {data_path}")
    exit(1)

operation = genai.create_tuned_model(
    display_name="legal_model",
    source_model=base_model,
    epoch_count=20,
    batch_size=4,
    learning_rate=0.001,
    training_data=training_data,
)

print("Fine-tuning started...")
for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print("Fine-tuning completed!")
print(result)

snapshots = pd.DataFrame(result.tuning_task.snapshots)
print("Final Loss:", snapshots["mean_loss"].iloc[-1])

tuned_model_name = result.name
model = genai.GenerativeModel(model_name=tuned_model_name)

example_input = "산업재해로 인해 병원에 입원하면 치료비는 누가 부담하나요?"
response = model.generate_content(example_input)
print(f"Input: {example_input}")
print(f"Output: {response.text}")
