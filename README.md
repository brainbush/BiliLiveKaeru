# BiliLiveKaeru

简简单单在海外点一个阿B的“开始直播”

website： https://live.neeemooo.com

支持使用Cookies登录或扫码登录获取Cookies。

## 使用 FFmpeg 转发直播流

如需要rtmp推流可使用一台有公网IP的国内机器上（比如大带宽NAT VPS）使用 `FFmpeg`

> ffmpeg -listen 1 -i 'rtmp://0.0.0.0:1935/app' -c copy -f flv 'rtmp://js.live-send.acg.tv/live-js/?xxxxxxxxxx'

`1935`为监听端口号，可直接更改成任意端口号，最后的 rtmp 地址是以 `推流地址 + ? + 推流码` 的形式组成，即推流地址和推流码中间加一个英文问号拼接起来。

在OBS中填写 `rtmp://xx.xx.xx.xx:1935/app` 即可开始推流（xx.xx.xx.xx为所使用的机器的IP地址）

如需要持续执行（毕竟B站的推流码一般都不会变），可考虑在screen中使用bash脚本执行：
````
while true
do
    ffmpeg -listen 1 -i 'rtmp://0.0.0.0:1935/app' -c copy -f flv 'rtmp://js.live-send.acg.tv/live-js/?xxxxxxxxxx'
    sleep 1
end
````
