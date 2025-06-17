import os
from langchain_community.llms import GPT4All
from lib.model.langchain_llm_wrapper import SimpleLangChainLLMWrapper

model_path = os.path.expanduser("~/.cache/gpt4all")
model_file = os.path.join(model_path, "Meta-Llama-3-8B-Instruct.Q4_0.gguf")

llm = GPT4All(
    model=model_file,
    verbose=True,
)

llm_wrapper = SimpleLangChainLLMWrapper(llm=llm)

