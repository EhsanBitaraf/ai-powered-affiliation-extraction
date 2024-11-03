import json
import os
from langflow.load import run_flow_from_json
from src.config import FLOW_TEMPLATE_PATH,AI_API_KEY


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
def parse_affiliation(affiliation:str): 
    # TWEAKS = {
    # "ChatInput-Jlerj": {},
    # "Prompt-th0CI": {},
    # "ChatOutput-ChR8F": {},
    # "TextOutput-IYI6h": {},
    # "OpenAIModel-zBO6c": {}
    # }
    TWEAKS = {
    "ChatInput-eLRa5": {},
    "Prompt-CATz2": {},
    "ChatOutput-bSg1i": {},
    "TextOutput-ReHip": {},
    "OpenAIModel-Fv9o0": {
        "api_key": AI_API_KEY,
        "model_name": "gpt-3.5-turbo-0125",
    }
    }
    flow_path = os.path.join(FLOW_TEMPLATE_PATH ,"AffiliationMiningWithOpenAI.json")
    result = run_flow_from_json(flow=flow_path,
                                input_value=affiliation,
                                fallback_to_env_vars=True, # False by default
                                log_level="critical",
                                tweaks=TWEAKS)

    # print(affiliation)
    # print(result[0].outputs[0].results['message'].text)

    json_str = result[0].outputs[0].results['message'].text
    try:
        r = json.loads(json_str)
        r['Status'] = "Ok"
    except Exception as e:
        r['Status'] = "Error"
        r['Input'] = affiliation
        if isinstance(e,json.JSONDecodeError):
            r['ErrorMsg'] = e.msg
            r["colno"] =  e.colno
        else:
            r['ErrorType'] = str(type(e))
    
    return r


    with open('AffiliationMiningWithOpenAI.json', 'w') as f:
        json.dump(result, f, indent=4, cls=CustomEncoder)