import json
import xmltodict
from libnmap.process import NmapProcess

# 옵션을 받아서 target 에 nmap 을 수행하고, 그 결과를 xml 형태로 반환함
# usage: nmap_target("localhost", "-A", "-p 8000,22,90,445")
def nmap_target(target, *options):
    SUCCESS = 0
    result = ''
    nm = NmapProcess(target, options = ' '.join(options))
    v = nm.run()
    if v == SUCCESS:
        result = nm.stdout
    else:
        print("Nmap Failed")
        exit(1)

    return result


def nmap_parser(xml_content):
    # json 형태로 바꿔 변수에 저장
    str_content = json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True)
    json_content = json.loads(str_content)
    json_data = json_content["nmaprun"]["host"]["ports"]
    json_data = json_data["port"]
    res = []

    # 나온 포트가 1개인 경우, list 형태로 만들어줌.
    # 나온 포트가 2개 이상인 경우와 일관성을 맞춰주기 위함
    if isinstance(json_data, dict):
        json_data = [ json_data ]

    for data in json_data:
        d = {}
        if "@portid" in data.keys():
            d["port"]=data["@portid"]
        if "@protocol" in data.keys():
            d["protocol"]=data["@protocol"]
        if "service" in data.keys():
            if "@name" in data["service"]:
                d["service_name"] = data["service"]["@name"]
            if "@product" in data["service"]:
                d["service_product"] = data["service"]["@product"]
            if "@version" in data["service"]:
                d["service_version"] = data["service"]["@version"]
        res.append(d)
    
    return res

if __name__ == "__main__":
    a = nmap_target("localhost", "-A", "-p 12345,80")
    res = nmap_parser(a)
    print(res)