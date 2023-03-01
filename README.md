# PatchDescriptionGeneration
Patch Description Generation with GPT3, it supports breakpoint resumes
## Patch Description Generator

This code generates descriptions for code patches using OpenAI's GPT-3 language model. The generated descriptions are then saved to a file for each patch.

### Code Structure

- `chatGPT_generator(_str)`: generates a description for a single patch using OpenAI's GPT-3 language model.
- `exchange(lines)`: replaces "+" signs in the input lines with "-" signs.
- `chunk_list(lst, chunk_size)`: splits a list into chunks of size `chunk_size`.
- `generate_descriptions(lines)`: generates descriptions for a list of code patches using `chatGPT_generator()`.
- `process_patches(datadict)`: processes the code patches in `datadict` and saves the resulting descriptions to files.

### Outputs

The generated patch descriptions are saved to separate files for positive and negative patches in the `pos_descriptions` and `neg_descriptions` directories, respectively. The `full.h5` file is also updated with the generated descriptions.


## Overview
This set of codes includes several functions that can generate code descriptions based on given code snippets using OpenAI's GPT-3 model.

The code includes the following functions:

- `chatGPT_generator`: Uses OpenAI's GPT-3 model to generate descriptions for a given code snippet.
- `exchange`: Takes a list of code snippets as input, swaps "+" with "-" in each snippet, and returns the modified snippets.
- `process_patches`: Takes a dictionary of code snippets as input, processes each snippet to generate descriptions using `generate_descriptions`, and saves the descriptions to a file.

## Dependencies
The code depends on the following libraries:

- `os`
- `ipdb`
- `openai`
- `time`
- `collections`
- `matplotlib`
- `tqdm`
- `torch`
- `multiprocessing`

## Usage
Before running the code, you need to set your OpenAI API key in the following line:

```
openai.api_key = "your openAI key"
```

To use the `process_patches` function, you need to provide a dictionary of code snippets in the following format:
```
datadict = {
    "codes": ["code snippet 1", "code snippet 2", ...]
}

```

You can then call the process_patches function as follows:
```
process_patches(datadict)
```
This function will process each code snippet in `datadict`, generate a description for it using `generate_descriptions`, and save the descriptions to a file.

## License
This code is released under the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT).