from langchain import PromptTemplate
import json
import os

input_prompt = PromptTemplate(
    input_variables=[
        "RepoName",
        "RepoDescription",
        "Filenames",
        "PrTitle",
        "PrBody",
        "GitDiff",
    ],
    template="""Below is an instruction that describes a task, paired with an input that provides further context. Write a code diff that appropriately completes the request.
### Instruction:
Generate a code diff that {PrTitle} and {PrBody} for {RepoName} and {RepoDescription}

### Input:
Filenames: {Filenames} 

### Response:
{GitDiff}""",
)

too_big_kb_count = 0
def generate_prompt(example_path, max_kb: 10):
    """
    Generates a prompt from examples
    """
    for path, _, files in os.walk(example_path, topdown=False):
        for filename in files:
            if filename.endswith(".json"):
                fullpath = os.path.join(path, filename)
                # next if file is bigger than 10kb
                if os.path.getsize(fullpath) > max_kb * 1024:
                    too_big_kb_count += 1
                    continue

                # load the json file
                with open(fullpath, "r") as f:
                    # load the json data
                    data = json.load(f)
                    yield input_prompt.format(
                        RepoName=data["RepoName"],
                        RepoDescription=data["RepoDescription"],
                        Filenames=data["Filenames"],
                        PrTitle=data["PrTitle"],
                        PrBody=data["PrBody"],
                        GitDiff=data["GitDiff"],
                    )
    return None

def stats():
  return {too_big_kb_count: too_big_kb_count}