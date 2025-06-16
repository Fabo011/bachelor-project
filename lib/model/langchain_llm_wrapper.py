from typing import Optional, List, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import LLMResult, ChatGeneration
from langchain_core.messages import AIMessage
from langchain_core.callbacks import CallbackManagerForLLMRun


class SimpleLangChainLLMWrapper(BaseChatModel):
    llm: Any

    @property
    def _llm_type(self) -> str:
        return "simple-langchain-llm-wrapper"

    def _generate(
        self,
        messages: List[List[Any]],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> LLMResult:
        generations: List[List[ChatGeneration]] = []

        for i, message_list in enumerate(messages):
            prompt_pieces = []
            for msg in message_list:
                if hasattr(msg, "content"):
                    prompt_pieces.append(msg.content)
                elif isinstance(msg, (tuple, list)) and len(msg) > 1:
                    prompt_pieces.append(str(msg[1]))
                elif isinstance(msg, dict):
                    if "content" in msg:
                        prompt_pieces.append(str(msg["content"]))
                    elif "text" in msg:
                        prompt_pieces.append(str(msg["text"]))
                    else:
                        prompt_pieces.append(str(msg))
                else:
                    prompt_pieces.append(str(msg))

            prompt = "\n".join(prompt_pieces)
            print(f"DEBUG: Prompt #{i} to LLM:\n{prompt}\n")

            raw_output = self.llm.generate([prompt], stop=stop, **kwargs)
            print(f"DEBUG: Raw output from LLM:\n{raw_output}\n")

            generation_list = []
            for gen in raw_output.generations[0]:  # all generations for this prompt
                generation_list.append(ChatGeneration(message=AIMessage(content=gen.text)))

            print(f"DEBUG: Extracted ChatGenerations:\n{generation_list}\n")

            generations.append(generation_list)

        print(f"DEBUG: Returning LLMResult with generations:\n{generations}\n")

        return LLMResult(generations=generations)

    async def agenerate(
       self,
       messages: List[List[Any]],
       stop: Optional[List[str]] = None,
       run_manager: Optional[CallbackManagerForLLMRun] = None,
       **kwargs
    ) -> LLMResult:
      # just call the sync _generate method wrapped in an async context
      # If your underlying llm supports async, use that instead
      return self._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

    def bind_tools(self, tools):
        return self





