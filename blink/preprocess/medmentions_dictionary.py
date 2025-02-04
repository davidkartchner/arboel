import os
import json
import pickle
from tqdm import tqdm

BLINK_ROOT = f"{os.path.abspath(os.path.dirname(__file__))}/../.."

input_dir = os.path.join(BLINK_ROOT, "data", "medmentions", "documents")
output_dir = os.path.join(
    BLINK_ROOT,
    "data",
    "medmentions",
    "processed",
)
output_fpath = os.path.join(output_dir, "dictionary.pickle")

dictionary = []
label_ids = set()

for doc_fname in tqdm(os.listdir(input_dir), desc="Loading docuemnts"):
    assert doc_fname.endswith(".json")
    entity_type = doc_fname.split(".")[0]
    if entity_type in ["train", "test", "val"]:
        continue
    with open(os.path.join(input_dir, doc_fname), "r") as f:
        for idx, line in enumerate(f):
            record = {}
            entity = json.loads(line.strip())
            record["cui"] = entity["document_id"]
            record["title"] = entity["title"]
            record["description"] = entity["text"]
            record["type"] = entity_type
            dictionary.append(record)
            label_ids.add(record["cui"])

assert len(dictionary) == len(label_ids)

print(f"Finished reading {len(dictionary)} entities")
print("Saving entity dictionary...")

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
with open(output_fpath, "wb") as write_handle:
    pickle.dump(dictionary, write_handle, protocol=pickle.HIGHEST_PROTOCOL)
