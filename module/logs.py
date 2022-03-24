import time
from module.getConfig import getConfig

class logs():
    def __init__(self) -> None:
        self.logPath = getConfig(type='logs')
        self.logID = str(int(time.time()))
    
    def info(self, message: str) -> None:
        logID = self.logID
        logPath = self.logPath
        
        print('Info: '+message)
        with open(logPath+logID+'.log', 'a', encoding='UTF-8') as f:
            f.write('Info: '+message+'\n')
        f.close()
    
    def error(self, message: str) -> None:
        logID = self.logID
        logPath = self.logPath
        
        print('Error: '+message)
        with open(logPath+logID+'.log', 'a', encoding='UTF-8') as f:
            f.write('Error: '+message+'\n')
        f.close()
