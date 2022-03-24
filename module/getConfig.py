import yaml, json

def getConfig(type: str=None, mid: int=None) -> json or str:
    '''
    获取Config
    
    type: 获取类型
    mid: 直播间号
    '''
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
    f.close()
    if type == None:
        config = {
            'ffmpeg': {
                'name': config['ffmpeg']['name'],
                'outPath': config['ffmpeg']['outPath'],
                'videoPath': config['ffmpeg']['videoPath']
            },
            'liveList': {
                'name': '['+config['liveList'][mid]['name']+']',
                'mid': str(config['liveList'][mid]['mid']),
                'rid': str(config['liveList'][mid]['rid'])
            }
        }
    elif type == 'SendMessage':
        config = {
            'ServerChanSendKey': config['SendMessage']['ServerChanSendKey'],
            'DingDing': {
                'accessToken': config['SendMessage']['DingDing']['accessToken'],
                'secret': config['SendMessage']['DingDing']['secret']
            }
        }
    elif type == 'logs':
        config = config['logsPath']
    return config
