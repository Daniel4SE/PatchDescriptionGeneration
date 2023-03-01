import os
import ipdb
import openai
import time
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch
from swap_signs import swap_sign
from multiprocessing import Pool

openai.api_key = "your openAI key"
# "Does this patch have some risks or involve some bugs, use a description describe and the description start with Yes or No:\n\n",
prompts = [
    "description of following codes:\n\n",
]

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "


def chatGPT_generator(_str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=_str,
        temperature=0.9,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )
    return response["choices"][0]["text"]


def exchange(lines):
    _lines = []
    for string in lines:
        # 将字符串按空格分割成列表
        words = string.split()

        # 遍历列表中的每个单词，如果以 "+" 开头则替换为 "-" 开头
        for i in range(len(words)):
            if words[i].startswith("+"):
                words[i] = "-" + words[i][1:]

        # 将列表中的单词重新组合成字符串，用空格分隔
        new_string = " ".join(words)

        print(new_string)  # 输出结果为 "-example string -with -pluses"

import os

def process_patches(datadict):
    codes = datadict["codes"]

    _codes = []
    for line in codes:
        sentences = line.split("<nl>")
        sentences = [swap_sign(j) for j in sentences]
        _codes.append("<nl>".join(sentences))
    datadict["codes"] = codes = _codes

    pos_chunks = chunk_list(codes, 50)
    pos_desc_dir = "pos_descriptions"
    if not os.path.exists(pos_desc_dir):
        os.makedirs(pos_desc_dir)
    pos_desc_files = []
    for i, chunk in enumerate(pos_chunks):
        desc_file = os.path.join(pos_desc_dir, f"chunk_{i}.txt")
        pos_desc_files.append(desc_file)
        if not os.path.exists(desc_file):
            try:
                descriptions = generate_descriptions(chunk, prompts[0])
                with open(desc_file, "w") as f:
                    f.write("\n".join(descriptions))
            except Exception as e:
                print(f"Failed to generate descriptions for chunk {i}: {e}")
    
    # concatenate descriptions from files
    posdescription = []
    for desc_file in pos_desc_files:
        with open(desc_file) as f:
            posdescription.extend(f.read().splitlines())

    datadict["posdescription"] = posdescription

    torch.save(datadict, "full.h5")



def chunk_list(lst, chunk_size):
    """Split a list into chunks of size chunk_size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def generate_descriptions(lines, prompt):
    descriptions = []
    for i in tqdm(lines):
        _i = i.split()
        if len(_i) > 150:
            i = " ".join(_i[:150])
        explanation = chatGPT_generator(prompt + i)
        last_nl_index = explanation.rfind("<nl>")
        if last_nl_index != -1:
            extracted_text = explanation[last_nl_index + len("<nl>"):].replace('\n','')
        else:
            extracted_text = explanation.replace('\n','')
        time.sleep(0.02)
        descriptions.append(extracted_text)
    return descriptions


if __name__ == "__main__":
    datadict = torch.load("your datadict.h5")
    process_patches(datadict)

