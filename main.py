# 导入requests包
import requests
import time
import json

# 要发送的微信号，上面关注公众号得到的， 改成自己的
# touser="oqoIt60GMJfkhF3vKdeOwimlnXLg"
tousers = ["oqoIt60GMJfkhF3vKdeOwimlnXLg", "oqoIt6-lqUAqN1SZveLc1wcRDwo0"]
# 消息模板ID， 改成自己的
template_id = "N7mLNlaR453AVH-F_OhyLgfSoCHTPCAKRYivPE6RHI4"
# 微信开发者的 appID， 改成自己的
wx_appid = "wxabd37e229bf640a5"
# 微信开发者的 appsecret， 改成自己的
wx_secret = "54fa987c1d47727bb06ab16a629ed37b"
# 和风天气项目的key， 改成自己的
we_key = "a6ad3c8fddc1459f9c5e36bfc548d429"

# 和风天气的地市代码，从这里查 https://github.com/qwd/LocationList/blob/master/POI-Air-Monitoring-Station-List-latest.csv，
# 或者调用API查询， 文档参考：https://dev.qweather.com/docs/api/geoapi/
# 这里填写当前城市
city_name = "九江"

# 获取token的URL，不用改
wx_token_url = "https://api.weixin.qq.com/cgi-bin/token"
# 获取天气URL， 不用改
we_url = "https://devapi.qweather.com/v7/weather/3d"
# 查询城市URL， 不用改
city_lookup_url = "https://geoapi.qweather.com/v2/city/lookup"
# 微信消息URL， 不用改
msg_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="

# 恋爱天数
love_date = "2023-12-20"
# 小笨蛋的生日
birthday = "2024-3-28"
# 我的生日
my_birthday = "2024-6-1"
# 距离春节的天数
diff_date1 = "2024-2-10"


def get_city_id(city_name):
    # 查询参数，你可能需要根据实际情况修改
    query_params = {
        "location": city_name,
        "key": we_key
    }

    # 发起查询请求
    response = requests.get(url=city_lookup_url, params=query_params)

    # 解析返回的数据
    data = response.json()

    if data["code"] == "200" and data["location"]:
        # 获取第一个城市的ID
        city_id = data["location"][0]["id"]
        return city_id
    else:
        # 处理错误情况，这里简单返回 None
        return None


def send_msg():
    # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
    my_params = {"grant_type": "client_credential", "appid": wx_appid, "secret": wx_secret}
    ## 请求获取token
    res = requests.get(url=wx_token_url, params=my_params)
    print("微信token:", res.text)  # 返回请求结果

    if res.json()['access_token'] == "":
        return "微信Token失败"
    we_param = {"location": get_city_id(city_name), "key": we_key}
    # 请求获取天气
    we_res = requests.get(url=we_url, params=we_param)
    print("天气返回:", we_res.text)
    if we_res.json()['code'] != '200':
        return "获取天气失败"
    we_data = we_res.json()['daily'][0]
    print("天气返回:", we_data)
    # 发送模板消息
    cur_time = time.time()
    msg_id = str(int(cur_time))

    # 计算当前日期距离未来某个日期还有多少天
    def days_until_future_date(target_date):
        current_date = datetime.now().date()
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        # 计算距离未来某个日期的天数差异
        days_remaining = (target_date - current_date).days
        return days_remaining

    from datetime import datetime

    # 计算已经恋爱的天数
    def days_since_start(start_date):
        # 获取当前日期
        current_date = datetime.now().date()
        # 将开始恋爱日期转换为 datetime 对象
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        # 计算距离现在的天数
        days_since_start = (current_date - start_date).days
        return days_since_start

    # 爬取爱词霸每日鸡汤
    def get_iciba_everyday_chicken_soup():
        url = "http://open.iciba.com/dsapi/"  # 词霸免费开放的jsonAPI接口
        r = requests.get(url)
        all = json.loads(r.text)  # 获取到json格式的内容，内容很多
        # print(all) # json内容，通过这行代码来确定每日一句的键名
        # Englis = all['content']  # 提取json中的英文鸡汤
        Chinese = all['note']  # 提取json中的中文鸡汤
        # everyday_soup = Englis + '\n' + Chinese  # 合并需要的字符串内容
        return Chinese  # 返回结果

    # 组装微信模版消息的数据
    send_json = {
        # "touser":touser,
        "touser": tousers,
        "template_id": template_id,
        "url": "https://www.qweather.com/",
        "client_msg_id": msg_id,
        "data": {
            # 可爱的xxx
            "name": {
                "value": "傻不拉几的鱼",
                "color": "#173177"
            },
            # 今天是
            "date": {
                "value": we_data['fxDate'],
                "color": "#173177"
            },
            # 地区
            "city": {
                "value": city_name,
                "color": "#173177"
            },
            # 今日天气
            "weather": {
                "value": we_data['textDay'],
                "color": "#173177"
            },
            # 今日最低温度
            "min_temperature": {
                "value": we_data['tempMin'],
                "color": "#173177"
            },
            # 今日最高温度
            "max_temperature": {
                "value": we_data['tempMax'],
                "color": "#173177"
            },
            # 我们已经恋爱
            "love_date": {
                "value": days_since_start(love_date),
                "color": "#173177"
            },
            # 距离你这个小笨蛋的生日还有
            "birthday": {
                "value": days_until_future_date(birthday),
                "color": "#173177"
            },
            # 距离我的生日还有
            "my_birthday": {
                "value": days_until_future_date(my_birthday),
                "color": "#173177"
            },
            # 距离春节还有
            "diff_date1": {
                "value": days_until_future_date(diff_date1),
                "color": "#173177"
            },
            # 日出时间
            "sunrise": {
                "value": we_data['sunrise'],
                "color": "#173177"
            },
            # 日落时间
            "sunset": {
                "value": we_data['sunset'],
                "color": "#173177"
            },
            # 白天风向
            "windDirDay": {
                "value": we_data['windDirDay'],
                "color": "#173177"
            },
            # 夜间风向
            "windDirNight": {
                "value": we_data['windDirNight'],
                "color": "#173177"
            },
            # 风力等级
            "windScaleDay": {
                "value": we_data['windScaleDay'],
                "color": "#173177"
            },
            # 每日一句
            "note": {
                "value": get_iciba_everyday_chicken_soup(),
                "color": "#173177"
            }
        }
    }

    # 发送微信模版消息
    # 单个消息接收者
    # msg_res = requests.post(url=msg_url+res.json()['access_token'],data=json.JSONEncoder().encode(send_json))
    # print("消息返回:",msg_res.text)
    # if msg_res.json()['errcode'] == 0:
    #     return "发送成功"
    # return "发送失败"

    # 多个消息接收者
    for user in tousers:
        send_json["touser"] = user
        msg_res = requests.post(url=msg_url + res.json()['access_token'], data=json.JSONEncoder().encode(send_json))
        print(f"消息返回给 {user}:", msg_res.text)
        if msg_res.json()['errcode'] != 0:
            return f"发送失败给 {user}"

    return "发送成功"


print(send_msg())
