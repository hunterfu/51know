##!/usr/bin/env python
#-*- coding:utf-8 –*-
#
# 更新官方镜像到开源方案仓库，维护镜像稳定性
#
import urllib2,urllib
from pprint import pprint
import time
import yaml
import sys,os
import getopt
import commands
from operator import itemgetter
try:
    import json
except ImportError:
    import simplejson as json


result_dict = []

logging_image_list = ['origin-logging-auth-proxy','origin-logging-elasticsearch','origin-logging-curator','origin-logging-kibana','origin-logging-fluentd']

metric_image_list = ['origin-metrics-hawkular-metrics','origin-metrics-heapster','origin-metrics-cassandra']
#logging_image_list = ['origin-logging-auth-proxy']

def url_postRequest(url):
    ''' 复杂参数提交 json 结构提交 '''
    #headers = {'X-Auth-Token'   : self.__token_id}
    #headers['Accept'] = 'application/json'
    #print url 
    req = urllib2.Request(url)
    #req.add_header('X-Auth-Token', self.__token_id)
    opener = urllib2.urlopen(req)
    content = json.loads(opener.read())
    return content
    #pprint(content)

def get_image(image,version):
    
    next_page = 'https://registry.hub.docker.com/v2/repositories/openshift/%s/tags/' % (image)
    #print next_page
    get_result(next_page,image,version)
    image_last = result_dict[0]
    # 清空结果
    del result_dict[:]
    return image_last
    #pprint(image_last)

def get_result(next_page,image,version):
    
    if next_page:
       content = url_postRequest(next_page)
       next_page = content['next']
       results_list = content['results']
       for image_dict in results_list:
          #print "%s\t\t%s" % (image_dict['last_updated'], image_dict['name'])
          name = image_dict['name']
          #if name.find("v3.6") == -1: continue
          if name.find(version) == -1: continue
          info_dict = {'image':image,'last_updated':image_dict['last_updated'],'name':image_dict['name']}
          result_dict.append(info_dict)
       get_result(next_page,image,version)

def get_logging_tag(version):
    """ 等到日志系统相关镜像 """ 
    for image in logging_image_list:
        #print "image = %s" % image
        #result_dict = []
        image_version = get_image(image,version)
        docker_tag(image_version,"v3.6.1")

def docker_tag(image_version,dest_version):
    """ 打标签 推送到51knowinfo仓库 """
    
    image = image_version['image']
    name = image_version['name']
    cmd_pull = "docker pull openshift/%s:%s" %(image,name)
    cmd_tag = "docker tag openshift/%s:%s 51knowinfo/%s:%s" %(image,name,image,dest_version)
    cmd_push = "docker push 51knowinfo/%s:%s" %(image,dest_version)
    print cmd_pull
    print cmd_tag
    print cmd_push
    print 

def get_metric_tag(version):
    """ 等到度量系统相关镜像 """
    for image in metric_image_list:
        #print "image = %s" % image
        #result_dict = []
        image_version = get_image(image,version)
        docker_tag(image_version,"v3.6.1")
    

def main():
    """
    主函数
    """
    #get_logging_tag("v3.6")
    get_metric_tag("v3.6")

if __name__ == "__main__":
    main()

