
import LLM_Chain.LLMCaller as LLMCaller
from typing import Callable

def set_API_used(used_api: Callable):
    LLMCaller.USED_API = used_api

def set_api_key(api_key):
    LLMCaller.API_KEY = api_key

def set_api_kwargs(api_kwargs):
    LLMCaller.API_KWARGS = api_kwargs