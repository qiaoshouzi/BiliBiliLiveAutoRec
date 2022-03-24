import sys, hmac, json, time, base64, hashlib, requests, urllib.parse
from module.logs import logs
from module.getConfig import getConfig

configData = getConfig(type='SendMessage')
ServerChanSendKey = configData['ServerChanSendKey'] # ServerChan的SendKey
DingDingAccessToken = configData['DingDing']['accessToken'] #备用推送 Token
DingDingSecret = configData['DingDing']['secret'] #备用推送 签名秘钥

class LiveSendMessage:
    def __init__(self, name: str, log: logs) -> None:
        '''
        name: name
        log: logs
        '''
        self.name = name
        self.log = log
    
    def liveOpen(self, time: str, liveTitle: str, liveCoverURL: str) -> None:
        '''
        直播开播推送
        
        time: 开播时间戳
        liveTitle: 直播标题
        liveCoverURL: 直播封面URL
        '''
        name = self.name
        log = self.log
        
        title = '['+time+']'
        desp = 'ffmpeg开启|开始时间戳: '+time+'|title: '+liveTitle+'|coverURL: '+liveCoverURL
        reqData = ServerChanSendMessage(name, log, title, desp)
        self.openTime = time
        self.url = 'https://sct.ftqq.com/readpush?id='+(reqData['data']['pushid'])+'&readkey='+(reqData['data']['readkey'])
    
    def liveDown(self, time: str) -> None:
        '''
        直播结束推送
        
        time: 结束时间戳
        '''
        name = self.name
        log = self.log
        openTime = self.openTime
        url = self.url
        
        title = '['+time+']'
        desp = 'ffmpeg关闭|开始时间戳: '+openTime+'|当前时间戳: '+time+'|[开始]('+url+')'
        ServerChanSendMessage(name, log, title, desp)

def ServerChanSendMessage(name: str, log: logs, title: str, desp: str) -> json or None:
    '''
    ServerChan推送
    
    name: name
    log: logs
    title: 标题
    desp: 描述
    '''
    title=name+' '+title
    api='https://sctapi.ftqq.com/'+ServerChanSendKey+'.send'
    json={
        'title': title,
        'desp': desp
    }
    try:
        data=requests.post(api, json).json()
    except:
        log.error('[方糖推送]推送失败|title='+title+'|desp='+desp)
        DingDingSendMessage(log, '[备用推送] [方糖推送]推送失败\ntitle='+title+'\ndesp='+desp+'\n脚本已关闭\n')
        log.error('使用sys.exit(1)关闭程序')
        sys.exit(1)
    code=data['code']
    if code == 0:
        log.info('[方糖推送]方糖推送成功|pushid='+(data['data']['pushid'])+'|readkey='+(data['data']['readkey']))
        return data
    else:
        message=data['message']
        log.error('[方糖推送]返回值异常|message='+message+'|title='+title+'|desp='+desp)
        DingDingSendMessage(log, '[备用推送] [方糖推送]返回值异常\nmessage='+message+'\ntitle='+title+'\ndesp='+desp+'\n脚本已关闭\n')
        log.error('使用sys.exit(1)关闭程序')
        sys.exit(1)

def DingDingSendMessage(log: logs, message: str) -> None:
    '''
    钉钉推送
    
    message: 消息
    '''
    log.info('备用推送已启用|message='+message)
    timestamp=str(round(time.time()*1000)) #获取timestamp

    # 获取签名
    secret_enc = DingDingSecret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, DingDingSecret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    api_parameters='https://oapi.dingtalk.com/robot/send?access_token='+DingDingAccessToken+'&timestamp='+timestamp+'&sign='+sign
    headers={'Content-Type': 'application/json'}
    data={
        'at': {
            'isAtAll': True
        },
        'text': {
            'content': message
        },
        'msgtype': 'text'
    }
    try:
        res=requests.post(api_parameters, data=json.dumps(data), headers=headers).json()
    except:
        log.error('备用推送失败')
    errcode=res['errcode']
    errmsg=str(res['errmsg'])
    if errcode==0:
        log.info('备用推送成功')
    elif errcode==310000:
        log.error('备用推送报错|errcode='+str(errcode)+'|errmsg='+errmsg)
    else:
        log.error('备用推送出现未知报错|errcode='+str(errcode)+'|errmsg='+errmsg)
