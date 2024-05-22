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
            prompt = [{"role": "user", "content": f"以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：{question}\n  答案："}]
        if shot == 'cot_zeroshot':
            prompt = [{"role": "user", "content": f"以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：{question}\n  答案：让我们一步一步思考，"}]
        if shot == 'fewshot':
            prompt = [{"role": "user", "content":  "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：在农场，迈克摘了7个苹果，南希摘了3个，基思摘了6个苹果和4个梨。一共摘了多少个苹果？\n  答案："},
                       {"role": "assistant", "content": "16个苹果"},
                       {"role": "user", "content": "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：塔米一小时开了55英里。照这样下去，她36小时能开多远？\n  答案："},
                       {"role": "assistant", "content": "1980英里"},
                       {"role": "user", "content": "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：一个琐事小组总共有15名成员，但在一场比赛中有6名成员没有出现。如果每个出现的成员都得了3分，总共得了多少分？\n  答案："},
                       {"role": "assistant", "content": "27分"},
                       {"role": "user", "content":f"以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：{question}\n  答案："}]
        if shot == 'cot_fewshot':
            prompt = [{"role": "user", "content":  "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：在农场，迈克摘了7个苹果，南希摘了3个，基思摘了6个苹果和4个梨。一共摘了多少个苹果？\n  答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "由于迈克有7个苹果，南希有3个苹果，基思有6个苹果，所以一共有7+3+6=16，答案是一共摘了16个苹果。"},
                       {"role": "user", "content": "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：塔米一小时开了55英里。照这样下去，她36小时能开多远？\n  答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "塔米一小时能开55英里，开了36小时的总距离，一共有55*36=1980英里，答案是能开1980英里。"},
                       {"role": "user", "content": "以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：一个琐事小组总共有15名成员，但在一场比赛中有6名成员没有出现。如果每个出现的成员都得了3分，总共得了多少分？\n  答案：让我们一步一步思考，"},
                       {"role": "assistant", "content": "小组一共有15名成员，6名成员没有出现，说明出现了15-6=9名成员。每名出现的成员有3分，所以9名成员一共得了9*(15-9)=27分，答案是得了27分。"},
                       {"role": "user", "content":f"以下是含有单位和数字计算的题目，请根据题目，给出正确的答案。 题目：{question}\n  答案：让我们一步一步思考，"}]

    if language == 'en':
        if shot == 'zeroshot':
            prompt = [{"role": "user", "content": f"The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：{question}\n  Answer："}]
        if shot == 'cot_zeroshot':
            prompt = [{"role": "user", "content": f"The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：{question}\n  Answer：Let's think step by step, "}]
        if shot == 'fewshot':
            prompt = [{"role": "user", "content":  "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：Mike picked 7 apples , Nancy picked 3 apples , and Keith picked 6 apples and 4 pears , at the farm . How many apples were picked in total ?\n  Answer："},
                       {"role": "assistant", "content": "16 apples"},
                       {"role": "user", "content": "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：Tammy drove 55 miles in one hour. At that rate, how far can she drive in 36 hours?\n  Answer："},
                       {"role": "assistant", "content": "1980 miles"},
                       {"role": "user", "content": "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：A trivia team had 15 members total, but during a game 6 members didn't show up. If each member that did show up scored 3 points, how many points were scored total?\n  Answer："},
                       {"role": "assistant", "content": "27 points"},
                       {"role": "user", "content":f"The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：{question}\n  Answer："}]
        if shot == 'cot_fewshot':
            prompt = [{"role": "user", "content":  "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：Mike picked 7 apples , Nancy picked 3 apples , and Keith picked 6 apples and 4 pears , at the farm . How many apples were picked in total ?\n  Answer：Let's think step by step, "},
                       {"role": "assistant", "content": "Due to Mike having 7 apples, Nancy having 3 apples, and Keith having 6 apples, there are a total of 7+3+6=16 apples picked."},
                       {"role": "user", "content": "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：Tammy drove 55 miles in one hour. At that rate, how far can she drive in 36 hours?\n  Answer：Let's think step by step, "},
                       {"role": "assistant", "content": "Tammy can drive 55 miles per hour, with a total distance of 36 hours, totaling 55 * 36=1980 miles. The answer is that it can drive 1980 miles."},
                       {"role": "user", "content": "The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：A trivia team had 15 members total, but during a game 6 members didn't show up. If each member that did show up scored 3 points, how many points were scored total?\n  Answer：Let's think step by step, "},
                       {"role": "assistant", "content": "There are a total of 15 members in the team, and 6 members did not appear, indicating the presence of 9 members from 15-6. Each member who appears has 3 points, so a total of 9 members scored 9 * (15-9)=27 points, and the answer is 27 points."},
                       {"role": "user", "content":f"The following are questions containing unit and numerical calculations. Please provide the correct answers based on the questions.  Question：{question}\n  Answer：Let's think step by step, "}]

    if language == 'suanjing':
        if shot == 'zeroshot':
            prompt = [{"role": "user", "content":f"以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：{question} \n  答案："}]
        if shot == 'cot_zeroshot':
            prompt = [{"role": "user", "content":f"以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：{question} \n  答案：让我们一步一步思考，"}]
        if shot == 'fewshot':
            prompt = [{"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有七个人平分八又三分之一钱。问：每个人各得到多少钱？\n  答案："},
                      {"role": "assistant", "content": "人得一钱、二十一分钱之四。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有一个直角梯形田，其中一面宽三十步，另外一面宽四十二步，高六十四步。问这个田的面积是多少？\n  答案："},
                      {"role": "assistant", "content": "九亩一百四十四步。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有九块黄金和十一块白银，它们的质量相同。如果将其中一块黄金和白银进行交换，那么黄金的重量就会轻十三两。问：每块黄金和每块白银的重量各是多少？\n  答案："},
                      {"role": "assistant", "content": "金重二斤三两一十八铢，银重一斤十三两六铢。"},
                      {"role": "user", "content":f"以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：{question} \n  答案："}]
        if shot == 'cot_fewshot':
            prompt = [{"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有七个人平分八又三分之一钱。问：每个人各得到多少钱？\n  答案：让我们一步一步思考，"},
                      {"role": "assistant", "content": "我们首先要明确'八又三分之一'这个数字的确切意思。在这里，'八又三分之一'意味着 8 加上 1/3，等于25/3。这个问题是关于平均分配的，所以我们需要将总金额除以人数。这里的总金额是25/3，平均每个人可以分到25/3除以7，这个结果用小数表示约等于1.19钱，用分数表示是25/21钱，或表示为一又二十一分之四钱，或表示为一钱二十一分钱之四。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有一个直角梯形田，其中一面宽三十步，另外一面宽四十二步，高六十四步。问这个田的面积是多少？\n  答案：让我们一步一步思考，"},
                      {"role": "assistant", "content": "要计算直角梯形的面积，我们可以使用公式：梯形面积=（上底+下底）* 高 / 2。在这个问题中，梯形的上底和下底是两个不同的边。由于梯形是直角梯形，我们可以直接使用这些边作为上底和下底。根据题目，这两边的长度分别是 30 步和 42 步，高是 64 步。所以，梯形的面积可以计算如下：梯形面积=（30+42）* 64 / 2 = 2304步，由于1亩=240步，所以2304步又等于9亩144步，即九亩一百四十四步。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有九块黄金和十一块白银，它们的质量相同。如果将其中一块黄金和白银进行交换，那么黄金的重量就会轻十三两。问：每块黄金和每块白银的重量各是多少？\n  答案：让我们一步一步思考，"},
                      {"role": "assistant", "content": "这是一个典型的数学问题，我们可以用方程来解决。设每块黄金的重量为X两，每块白银的重量为Y两。根据题意，我们有9块黄金和11块白银，所以黄金部分的重量为9X，白银部分的重量为11Y。首先9块黄金和11块白银的质量相同，所以9X = 11Y。当我们将一块黄金和一块白银进行交换后，黄金部分的重量变为9X - X + Y = 8X + Y，白银部分的重量变为11Y - Y + X = 10Y + X。根据题意，新的黄金部分重量比新的白银重量轻十三两，即10Y + X - (8X + Y) = 13。现在我们可以通过9X = 11Y和10Y + X - (8X + Y) = 13这两个方程，来解出每块黄金和每块白银的重量，让我们计算一下。首先，让我们处理第二个方程10Y + X - (8X + Y) = 13。我们可以简化它，然后使用第一个方程来找到解。这个简化过程如下：先化简为10Y + X - 8X - Y = 13，再化简为9Y - 7X =13。接下来，我们可以利用第一个方程9X = 11Y来解9Y - 7X =13。求解之后，我们可以得到以下结果：X（黄金的重量）是143/4两，即35.75两。Y（白银的重量）是117/4两，即29.25两。又因为1斤=16两，一两=24铢，所以金重35.75两等于二斤三两一十八铢，银重29.25两等于一斤十三两六铢。"},
                      {"role": "user", "content":f"以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：{question} \n  答案：让我们一步一步思考，"}]
        if shot == 'numcot':
            prompt = [{"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有七个人平分八又三分之一钱。问：每个人各得到多少钱？\n  答案：让我们一步一步思考，这里我们要先了解一些知识，1秒=10忽；1毫=10秒；1厘=10毫；1分=10厘；一寸=10分；1尺=10存；1丈=10尺；1引=10丈；1端=50尺；1疋=40尺；1匹=1疋；1步=6尺；1顷=100亩；1亩=240步；1亩=240积步；1里=300步；1里=375亩；1两=24铢；1斤=16两；1钧=30斤；1石=4钧；1圭=6粟；1抄=10圭；1撮=10抄；1勺=10撮；1合=10勺；1升=10合；1斗=10升；1斛=10斗；1秉=16斛；50栗米=30粝米；50栗米=27粺米；50栗米=24凿米；50栗米=21御米；50栗米=13.5小䵂；50栗米=54大䵂；50栗米=75粝饭；50栗米=54粺饭；50栗米=48凿饭；50栗米=42御饭；50栗米=45菽；50栗米=45答；50栗米=45麻；50栗米=45麦；50栗米=60稻；50栗米=63豉；50栗米=90豉；50栗米=115熟菽；50栗米=175蘖；1岁=354日；4穿地=5壤；4穿地=5坚；4穿地=5墟。"},
                      {"role": "assistant", "content": "我们首先要明确'八又三分之一'这个数字的确切意思。在这里，'八又三分之一'意味着 8 加上 1/3，等于25/3。这个问题是关于平均分配的，所以我们需要将总金额除以人数。这里的总金额是25/3，平均每个人可以分到25/3除以7，这个结果用小数表示约等于1.19钱，，用分数表示是25/21钱，或表示为一又二十一分之四钱，或表示为一钱二十一分钱之四。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有一个直角梯形田，其中一面宽三十步，另外一面宽四十二步，高六十四步。问这个田的面积是多少？\n  答案：让我们一步一步思考，这里我们要先了解一些知识，1秒=10忽；1毫=10秒；1厘=10毫；1分=10厘；一寸=10分；1尺=10存；1丈=10尺；1引=10丈；1端=50尺；1疋=40尺；1匹=1疋；1步=6尺；1顷=100亩；1亩=240步；1亩=240积步；1里=300步；1里=375亩；1两=24铢；1斤=16两；1钧=30斤；1石=4钧；1圭=6粟；1抄=10圭；1撮=10抄；1勺=10撮；1合=10勺；1升=10合；1斗=10升；1斛=10斗；1秉=16斛；50栗米=30粝米；50栗米=27粺米；50栗米=24凿米；50栗米=21御米；50栗米=13.5小䵂；50栗米=54大䵂；50栗米=75粝饭；50栗米=54粺饭；50栗米=48凿饭；50栗米=42御饭；50栗米=45菽；50栗米=45答；50栗米=45麻；50栗米=45麦；50栗米=60稻；50栗米=63豉；50栗米=90豉；50栗米=115熟菽；50栗米=175蘖；1岁=354日；4穿地=5壤；4穿地=5坚；4穿地=5墟。"},
                      {"role": "assistant", "content": "要计算直角梯形的面积，我们可以使用公式：梯形面积=（上底+下底）* 高 / 2。在这个问题中，梯形的上底和下底是两个不同的边。由于梯形是直角梯形，我们可以直接使用这些边作为上底和下底。根据题目，这两边的长度分别是 30 步和 42 步，高是 64 步。所以，梯形的面积可以计算如下：梯形面积=（30+42）* 64 / 2 = 2304步，由于1亩=240步，所以2304步又等于9亩144步，即九亩一百四十四步。"},
                      {"role": "user", "content": "以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：现在有九块黄金和十一块白银，它们的质量相同。如果将其中一块黄金和白银进行交换，那么黄金的重量就会轻十三两。问：每块黄金和每块白银的重量各是多少？\n  答案：让我们一步一步思考，这里我们要先了解一些知识，1秒=10忽；1毫=10秒；1厘=10毫；1分=10厘；一寸=10分；1尺=10存；1丈=10尺；1引=10丈；1端=50尺；1疋=40尺；1匹=1疋；1步=6尺；1顷=100亩；1亩=240步；1亩=240积步；1里=300步；1里=375亩；1两=24铢；1斤=16两；1钧=30斤；1石=4钧；1圭=6粟；1抄=10圭；1撮=10抄；1勺=10撮；1合=10勺；1升=10合；1斗=10升；1斛=10斗；1秉=16斛；50栗米=30粝米；50栗米=27粺米；50栗米=24凿米；50栗米=21御米；50栗米=13.5小䵂；50栗米=54大䵂；50栗米=75粝饭；50栗米=54粺饭；50栗米=48凿饭；50栗米=42御饭；50栗米=45菽；50栗米=45答；50栗米=45麻；50栗米=45麦；50栗米=60稻；50栗米=63豉；50栗米=90豉；50栗米=115熟菽；50栗米=175蘖；1岁=354日；4穿地=5壤；4穿地=5坚；4穿地=5墟。"},
                      {"role": "assistant", "content": "这是一个典型的数学问题，我们可以用方程来解决。设每块黄金的重量为X两，每块白银的重量为Y两。根据题意，我们有9块黄金和11块白银，所以黄金部分的重量为9X，白银部分的重量为11Y。首先9块黄金和11块白银的质量相同，所以9X = 11Y。当我们将一块黄金和一块白银进行交换后，黄金部分的重量变为9X - X + Y = 8X + Y，白银部分的重量变为11Y - Y + X = 10Y + X。根据题意，新的黄金部分重量比新的白银重量轻十三两，即10Y + X - (8X + Y) = 13。现在我们可以通过9X = 11Y和10Y + X - (8X + Y) = 13这两个方程，来解出每块黄金和每块白银的重量，让我们计算一下。首先，让我们处理第二个方程10Y + X - (8X + Y) = 13。我们可以简化它，然后使用第一个方程来找到解。这个简化过程如下：先化简为10Y + X - 8X - Y = 13，再化简为9Y - 7X =13。接下来，我们可以利用第一个方程9X = 11Y来解9Y - 7X =13。求解之后，我们可以得到以下结果：X（黄金的重量）是143/4两，即35.75两。Y（白银的重量）是117/4两，即29.25两。又因为1斤=16两，一两=24铢，所以金重35.75两等于二斤三两一十八铢，银重29.25两等于一斤十三两六铢。"},
                      {"role": "user", "content":f"以下是含有单位和关于汉字数字计算的题目，请根据题目，给出正确的答案。 题目：{question} \n  答案：让我们一步一步思考，这里我们要先了解一些知识，1秒=10忽；1毫=10秒；1厘=10毫；1分=10厘；一寸=10分；1尺=10存；1丈=10尺；1引=10丈；1端=50尺；1疋=40尺；1匹=1疋；1步=6尺；1顷=100亩；1亩=240步；1亩=240积步；1里=300步；1里=375亩；1两=24铢；1斤=16两；1钧=30斤；1石=4钧；1圭=6粟；1抄=10圭；1撮=10抄；1勺=10撮；1合=10勺；1升=10合；1斗=10升；1斛=10斗；1秉=16斛；50栗米=30粝米；50栗米=27粺米；50栗米=24凿米；50栗米=21御米；50栗米=13.5小䵂；50栗米=54大䵂；50栗米=75粝饭；50栗米=54粺饭；50栗米=48凿饭；50栗米=42御饭；50栗米=45菽；50栗米=45答；50栗米=45麻；50栗米=45麦；50栗米=60稻；50栗米=63豉；50栗米=90豉；50栗米=115熟菽；50栗米=175蘖；1岁=354日；4穿地=5壤；4穿地=5坚；4穿地=5墟。"}]
    return prompt