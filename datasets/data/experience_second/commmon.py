from chat_api import *

def call_api(model, quesion, format=False):
    if model == 'chatGPT':
        return chat_gpt35(quesion, format)
    if model == 'chatglm26b':
        return chat_chatglm26b(quesion, format)
    if model == 'wenxinyy':
        return chat_wenxinyy(quesion, format)
    if model == 'zhipu':
        return chat_zhipu(quesion, format)
    return f"model错误，传入的是{model}，出现问题，需要重跑"

def format_unit_measurement(language, shot, question):
    prompt = []
    if language == 'zh':
        if shot == 'zeroshot':
            prompt = [{"role": "user", "content": f"以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：{question} \n答案："}]
        if shot == 'cot_zeroshot':
            prompt = [{"role": "user", "content": f"以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：{question} \n答案：让我们一步一步思考，"}]
        if shot == 'fewshot':
            prompt = [{"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：5900米=？厘米 \n答案："},
                       {"role": "assistant", "content": "590000厘米"},
                       {"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：479分钟 - 630秒钟 = ?秒钟 \n答案："},
                       {"role": "assistant", "content": "28110秒钟"},
                       {"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：7吨54千克 + 68千克 = ?吨?千克 \n答案："},
                       {"role": "assistant", "content": "7吨122千克"},
                       {"role": "user", "content": f"以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：{question} \n答案："}]
        if shot == 'cot_fewshot':
            prompt = [{"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：5900米=？厘米 \n答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "问号右侧的单位是厘米，由于1米=100厘米，所以5900米=5900*100厘米，所以答案是590000厘米。"},
                       {"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：479分钟 - 630秒钟 = ?秒钟 \n答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "问号右侧的单位是秒钟，由于1分钟=60秒钟，因此479分钟=479*60秒钟=28740秒钟。又因为28740秒钟-630秒钟=28110秒钟， 所以答案是28110秒钟。"},
                       {"role": "user", "content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：7吨54千克 + 68千克 = ?吨?千克 \n答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "问号右侧的单位是吨和千克，由于1吨=1000千克，因此7吨54千克=7*1000+54=7054千克。因为7054千克+68千克=7122千克，且1千克=1/1000吨，所以7122千克=7吨122千克。"},
                       {"role": "user", "content": f"以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：{question} \n答案：让我们一步一步思考，"}]
        if shot == 'numcot':
            prompt = [{"role": "user","content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：5900米=？厘米 \n答案：让我们一步一步思考，首先需要了解如下的单位转化常识：1吨=1000千克；1千克=1000克；1克=1000毫克；1周=7天；1天=24小时；1小时=60分钟；1分钟=60秒钟；1秒钟=1000毫秒；1千米=1000米；1米=10分米；1分米=10厘米；1厘米=10毫米；1元=10角；1角=10分钱。"},
                      {"role": "assistant","content": "问号右侧的单位是厘米，由于1米=100厘米，所以5900米=5900*100厘米，所以答案是590000厘米。"},
                      {"role": "user","content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：479分钟 - 630秒钟 = ?秒钟 \n答案：让我们一步一步思考，首先需要了解如下的单位转化常识：1吨=1000千克；1千克=1000克；1克=1000毫克；1周=7天；1天=24小时；1小时=60分钟；1分钟=60秒钟；1秒钟=1000毫秒；1千米=1000米；1米=10分米；1分米=10厘米；1厘米=10毫米；1元=10角；1角=10分钱。"},
                      {"role": "assistant","content": "问号右侧的单位是秒钟，由于1分钟=60秒钟，因此479分钟=479*60秒钟=28740秒钟。又因为28740秒钟-630秒钟=28110秒钟， 所以答案是28110秒钟。"},
                      {"role": "user","content": "以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：7吨54千克 + 68千克 = ?吨?千克 \n答案：让我们一步一步思考，首先需要了解如下的单位转化常识：1吨=1000千克；1千克=1000克；1克=1000毫克；1周=7天；1天=24小时；1小时=60分钟；1分钟=60秒钟；1秒钟=1000毫秒；1千米=1000米；1米=10分米；1分米=10厘米；1厘米=10毫米；1元=10角；1角=10分钱。"},
                      {"role": "assistant","content": "问号右侧的单位是吨和千克，由于1吨=1000千克，因此7吨54千克=7*1000+54=7054千克。因为7054千克+68千克=7122千克，且1千克=1/1000吨，所以7122千克=7吨122千克。"},
                      {"role": "user","content": f"以下是关于单位转化的题目，请根据题目，给出问号处的正确答案。 题目：{question} \n答案：让我们一步一步思考，首先需要了解如下的单位转化常识：1吨=1000千克；1千克=1000克；1克=1000毫克；1周=7天；1天=24小时；1小时=60分钟；1分钟=60秒钟；1秒钟=1000毫秒；1千米=1000米；1米=10分米；1分米=10厘米；1厘米=10毫米；1元=10角；1角=10分钱。"}]
    if language == 'en':
        if shot == 'zeroshot':
            prompt = [{"role": "user", "content": f"The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：{question} \nanswer: "}]
        if shot == 'cot_zeroshot':
            prompt = [{"role": "user", "content": f"The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：{question} \nanswer: Let's think step by step, "}]
        if shot == 'fewshot':
            prompt = [{"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：5900 meters= ?centimeters \nanswer: "},
                      {"role": "assistant", "content": "590000 centimeters"},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：479 minutes - 630 seconds= ?seconds \nanswer: "},
                      {"role": "assistant", "content": "28110 seconds"},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：7 tons 54 kilogram + 68 kilogram= ?tons ?kilograms \nanswer: "},
                      {"role": "assistant", "content": "7 tons 122 kilograms"},
                      {"role": "user", "content": f"The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：{question} \nanswer: "}]
        if shot == 'cot_fewshot':
            prompt = [{"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：5900 meters= ?centimeter \nanswer: Let's think step by step, "},
                      {"role": "assistant", "content": "The unit on the right side of the question mark is centimeters. Since 1 meter=100 centimeters, 5900 meters=5900 * 100 centimeters, so the answer is 590000 centimeters."},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：479 minutes - 630 seconds= ?seconds \nanswer: Let's think step by step, "},
                      {"role": "assistant", "content": "The unit on the right side of the question mark is seconds. Since 1 minute equals 60 seconds, 479 minutes=479 * 60 seconds=28740 seconds. Because 28740 seconds - 630 seconds=28110 seconds, the answer is 28110 seconds."},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：7 tons 54 kilogram + 68 kilogram= ?tons ?kilograms \nanswer: Let's think step by step, "},
                      {"role": "assistant", "content": "The units on the right side of the question mark are tons and kilograms. Since 1 ton=1000 kilograms, 7 tons and 54 kilograms=7 * 1000+54=7054 kilograms. Because 7054 kg+68 kg=7122 kg, and 1 kg=1/1000 tons, 7122 kg=7 tons 122 kg."},
                      {"role": "user", "content": f"The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：{question} \nanswer: Let's think step by step, "}]
        if shot == 'numcot':
            prompt = [{"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：5900 meters= ?centimeter \nanswer: Let's think step by step, Firstly, it is necessary to understand the following common knowledge about unit conversion: 1 ton=1000 kilograms; 1 kilogram=1000 grams; 1 gram=1000 milligrams; 1 week=7 days; 1 day=24 hours; 1 hour=60 minutes; 1 minute=60 seconds; 1 second=1000 milliseconds; 1 kilometer=1000 meters; 1 meter=10 decimeters; 1 decimeter=10 centimeters; 1 centimeter=10 millimeters; 1 yuan=10 jiao; 1 jiao=10 cents."},
                      {"role": "assistant", "content": "The unit on the right side of the question mark is centimeters. Since 1 meter=100 centimeters, 5900 meters=5900 * 100 centimeters, so the answer is 590000 centimeters."},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：479 minutes - 630 seconds= ?seconds \nanswer: Let's think step by step, Firstly, it is necessary to understand the following common knowledge about unit conversion: 1 ton=1000 kilograms; 1 kilogram=1000 grams; 1 gram=1000 milligrams; 1 week=7 days; 1 day=24 hours; 1 hour=60 minutes; 1 minute=60 seconds; 1 second=1000 milliseconds; 1 kilometer=1000 meters; 1 meter=10 decimeters; 1 decimeter=10 centimeters; 1 centimeter=10 millimeters; 1 yuan=10 jiao; 1 jiao=10 cents."},
                      {"role": "assistant", "content": "The unit on the right side of the question mark is seconds. Since 1 minute equals 60 seconds, 479 minutes=479 * 60 seconds=28740 seconds. Because 28740 seconds - 630 seconds=28110 seconds, the answer is 28110 seconds."},
                      {"role": "user", "content": "The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：7 tons 54 kilogram + 68 kilogram= ?tons ?kilograms \nanswer: Let's think step by step, Firstly, it is necessary to understand the following common knowledge about unit conversion: 1 ton=1000 kilograms; 1 kilogram=1000 grams; 1 gram=1000 milligrams; 1 week=7 days; 1 day=24 hours; 1 hour=60 minutes; 1 minute=60 seconds; 1 second=1000 milliseconds; 1 kilometer=1000 meters; 1 meter=10 decimeters; 1 decimeter=10 centimeters; 1 centimeter=10 millimeters; 1 yuan=10 jiao; 1 jiao=10 cents."},
                      {"role": "assistant", "content": "The units on the right side of the question mark are tons and kilograms. Since 1 ton=1000 kilograms, 7 tons and 54 kilograms=7 * 1000+54=7054 kilograms. Because 7054 kg+68 kg=7122 kg, and 1 kg=1/1000 tons, 7122 kg=7 tons 122 kg."},
                      {"role": "user", "content": f"The following is a question about unit conversion. Please provide the correct answer at the question mark according to the question. question：{question} \nanswer: Let's think step by step, Firstly, it is necessary to understand the following common knowledge about unit conversion: 1 ton=1000 kilograms; 1 kilogram=1000 grams; 1 gram=1000 milligrams; 1 week=7 days; 1 day=24 hours; 1 hour=60 minutes; 1 minute=60 seconds; 1 second=1000 milliseconds; 1 kilometer=1000 meters; 1 meter=10 decimeters; 1 decimeter=10 centimeters; 1 centimeter=10 millimeters; 1 yuan=10 jiao; 1 jiao=10 cents."}]


    return prompt