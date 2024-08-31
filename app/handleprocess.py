import subprocess
import time

def get_pids(port)-> list | list[int]:
    try:
        # 尝试使用sudo权限运行lsof命令
        output = subprocess.run(['sudo', 'lsof', '-i', f':{port}'], capture_output=True, text=True, check=True).stdout
    except:
        try:
            # 如果sudo失败，则尝试不使用sudo权限运行lsof命令
            output = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError:
            # 处理lsof命令执行失败的情况
            return []
    
    # 使用列表推导式获取进程ID
    # print(output) # 输出 str 类型的进程信息, 
    # output.splitlines() # 按将字符串按照分隔符\n、\r、\r\n进行分割。 返回一个列表。 keepends=False：不保留分隔符(默认值)。 
    pids = [int(line.split()[1]) for line in output.splitlines()[1:] if line.strip()]
    return pids

def kill_process(port) -> None:
    pids = get_pids(port)
    if not pids:
        return
    for pid in pids:
        subprocess.run(['sudo', 'kill', '-9', str(pid)])
    time.sleep(2) # 等待进程结束,不然太快了,易出错
    print(f'====== Killed processes on port: {port} ======')
    return

if __name__ == '__main__':
    port = 9100
    print(get_pids(port))
    # kill_process(port)
    print(f'Killed processes on port {port}')
