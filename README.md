# leetcode-ranking-visualization-echart

## Install


```bash
Target=/var/www/html
cp index.html $Target/index.html
cp my_list.json $Target/my_list.json
```

```bash
sudo mount -t none -o bind,ro .  /var/www/html
# 取消
mount --move .  /var/www/html
```

## crontab
`crontab -e` 添加定时任务
```bash
HOME=/home/shaojiemike
DIR=/home/shaojiemike/test/echart        
@reboot cd $DIR && source myPy/bin/activate && python3 src/main.py > ~/test/echart.log && echo "reboot" >> ~/test/echarttime.log   
* 4 * * * cd $DIR && source myPy/bin/activate && python3 src/main.py > ~/test/echart.log && date >> ~/test/echarttime.log  
```
## Todo

 - [ ] get LC data