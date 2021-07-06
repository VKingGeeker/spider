import os
import time
import urllib.request
from lxml import etree

selector = etree.parse('http://open.weixin.qq.com/connect/qrconnect?appid=wx5a3bbeac0d87c75a&scope=snsapi_login&redirect_uri=https%3A%2F%2Fxinyue.qq.com%2Fcomm-htdocs%2Fmilo_mobile%2Fwxlogin.html%3Fappid%3Dwx5a3bbeac0d87c75a%26sServiceType%3Dxinyue%26originalUrl%3Dhttps%253A%252F%252Fxinyue.qq.com%252Fbeta%252F%2523%252FgameWelfare&state=1&login_type=jssdk&self_redirect=true&styletype=&sizetype=&bgcolor=&rst=&style=black', etree.HTMLParser())
html = selector.xpath('/html/body/div[1]/div/div/div[2]/div[1]/img')
print(html[0].get('src'))

# open.weixin.qq.com/connect/qrcode/091nS7Hf27kd000R