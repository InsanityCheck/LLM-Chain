from typing import Union, Any
from .LLMCaller import call_LLM



class _AbstractBaseLLMModule():

    def __init__(self, appendToInput=False, **kwargs) -> None:
        self.appendToInput = appendToInput

        
    def preprocess(self, text_input: str) -> str:
        return text_input

    def LLM_call(self, text_input: str) -> str:
        text_output = call_LLM(text_input)
        return text_input, text_output
    
    def postprocess(self, text_input: str, text_output: str) -> str:
        if self.appendToInput:
            return text_input + text_output
        else:
            return text_output
    
    def __rrshift__(self, leftText: str) -> str:
        return self.postprocess(*self.LLM_call(self.preprocess(leftText)))


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
        else:
            return super().__rrshift__(leftText)



class TextTemplateModule(BaseLLMModule):

    def __init__(self, template: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.template = template
        self.kwargs = kwargs

    def preprocess(self, text_input: str) -> str:
        return self.template.format(text_input, **self.kwargs)

    def __call__(self, **kwds: Any) -> Any:
        self.kwargs.update(kwds)
        return self
        
    @staticmethod
    def from_file(filename: str, **kwargs) -> "TextTemplateModule":
        with open(filename, "r") as f:
            template = f.read()
        return TextTemplateModule(template, **kwargs)




if __name__=="__main__":
    
    template = "hallo {name} wie gehts dir? {}"

    T = TextTemplateModule(template, name="Max", appendToInput=True)



    B = BaseLLMModule(appendToInput=True)

    print("abc">>B>>T)
    print("abc">>B>>T(name="Moritz"))