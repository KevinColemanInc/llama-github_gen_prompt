# ReadMe

Data transformation script to transform Github API responses to LLM query strings

```python
from llama_github_gen_prompt import generate_prompt

generate_prompt(example_path, max_kb: 10).__next__()
```