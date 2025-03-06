# PyOfficeRobot.chat.chat_by_deepseek中修改chat_by_deepseek函数如下：
# 添加requests库

import requests

def chat_by_deepseek(who, api_key, url):
    wx.GetSessionList()  # 获取会话列表
    wx.ChatWith(who)  # 打开`who`聊天窗口
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    temp_msg = None
    while True:
        try:
            friend_name, receive_msg = wx.GetAllMessage[-1][0], wx.GetAllMessage[-1][1]  # 获取朋友的名字、发送的信息
            if (friend_name == who) & (receive_msg != temp_msg):
                """
                条件：
                朋友名字正确:(friend_name == who)
                不是上次的对话:(receive_msg != temp_msg)
                对方内容在自己的预设里:(receive_msg in kv.keys())
                """
                print(f'【{who}】发送：【{receive_msg}】')

                data = {
                    "model": "deepseek-chat",  # 指定使用 R1 模型（deepseek-reasoner）或者 V3 模型（deepseek-chat）
                    "messages": [
                        {"role": "system", "content": "你是一个温柔体贴有点黏人但不会过多询问别人需求的男朋友，像真人一样聊天"},
                        {"role": "user", "content": receive_msg}
                    ],
                    "stream": False  # 关闭流式传输
                }

                response = requests.post(url, headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    print(result['choices'][0]['message']['content'])
                else:
                    print("请求失败，错误码：", response.status_code)

                # reply_msg = poai.chat.deepseek(api_key, content=receive_msg)
                wx.SendMsg(result['choices'][0]['message']['content'], who)  # 向`who`发送消息
                temp_msg = result['choices'][0]['message']['content']
        except:
            pass
