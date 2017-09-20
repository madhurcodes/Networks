import socket
import json
import base64
import os
import threading

harfile_name = "bbc.har"
foldername = harfile_name.split(".")[0]
harfile = open(harfile_name,"r")
har_json = json.load(harfile)
num_requests = len(har_json["log"]["entries"])
for i in har_json["log"]["entries"]:
    url = i["request"]["url"]
    prefix = url[0:5]
    # print(prefix)
    if prefix != "http:":
        continue
    url_split = url.split("://")
    
    content_file_path = foldername
    content_file_path = content_file_path + "/" + url_split[-1]
    if int(i["response"]["content"]["size"])!=0:
#         if not "text" in i["response"]["content"].keys():
#             continue
        print(content_file_path)
        if content_file_path[-1]=="/":
            content_file_path = content_file_path + "index.html"
        # print(os.path.dirname(right_part))
        if not os.path.exists(os.path.dirname(content_file_path)):
            try:
                os.makedirs(os.path.dirname(content_file_path))
            except: # Guard against race condition
                print("Error :Race")
                exit(1)
        har_req = i["request"]
        http_version = "HTTP" + har_req["httpVersion"][4:]
        request_str= har_req["method"] + " /" + har_req["url"].split("//")[1].split("/",maxsplit=1)[-1]+" "+ http_version + "\n" 
        hostname = (har_req["url"].split("//")[1]).split("/")[0]
        request_str = request_str + "Host"+": " + hostname+"\n"
        for el in har_req["headers"]:
            if el["name"] not in ("User-Agent","Connection"):continue
            request_str = request_str + el["name"]+": " + el["value"]+"\n"
#         request_str = request_str + "Conncetion"+": " + "Close"+"\n"
#         request_str = request_str + "User-Agent"+": " + har_req["headers"]+"\n"
        request_str = request_str + "\n"
        print("------------------------------")
        print(request_str)
        print("------------------------------")
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
                
        header = received_bytes.split(b"\r\n\r\n")[0]
        client_socket.close()
        content = received_bytes.split(b"\r\n\r\n")[-1]
        headerfile = open(content_file_path+"_header","wb")
        headerfile.write(header)
        headerfile.close()
        contentfile = open(content_file_path,"wb")
        contentfile.write(content)
        contentfile.close()
