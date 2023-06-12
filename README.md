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
`sudo crontab -e` 添加定时任务
```bash
HOME=/home/shaojiemike
DIR=/home/shaojiemike/test/echart        
@reboot cd $DIR && source myPy/bin/activate && python3 src/main.py > ~/test/echart.log && cp my_list.json /var/www/html &&echo "reboot" >> ~/test/echarttime.log   
* 4 * * * cd $DIR && source myPy/bin/activate && python3 src/main.py > ~/test/echart.log && cp my_list.json /var/www/html && date >> ~/test/echarttime.log  
```
## Todo

 - [ ] Add website visitor count statistics and display data update time
 - [x] Add competition prediction scores by scraping data from the website https://lccn.lbao.site/.

