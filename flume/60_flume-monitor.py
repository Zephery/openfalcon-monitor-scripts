#!/usr/bin/python
#!-*- coding:utf8 -*-

'''
read flume metrics from flume JSON Reporting
flume-env.sh should add JAVA_OPTS: -Dflume.monitoring.type=http -Dflume.monitoring.port=3000
'''

import requests
import json
import time
import socket

hostname=socket.gethostname()
ts=int(time.time())
step=60
GAUGE="GAUGE"

def load(hostname,metric,timestamp,step,value,counterType,tags):
    msg={
        "endpoint": hostname,
        "metric": metric,
        "timestamp": timestamp,
        "step": step,
        "value": value,
        "counterType": counterType,
        "tags": tags,
        }

    return msg

try:
    #this is your flume metrics http url, you should change is by your flume environment
    url="http://127.0.0.1:3000/metrics"
    tags="port=3000"
    v=requests.get(url)
    res=json.loads(v.text)
    payload=[]
    for key in res:
        type=res[key]["Type"]
        if type == "SOURCE":
            for param in ["OpenConnectionCount"]:
                metric=key.replace("SOURCE.","")+"_"+param
                value=float(res[key][param])
                msg=load(hostname,metric,ts,step,value,GAUGE,tags)
                payload.append(msg)

            for param in ["AppendBatchAcceptedCount", "AppendBatchReceivedCount", "EventAcceptedCount", "AppendReceivedCount", "EventReceivedCount", "AppendAcceptedCount"]:
                metric=key.replace("SOURCE.","")+"_"+param
                value=float(res[key][param])
                msg=load(hostname,metric,ts,step,value,GAUGE,tags)
                payload.append(msg)

        elif type == "CHANNEL":
            for param in ["ChannelSize", "ChannelFillPercentage"]:
                metric=key.replace("CHANNEL.","")+"_"+param
                value=float(res[key][param])
                msg=load(hostname,metric,ts,step,value,GAUGE,tags)
                payload.append(msg)

            for param in ["EventPutSuccessCount", "EventPutAttemptCount", "EventTakeSuccessCount", "EventTakeAttemptCount"]:
                metric=key.replace("CHANNEL.","")+"_"+param
                value=float(res[key][param])
                msg=load(hostname,metric,ts,step,value,GAUGE,tags)
                payload.append(msg)

        elif type == "SINK":
            for param in ["BatchCompleteCount", "ConnectionFailedCount", "EventDrainAttemptCount", "ConnectionCreatedCount", "BatchEmptyCount", "ConnectionClosedCount", "EventDrainSuccessCount", "BatchUnderflowCount"]:
                metric=key.replace("SINK.","")+"_"+param
                value=float(res[key][param])
                msg=load(hostname,metric,ts,step,value,GAUGE,tags)
                payload.append(msg)

    print json.dumps(payload)
    #r = requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload))
except Exception,e:
    print e
