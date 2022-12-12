from typing import Union, Any
from .LLMCaller import call_LLM



class _AbstractBaseLLMModule():

    def __init__(self, appendToInput=False, **kwargs) -> None:
        self.appendToInput = appendToInput

        
    def preprocess(self, text_input="", **kwargs) -> str:
        return text_input

    def LLM_call(self, text_input: str) -> str:
        text_output = call_LLM(text_input)
        return text_input, text_output
    
    def postprocess(self, text_input: str, text_output: str) -> dict:
        if self.appendToInput:
            return {"text_input":text_input + text_output}
        else:
            return {"text_input":text_output}

    def full_process(self, text_input: dict) -> dict:
        return self.postprocess(*self.LLM_call(self.preprocess(**text_input)))
    
    def __rrshift__(self, leftText: str) -> str:
        if isinstance(leftText, str):
            d = {"text_input": leftText}
        return self.full_process(d)


class _ChainedModule(_AbstractBaseLLMModule):

    def __init__(self, leftModule: _AbstractBaseLLMModule, rightModule: _AbstractBaseLLMModule) -> None:
        super().__init__()
        self.leftModule = leftModule
        self.rightModule = rightModule

    def __rrshift__(self, leftText: Union[str, _AbstractBaseLLMModule] ) -> Union[str, _AbstractBaseLLMModule]:
        left_res = leftText>>self.leftModule
        full_res = left_res>>self.rightModule
        return full_res



class BaseLLMModule(_AbstractBaseLLMModule):
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

    def __rrshift__(self, leftText: Union[str, _AbstractBaseLLMModule] ) -> Union[str, _AbstractBaseLLMModule]:
        if isinstance(leftText, _AbstractBaseLLMModule):
            return _ChainedModule(leftText, self)
        elif isinstance(leftText, str):
            return super().__rrshift__(leftText)
        elif isinstance(leftText, dict):
            return super().__rrshift__(leftText)
        



class TextTemplateModule(BaseLLMModule):

    def __init__(self, template: str, kwarg_priority_input=True, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template = template
        self.class_kwargs = kwargs
        self.kwarg_priority_input = kwarg_priority_input


    def preprocess(self, text_input="", **kwargs) -> str:
        cur = self.class_kwargs.copy()
        if self.kwarg_priority_input:
            cur.update(kwargs)
        else:
            kwargs.update(cur)
            cur = kwargs
        return self.template.format(text_input, **cur)

    def __call__(self, **kwds: Any) -> Any:
        self.class_kwargs.update(kwds)
        return self
        
    @staticmethod
    def from_file(filename: str, **kwargs) -> "TextTemplateModule":
        with open(filename, "r") as f:
            template = f.read()
        return TextTemplateModule(template, **kwargs)



