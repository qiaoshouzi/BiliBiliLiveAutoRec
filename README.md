# BiliBiliLiveAutoRec

自动录播脚本

```yaml
logsPath: ./logs/ #日志路径

ffmpeg:
  name: ffmpeg #启动ffmpeg的命令
  outPath: ./tmp/ #临时输出路径
  videoPath: ./video/ #视频保存路径

SendMessage:
  ServerChanSendKey: #ServerChan密钥
  DingDing:
    accessToken: #钉钉accessToken
    secret: #钉钉加签密钥

liveList:
  000000: #UID
    name: XXXXXX #名称
    mid: 000000 #UID
    rid: 111111 #直播间号
```
