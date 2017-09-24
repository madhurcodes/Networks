import json
import sys

with open(sys.argv[1], 'r') as json_string:
    parsed_json = json.load(json_string)
print ("Total number of objects downloaded :", len(parsed_json["log"]["entries"]))
print ("\n")
print ("Number of objects downloaded from different domains")
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] += 1
for i in domain.keys():
    print (i, domain[i])
print ("\n")    
total_size = 0
for i in range(len(parsed_json["log"]["entries"])):
    total_size += parsed_json["log"]["entries"][i]["response"]["content"]["size"]
print ("Total size of content downloaded (in bytes) :", total_size)
print ("\n")
print ("Size of content downloaded (in bytes) from different domains")
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] += parsed_json["log"]["entries"][i]["response"]["content"]["size"]   
for i in domain.keys():
    print (i, domain[i])
print ("\n")    
print ("Number of TCP connections opened to each domain")    
domain = {}
for i in range(len(parsed_json["log"]["entries"])):
    domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]] = set([])
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        domain[parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1]].add(parsed_json["log"]["entries"][i]["connection"])
for i in domain.keys():
    print(i, len(domain[i]))
print("\n")    
print ("Number and size of objects downloaded on each TCP connection")
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
        print (i, connectionNum[j], connectionSize[j])
print ("\n")        
print ("Page load time obtained from onLoad entry :", parsed_json["log"]["pages"][0]["pageTimings"]["onLoad"])
print ("\n")
print ("Time spent in DNS query when opening the first TCP connection for each domain")
for i in range(len(parsed_json["log"]["entries"])):
    if (parsed_json["log"]["entries"][i]["timings"]["dns"] != -1):
        print (parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1], parsed_json["log"]["entries"][i]["timings"]["dns"])
print ("\n")

connect = {}
response = {}
receive = {}
print ("Timing analysis on each TCP connection")
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        connect[parsed_json["log"]["entries"][i]["connection"]] = 0
        response[parsed_json["log"]["entries"][i]["connection"]] = 0
        receive[parsed_json["log"]["entries"][i]["connection"]] = 0
for i in range(len(parsed_json["log"]["entries"])):
    if "connection" in parsed_json["log"]["entries"][i]:
        if parsed_json["log"]["entries"][i]["timings"]["connect"] != -1:
            connect[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["connect"]
        response[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["wait"]
        receive[parsed_json["log"]["entries"][i]["connection"]] += parsed_json["log"]["entries"][i]["timings"]["receive"]
for i in sorted(connect):
    print (i, connect[i], response[i], receive[i])
        
#print ("Timing analysis on each TCP connection")
#for i in range(len(parsed_json["log"]["entries"])):
#    if "connection" in parsed_json["log"]["entries"][i] and parsed_json["log"]["entries"][i]["timings"]["connect"] != -1:
#        print ("connection :", parsed_json["log"]["entries"][i]["connection"])
#        print ("domain :", parsed_json["log"]["entries"][i]["request"]["url"].split("//")[1].split("/")[0].split(".", 1)[1])
#        print ("connection establishment time :", parsed_json["log"]["entries"][i]["timings"]["connect"])
#        print ("response wait time :", parsed_json["log"]["entries"][i]["timings"]["wait"])
#        print ("receive data time :", parsed_json["log"]["entries"][i]["timings"]["receive"])
    
    
