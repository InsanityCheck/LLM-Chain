


API_KEY = None
API_KWARGS = None

def empty_api(text_input: str) -> str:
    return ""

def call_openai_api(text_input: str) -> str:
    import openai
    if API_KEY is None:
        raise ValueError("API_KEY is not set. Please set it with LLMLib.set_api_key(api_key)")
    openai.api_key = API_KEY
    config = {
        "model": "text-davinci-002",
        "prompt": text_input,
        "max_tokens": 100,
        "temperature": 0.9,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    try:
        config.update(API_KWARGS)
    except AttributeError:
        print("No LLM_kwargs set. Using default values. You can set it with LLMLib.set_api_kwargs(api_kwargs)")
    response = openai.Completion.create(**config) 
    text_output = response.choices[0].text
    return text_output



USED_API = None



def call_LLM(text_input: str) -> str:
    global USED_API
    if USED_API is None:
        print("No API set. Using Empty API by default. Please set it with LLMLib.set_api(api)")
        USED_API = empty_api
    return USED_API(text_input)
    