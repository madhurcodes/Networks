import json
import sys

with open(sys.argv[1], 'r') as json_string:
    parsed_json = json.load(json_string)
    
print ("Total number of objects downloaded :", len(parsed_json["log"]["entries"]))
print ("Number of objects downloaded from different domains")
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] += 1
for i in domain.keys():
    print (i, "-", domain[i])
print ("\n")    

total_size = 0
for i in range(len(parsed_json["log"]["entries"])):
    total_size += parsed_json["log"]["entries"][i]["response"]["content"]["size"]
print ("Total size of content downloaded (in bytes) :", total_size)
print ("Size of content downloaded (in bytes) from different domains")
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] += parsed_json["log"]["entries"][i]["response"]["content"]["size"]   
for i in domain.keys():
    print (i, "-", domain[i])
print ("\n")  

print ("Number of TCP connections opened to each domain") 
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = set([])
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]].add(parsed_json["log"]["entries"][i]["connection"])
for i in domain.keys():
    print(i, "-", len(domain[i]))
print ("\n")

print ("Number and size of objects downloaded on each TCP connection")
print ("connection ID - domain - number of objects - size of objects")
connectionNum = {}
connectionSize = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        connectionNum[parsed_json["log"]["entries"][i]["connection"]] = connectionSize[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        connectionNum[parsed_json["log"]["entries"][i]["connection"]] += 1
        connectionSize[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["response"]["content"]["size"]
for i in domain.keys():
    for j in domain[i]:
        print (j, "-", i, "-", connectionNum[j], "-", connectionSize[j])
print ("\n")   

print ("Time spent in DNS query when opening the first TCP connection for each hostname")
print ("connection ID - hostname - DNS query time")
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i] and parsed_json["log"]["entries"][i]["timings"]["dns"] != -1:
        print (parsed_json["log"]["entries"][i]["connection"], "-", parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0], "-", parsed_json["log"]["entries"][i]["timings"]["dns"])
print ("\n")

print ("Timing analysis on each TCP connection")
connect = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        connect[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i] and parsed_json["log"]["entries"][i]["timings"]["connect"] != -1:
        connect[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["connect"]
        
# Average time spent by a TCP connection on waiting for a server to respond        
wait = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        wait[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        wait[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["wait"]
for i in wait.keys():
    wait[i] /= connectionNum[i]
    
# Total time spent in receiving data
receive = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        receive[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        receive[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["receive"]
       
maxSize = {}
rcvTime = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        maxSize[parsed_json["log"]["entries"][i]["connection"]] = 0
        rcvTime[parsed_json["log"]["entries"][i]["connection"]] = 0
        for j in range(len(parsed_json["log"]["entries"])):
            if "connection" in parsed_json["log"]["entries"][j] and parsed_json["log"]["entries"][i]["connection"] == parsed_json["log"]["entries"][j]["connection"]:
                if maxSize[parsed_json["log"]["entries"][i]["connection"]] < parsed_json["log"]["entries"][j]["response"]["content"]["size"]:
                    maxSize[parsed_json["log"]["entries"][i]["connection"]] = parsed_json["log"]["entries"][j]["response"]["content"]["size"]
                    rcvTime[parsed_json["log"]["entries"][i]["connection"]] = parsed_json["log"]["entries"][j]["timings"]["receive"]
            
print ("connection ID - connection establishment time - average waiting time - total receive time - average goodput - maximum achieved goodput")        
for i in connect.keys():
    if rcvTime[i] == 0:
        try:
            print (i, "-", connect[i], "-", wait[i], "-", receive[i], "-", connectionSize[i] / receive[i], "-", 0.0)
        except:
            print (i, "-", connect[i], "-", wait[i], "-", receive[i], "-", connectionSize[i] / 1, "-", 0.0)
    else:    
        print (i, "-", connect[i], "-", wait[i], "-", receive[i], "-", connectionSize[i] / receive[i], "-", maxSize[i] / rcvTime[i])
print ("\n")

totalReceiveTime = 0
for i in range(len(parsed_json["log"]["entries"])):
    totalReceiveTime += parsed_json["log"]["entries"][i]["timings"]["receive"]
print ("Average achieved goodput of the network (across all domains) :", total_size / totalReceiveTime)    
maxGoodput = 0
for i in connect.keys():
    if rcvTime[i] != 0 and maxGoodput < maxSize[i] / rcvTime[i]:
        maxGoodput = maxSize[i] / rcvTime[i]
print ("Maximum of the maximum achieved goodput (on all connections) :", maxGoodput, "\n")        

print ("Page load time obtained from onLoad entry :", parsed_json["log"]["pages"][0]["pageTimings"]["onLoad"])
pageLoadTime = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        pageLoadTime[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in pageLoadTime.keys():
    pageLoadTime[i] += connect[i]
maxWaitTime = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        maxWaitTime[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        if maxWaitTime[parsed_json["log"]["entries"][i]["connection"]] < parsed_json["log"]["entries"][i]["timings"]["wait"]:
            maxWaitTime[parsed_json["log"]["entries"][i]["connection"]] = parsed_json["log"]["entries"][i]["timings"]["wait"] 
for i in pageLoadTime.keys():
    pageLoadTime[i] += maxWaitTime[i]
sumSendTime = {}
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        sumSendTime[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        sumSendTime[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["send"]
for i in pageLoadTime.keys():
    pageLoadTime[i] += sumSendTime[i]  
for i in pageLoadTime.keys():
    pageLoadTime[i] += receive[i]
maxTime = 0
for i in pageLoadTime.keys():
    if maxTime < pageLoadTime[i]:
        maxTime = pageLoadTime[i]
maxDNSTime = 0
for i in range(len(parsed_json["log"]["entries"])):
    if maxDNSTime < parsed_json["log"]["entries"][i]["timings"]["dns"]:
        maxDNSTime = parsed_json["log"]["entries"][i]["timings"]["dns"]
maxTime += maxDNSTime
print ("Best page load time obtained by collapsing all GET requests on each TCP connection and opening all connections simultaneously (in ms):", maxTime)
for i in pageLoadTime.keys():
    pageLoadTime[i] -= receive[i]
for i in pageLoadTime.keys():
    if maxSize[i] != 0 and rcvTime[i] != 0:
        pageLoadTime[i] += connectionSize[i] / (maxSize[i] / rcvTime[i])
maxTime = 0
for i in pageLoadTime.keys():
    if maxTime < pageLoadTime[i]:
        maxTime = pageLoadTime[i]
maxTime += maxDNSTime
print ("Best page load time obtained by assuming that all content on a connection can be downloaded at the maximum achieved goodput (in ms):", maxTime)
