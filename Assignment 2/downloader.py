import socket
import json
import base64
import os
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
    right_part = foldername
    right_part = right_part + "/" + spl[-1]
    if int(i["response"]["content"]["size"])!=0:
        if not "text" in i["response"]["content"].keys():
            continue
        print(right_part)
        if right_part[-1]=="/":
            right_part = right_part + "index.html"
        # print(os.path.dirname(right_part))
        if not os.path.exists(os.path.dirname(right_part)):
            try:
                os.makedirs(os.path.dirname(right_part))
            except: # Guard against race condition
                print("Error :Race")
                exit(1)
        
        # print(i["response"]["content"]["text"])
        to_write = i["response"]["content"]["text"]
        if "encoding" in i["response"]["content"].keys():
            if i["response"]["content"]["encoding"] == "base64":
                # print(right_part)
                # print(to_write)
                newfile = open(right_part,"wb")
                to_write = base64.b64decode(to_write)
                # to_write = to_write.decode("ascii")
                newfile.write(to_write)
                newfile.close()
            else:
                print("Wierd Encoding")
                raise ValueError
        else:
            newfile = open(right_part,"w")
            newfile.write(to_write)
            newfile.close()

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# # host = socket.gethostname()                           
# # client_socket.connect(("67.207.86.98", 3469))                               
# client_socket.connect(("www.nytimes.com", 80))                               

# # Receive no more than 1024 bytes
# req = b"""GET / HTTP/1.1 
# User-Agent: SSSS
# Host: www.nytimes.com
# Accept-Language: en-us
# Connection: Keep-Alive

# """
# client_socket.send(req)
# msg = client_socket.recv(2024)                                     

# client_socket.close()

# print (msg.decode('ascii'))
