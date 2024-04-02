# Python file for functions dedicated to allowing users to run the pipeline
# 2024-03-25

from graph_generation import generate_graph_for_method
from graph2path import graph2path
import json
import os
import numpy as np


# Function that takes a java function with no function name or {} and returns the AST representation in desired format
def source_code_to_AST_rep_pipeline(method, mode="onePath"):
    os.remove("data/tempgraphs/tmp_AST_output.json")
    generate_graph_for_method("tmp", method, "data/tempgraphs")
    graph2path("data/tempgraphs", mode=mode, output_file_path="data/paths.json")

    methods = json.loads(open("data/paths.json").read())
    if mode == "onePath":
        return methods["tmp"][0]
    elif mode == "paths":
        return " | ".join(methods["tmp"])
    else:
        return -1


# Function that takes a prompt and returns the model's predictions
# Input should be ran through source_code_to_AST_rep_pipeline first if trying to enter plain source code
def prompt_model(prompt, num_tokens, tokenizer, model):
    query = "<mask>" * num_tokens + "(...)" + prompt
    inp = tokenizer(query, return_tensors="tf")
    mask_loc = np.where(inp.input_ids.numpy()[0] == tokenizer.mask_token_id)[0].tolist()
    out = model(inp).logits[0].numpy()
    predicted_tokens = np.argmax(out[mask_loc], axis=1).tolist()
    return tokenizer.decode(predicted_tokens)
