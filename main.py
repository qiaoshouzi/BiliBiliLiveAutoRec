import os, sys, json, time, shutil, requests
from module.logs import logs
from module.getConfig import getConfig
from module.SendMessage import LiveSendMessage, ServerChanSendMessage, DingDingSendMessage

MID = 000000 #UID

configData = getConfig(mid=MID)
name = configData['liveList']['name']
ffmpeg = configData['ffmpeg']['name']
ffmpegOutPath = configData['ffmpeg']['outPath']
ffmpegVideoPath = configData['ffmpeg']['videoPath']

api = [
    'https://api.bilibili.com/x/space/acc/info', #获取直播间基本信息
    'http://api.live.bilibili.com/room/v1/Room/playUrl' #获取直播间源URL
]
parametersTem = [
    {
        'mid': '' #UID
    },
    {
        'cid': '', #直播间ID
        'platform': 'web',
        'qn': 4,
        #'quality': '10000'
    }
]

log = logs()

def getAPI(api: str, parameters: str, message: str) -> json:
    '''
    发送请求
    
    api: 请求地址
    parameters: 请求参数
    message: 日志信息
    '''
    errorCounter = 0
    while True:
        try:
            json=requests.get(api, parameters).json()
        except:
            ServerChanSendMessage(name, log, 'API获取失败', 'API简介: '+message) #通过message获取API简介并通知API访问异常
            log.error('API获取失败|简介='+message)
            json = {'code': 666}
        code=json['code']
        if errorCounter > 10:
            ServerChanSendMessage(name, log, 'API请求错误次数过多', 'message='+message+'|程序自毁')
            log.error('API请求错误次数过多|message='+message+'|程序自毁')
            sys.exit(1)
        elif code == -412:
            errorCounter = errorCounter+1
            ServerChanSendMessage(name, log, 'IP被拦截', 'IP被拦截，已自动等待5min')
            log.error('IP被拦截，已自动等待5min')
            time.sleep(600)
        elif code == 666:
            errorCounter = errorCounter+1
            ServerChanSendMessage(name, log, 'API获取失败，尝试修复', 'API简介: '+message+' | STOP 30s')
            log.error('API获取失败，尝试修复|简介='+message)
            time.sleep(30)
        else:
            data=json['data']
            return data
def getLiveInfo(message: str) -> json:
    '''
    获取直播间状态
    
    message: 日志信息
    '''
    parameters = parametersTem[0]
    parameters['mid'] = int(configData['liveList']['mid'])
    reqData = getAPI(api[0], parameters, message)
    
    return reqData
def getLiveUrl(message: str) -> json:
    '''
    获取直播间源URL
    
    message: 日志信息
    '''
    parameters = parametersTem[1]
    parameters['cid'] = int(configData['liveList']['rid'])
        
    return getAPI(api[1], parameters, message)

def getNowTime() -> str:
    '''
    获取当前时间
    '''
    return str(int(time.time()))

def main() -> None:
    log.info('开始运行')
    while True:
        status = 0
        try:
            status = (getLiveInfo('直播间状态'))['live_room']['liveStatus'] #获取直播间状态
        except:
            pass
        if status == 1:
            log.info('检测到开播')
            reqData = getLiveInfo('直播间基本信息') #获取直播间基本信息
            liveTitle = reqData['live_room']['title'] #直播间标题
            liveCoverURL = reqData['live_room']['cover'] #直播间封面
            liveUrl = (getLiveUrl('直播间源URL'))['durl'][0]['url'] #直播源
            log.info('获取到直播源URL: '+liveUrl)
            time.sleep(0)
            Time = getNowTime()
            #日志log: ffmpeg启动
            lsm = LiveSendMessage(name, log)
            lsm.liveOpen(Time, liveTitle, liveCoverURL)
            log.info('['+Time+']ffmpeg开启')
            os.system(ffmpeg+' -headers "referer: https://bilibili.com/" -i "'+liveUrl+'" -c copy '+ffmpegOutPath+Time+'.mp4') #启动ffmpeg
            shutil.copy(ffmpegOutPath+Time+'.mp4', ffmpegVideoPath+Time+'.mp4') #复制到video文件夹
            os.remove(ffmpegOutPath+Time+'.mp4') #删除ffmpeg生成的文件
            #日志log: ffmpeg关闭
            lsm.liveDown(getNowTime())
        time.sleep(30)

if __name__ == '__main__':
    os.makedirs('tmp', exist_ok=True)
    os.makedirs('video', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    main()
