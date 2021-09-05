import os
import time
import sys
import subprocess
import threading
import psutil 
from procmon_parser import ProcmonLogsReader


TIME = 5

START_COMMAND = "Procmon64.exe /Minimized /Runtime "+str(TIME)+" /BackingFile out.pml"

extensions = {"doc": "WINWORD.EXE", "excel":"EXCEL.EXE","hwp":"HWP.EXE","exe":"","docx":"WINWORD.EXE"}


parse_result=[]


def kill_process(ps_name):

    if len(ps_name.split()) == 2:
        ps_name = ps_name.split()[0]
    ps_name = ps_name.lstrip()
    ps_name = ps_name.rstrip()
    
    print(ps_name.encode())

    for proc in psutil.process_iter():
        try:
            # 프로세스 이름, PID값 가져오기
            processName = proc.name()
            processID = proc.pid
            if processName == ps_name:
                print("MATCH")
                parent_pid = processID  #PID
                parent = psutil.Process(parent_pid) # PID 찾기
                for child in parent.children(recursive=True):  #자식-부모 종료
                    child.kill()
                parent.kill()
     
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):   #예외처리
            pass


def pml_parse(binary_name):
    file_lists = os.listdir(os.getcwd()) #search_logging_files
    
    print("[*]  Start Parsing!!!")
    for files in file_lists: # 특정 용량 초과하면 out-1.pml, out-2.pml 이렇게 만들어진다.
        if ".pml" not in files:
            continue
            
        while True:
            try:
                f = open(files, "rb")
                pml_reader = ProcmonLogsReader(f)
                break
            except:
                f.close()


        for i in range(len(pml_reader)):
            events = next(pml_reader)         
            if binary_name in str(events.process):
                parse_result.append(events)
                
                
    # print(parse_result)
    
def run_malware(f_name):
    subprocess.Popen(["python", "a.py", str(f_name)], stdout=subprocess.PIPE, shell=True)
    print("[*]  start!!")
    
def execute(f_name):
    
    subprocess.Popen(START_COMMAND.split(), stdout=subprocess.PIPE, shell=True)
    
    t = threading.Thread(target=run_malware,args=(f_name,))
    t.start()
    
    print("[*]  Waitting...")
    time.sleep(TIME)
    kill_process(f_name)  


def analysis_extention(name):
    si = name.split('.')[1].lower() # 파일 확장자명 뽑는다.
    
    ps = extensions[si] # 확장자명에 해당하는 프로세스명 뽑는다.
    
    return ps+" "+name


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("add argv")
        exit(1)
        
    param = sys.argv[1]
    
    ps_full_name = analysis_extention(param) # wordpress.exe 파일명 <- 이렇게 return

    execute(ps_full_name)

    pml_parse(param)


    #Save parse result 
    with open("monitoring_res.txt","wb") as f:
        for data in parse_result:
            f.write(str(data).encode())
            f.write("\n".encode())