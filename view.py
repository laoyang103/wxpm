# -*- coding: utf-8 -*-
 
import os
import web              #web.py
import time
import datetime
import hashlib          #hash加密算法
from lxml import etree  #xml解析
import requests         #http请求
import json
import codecs           
 
#===================微信公众账号信息================================
#把微信开发页面中的相关信息填进来，字符串格式
my_appid = '******************'
my_secret = '*****************************'
#========匹配URL的正则表达式,url/将被WeixinInterface类处理===========
urls = ( '/','WeixinInterface' )
 
#===================微信权限交互====================================
def _check_hash(data):
  '''
  响应微信发送的GET请求(Hash校验)
  :param data: 接收到的数据
  :return: True or False，是否通过验证
  '''
  signature=data.signature  #加密签名
  timestamp=data.timestamp  #时间戳
  nonce=data.nonce          #随机数
  #自己的token
  token = "ptcs"
  #字典序排序
  list=[token,timestamp,nonce]
  list.sort()
  sha1=hashlib.sha1()
  map(sha1.update,list)
  hashcode=sha1.hexdigest()
  #如果是来自微信的请求，则回复echostr
  if hashcode == signature:
    return True
  return False
 
#=====================微信+HTTP server===============================
class WeixinInterface:
 
  def __init__(self):
    self.app_root = os.path.dirname(__file__)
    self.templates_root = os.path.join(self.app_root, 'templates')
    self.render = web.template.render(self.templates_root)

  def replyText(self, fromUser, toUser, xml):
    msg = xml.find('Content').text
    return self.render.reply_text(fromUser, toUser, int(time.time()), u'你刚才说的是：' + msg)

  def replyEvent(self, fromUser, toUser, xml):
    event = xml.find('Event').text
    if event == "CLICK": 
      msg = '功能开发中，敬请关注。'
      btn = xml.find('EventKey').text
      if btn == "GET_OPENID":
        msg = fromUser
      return self.render.reply_text(fromUser, toUser, int(time.time()), msg)
    elif event == "subscribe": 
      return self.render.reply_text(fromUser, toUser, int(time.time()), u'您好，欢迎关注北京协软科技有限公司，您的ID是：' + fromUser)

  def GET(self):
    data = web.input()
    if _check_hash(data):
      return data.echostr

  def POST(self):
    str_xml = web.data()
    print(str_xml)
    xml = etree.fromstring(str_xml)
    msgType=xml.find("MsgType").text
    fromUser=xml.find("FromUserName").text
    toUser=xml.find("ToUserName").text
    #对不同类型的消息分别处理:
    if msgType == 'text':
      return self.replyText(fromUser, toUser, xml)
    elif msgType == 'event':
      return self.replyEvent(fromUser, toUser, xml)
 
#=====================启动app========================================
 
if __name__ == "__main__":
  app = web.application(urls,globals())
  app.run()

