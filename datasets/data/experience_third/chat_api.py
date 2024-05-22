import openai
import requests
import json
import zhipuai

#调用chatgpt3.5的接口
def chat_gpt35(prompt, format):
    if format == True:
        mess = prompt
    else:
        mess = [{"role": "user", "content": prompt}]
    try:
        openai.api_key = "XXXXXXXXX"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = mess)
        return response.choices[0].message['content'].replace("\n", "").replace("\n", "")
    except Exception as e:
        print("响应出错")
        return 'error-chat_gpt35的api出现问题，需要重跑'


#调用文心一言的接口
def chat_wenxinyy(prompt, format):
    try:
        def get_access_token():
            token_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=XXXXXXXXX&client_secret=XXXXXXXXX" # 院里的
            token_payload = json.dumps("")
            token_headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'}
            token = requests.request("POST", token_url, headers=token_headers, data=token_payload)
            return token.json().get("access_token")

        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()  # ERNIE-Bot 4.0
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token() # ERNIE-Bot-turbo
        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()  # ERNIE-Bot
        if format == True:
            mess = {"messages": prompt}
        else:
            mess = {"messages": [ {"role": "user", "content": prompt}]}
        payload = json.dumps(mess)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text).get("result").replace("\n", "")
    except Exception as e:
        return 'error-wenxinyy的api出现问题，需要重跑'


# 调用langchain-chatchat的chatglm2_6b接口
def chat_chatglm26b(prompt, format):
    try:
        if format == True:
            quesion = prompt.pop()
            history = prompt
            query = quesion.get('content')
        else:
            history = []
            query = prompt
        url = 'http://127.0.0.1:12001/chat/chat'
        response = requests.post(url, headers={"Authorization": "", "Content-Type": "application/json"},
                                     json={"query": query,
                                         "history": history,
                                         "model_name": "chatglm2-6b",
                                         "temperature": 0.7,
                                         "prompt_name": "default"})
        if response.status_code == 200:
            return json.loads(response.text)["text"].replace("\n", "")
    except Exception as e:
        result = {'text': 'error-chatglm26b的api出现问题，需要重跑'}
        return json.dumps(result)

#调用智谱的接口
def chat_zhipu(prompt, format):
    try:
        zhipuai.api_key = "XXXXXXXXX"
        if format == True:
            mess = prompt
        else:
            mess = [{"role": "user", "content": prompt}]
        response = zhipuai.model_api.invoke(
            model="chatglm_turbo",
            prompt = mess,
            top_p=0.7,
            temperature=0.9,
        )
        result = response["data"]["choices"][0]["content"].replace("\n", "")
    except Exception as e:
        if "敏感内容" in response["msg"]:
            return response["msg"]
        result = "zhipu的api出现问题，需要重跑"
    return result.replace("\"", "").strip()