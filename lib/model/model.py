from langchain_community.llms import Ollama
from lib.model.langchain_llm_wrapper import SimpleLangChainLLMWrapper

llm = Ollama(
    model="deepseek-lite", # or llama3
    verbose=True,
)

llm_wrapper = SimpleLangChainLLMWrapper(llm=llm)


