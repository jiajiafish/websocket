from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
from pprint import pprint
import json
import threading

# Create your views here.

clients = []


def index(request):
    return render(request, 'index.html')


def index2(request):
    return render(request, 'index2.html')


# @accept_websocket
# def echo(request):
#     if request.is_websocket:#如果是webvsocket
#         lock = threading.RLock() #rlock线程锁
#         try:
#             lock.acquire()#抢占资源
#             clients.append(request.websocket)#把websocket加入到clients
#             print(clients)
#             for message in request.websocket:
#                 if not message:
#                     break
#                 for client in clients:
#                     client.send(message)
#         finally:
#             clients.remove(request.websocket)
#             lock.release()#释放锁

def modify_message(message):
    return message.lower()


@accept_websocket
def echo(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        print(request.websocket.count_messages())
        print(request.websocket.has_messages())
        clients.append(request)
        pprint(request.GET['note'])

        for message in request.websocket:
            for client in clients:
                pprint(client.websocket.closed)
                if client.websocket.closed:
                    pass
                else:
                    pprint(message)
                    data = {'type': 'Reply',
                            'content': str(message, 'utf-8'),
                            "avatar": "http://shotgun.saic-gm.com/thumbnail/api_image/165943?AccessKeyId=uTbPnnWUNhn2nSG7Agrp&Expires=1554895522&Signature=zLbX7Zn2MkAc2wWJMfdsSKaIlC%2Bm5yLx11vC1tlbSCM%3D",
                            "created_at": "2019-04-10T16:40:36+08:00"

                            }
                    pprint(data)
                    # client.websocket.send(message)
                    client.websocket.send(json.dumps(data))
# @require_websocket
# def echo_once(request):
#     message = request.websocket.wait()
#     print(request.websocket.count_messages())
#     print(request.websocket.has_messages())
#     request.websocket.send(message)
