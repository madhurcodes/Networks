import socket
import json
import base64
import time
import os
import threading

debug = 1
if not debug:
    while 1:
        try:
            numThreadsPerDomain = int(input("Enter the number of Threads Per Domain: "))
            numObjectsPerThread = int(input("Enter the number of Objects Per Thread: "))
            harfile_name = input("Enter the HAR File Name: ")
            harfile = open(harfile_name,"r")
            # pipe = int(input("Enter 1 for Pipelined Execution and 0 for not: "))
            pipe = 0
            PIPELINED = False if pipe ==1 else False
            break
        except:
            print("Invalid input. Please try again.")
else:
    numThreadsPerDomain = 3
    numObjectsPerThread = 2
    harfile_name = "bbc.har"
    harfile = open(harfile_name,"r")
    PIPELINED = False

foldername = harfile_name.split(".")[0]
har_json = json.load(harfile)
num_requests = len(har_json["log"]["entries"])
domain_dict = {}
act = threading.activeCount()
def fetch_thread(request_small):
    if not PIPELINED:
        for i in request_small:
#             print(threading.current_thread().name, " Processed url ", i["request"]["url"])
            url = i["request"]["url"]
            prefix = url[0:5]
            if prefix != "http:":
                continue
            url_split = url.split("://")

            content_file_path = foldername
            content_file_path = content_file_path + "/" + url_split[-1]
            if 1==1:#int(i["response"]["content"]["size"])!=0:
                har_req = i["request"]
                http_version = "HTTP" + har_req["httpVersion"][4:]
                request_str= har_req["method"] + " /" + har_req["url"].split("//")[1].split("/",maxsplit=1)[-1]+" "+ http_version + "\n" 
                hostname = (har_req["url"].split("//")[1]).split("/")[0]
                request_str = request_str + "Host"+": " + hostname+"\n"
                for el in har_req["headers"]:
                    if el["name"] not in ("User-Agent","Connection"):continue
                    request_str = request_str + el["name"]+": " + el["value"]+"\n"
                request_str = request_str + "\n"
        #         print("------------------------------")
        #         print(request_str)
        #         print("------------------------------")
                encoded_request = request_str.encode()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                print("Hostname is ", hostname)
                client_socket.connect((hostname, 80))
                client_socket.send(encoded_request)
                received_bytes = b""
                client_socket.settimeout(0.2)
                while 1:
                    try:
                        msg = client_socket.recv(1024)
                        if(len(msg)==0):
                            break
                        received_bytes = received_bytes + msg
                    except:
                        break
                split = received_bytes.split(b"\r\n\r\n")
                if len(received_bytes)<1 or len(split)<2:
                    continue
                header = split[0]
                client_socket.close()
                content = split[1]
                if content_file_path[-1]=="/":
                    content_file_path = content_file_path + "index.html"
                if not os.path.exists(os.path.dirname(content_file_path)):
                    try:
                        os.makedirs(os.path.dirname(content_file_path))
                    except: # Guard against race condition
                        print("Error :Race")
                try:
                    headerfile = open(content_file_path+"_header","wb")
                except:
                    headerfile = open(content_file_path[:33]+"_header","wb")
                headerfile.write(header)
                headerfile.close()
                try:
                    contentfile = open(content_file_path,"wb")
                except:
                    contentfile = open(content_file_path[:33],"wb")
                contentfile.write(content)
                contentfile.close()
#         else:
#             for i in request_small:
                
def dom_thread_fun(reqlist):
    tl = []
    done = 0
    tind = 0
    while len(reqlist) != done:
        if len(tl) == numThreadsPerDomain:
            while 1:
                a = 0
                for th in tl:
                    if th.isAlive():
                        a = 1
                if a==1:
                    continue
                else:
                    tl =[]
                    break
        tempList = reqlist[done:min(done+numObjectsPerThread, len(reqlist))]
        done += len(tempList)
        nt  = threading.Thread(name=threading.current_thread().name+"fetch"+str(tind),target=fetch_thread,args=(tempList,))
        tl.append(nt)
        tind+=1
        nt.start()
start_time = time.time()
for i in har_json["log"]["entries"]:
    domain_name = i["request"]["url"].split("//",maxsplit=1)[-1].split("/")[0].split(".",maxsplit=1)[1]
    if domain_name in domain_dict.keys():
        domain_dict[domain_name].append(i)
    else:
        domain_dict[domain_name] = [i]
list_of_threads = []
for dom in domain_dict.keys():
    t = threading.Thread(name=dom,target=dom_thread_fun,args=(domain_dict[dom],))
    list_of_threads.append(t)
    t.start()
while(threading.activeCount()!=act):
#     print("-")
    pass
elapsed_time = time.time() - start_time
print("Time Elasped is ", elapsed_time)