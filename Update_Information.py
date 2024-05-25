import psutil
import platform
from datetime import datetime
import time
import netifaces
import tkinter as tk
from tkinter import ttk

try:
    import pynvml
    pynvml.nvmlInit()
    gpu_temp_available = True
except ImportError:
    gpu_temp_available = False

def get_size(bytes, suffix="B"):
    """
    将字节数转换为适当的大小（如KB，MB，GB等）
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info():
    try:
        # 获取操作系统信息
        uname = platform.uname()
        system_info = {
            "系统": uname.system,
            "节点名称": uname.node,
            "版本": uname.version,
            "机器": uname.machine,
            "处理器": uname.processor,
        }

        # 获取CPU信息
        cpu_info = {
            "物理核心数": psutil.cpu_count(logical=False),
            "逻辑核心数": psutil.cpu_count(logical=True),
            "CPU频率": f"{psutil.cpu_freq().current:.2f} MHz",
            "CPU使用率": f"{psutil.cpu_percent(interval=1)}%",
        }

        # 获取内存信息
        svmem = psutil.virtual_memory()
        memory_info = {
            "总内存": get_size(svmem.total),
            "可用内存": get_size(svmem.available),
            "已使用内存": get_size(svmem.used),
            "内存使用率": f"{svmem.percent}%",
        }

        # 获取温度信息
        temps = psutil.sensors_temperatures()
        temperature_info = {}
        if 'coretemp' in temps:
            for entry in temps['coretemp']:
                temperature_info[entry.label or 'CPU温度'] = f"{entry.current}°C"

        # 获取GPU温度（如果可用）
        if gpu_temp_available:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                temperature_info["GPU温度"] = f"{gpu_temp}°C"
            except Exception as e:
                temperature_info["GPU温度"] = "无法获取"

        # 获取网络信息
        network_info = {}
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            if interface not in ['lo', 'utun']:  # 过滤掉不需要的接口
                for addr in addrs:
                    if addr.family == netifaces.AF_INET:
                        mac_addr = None
                        if addrs:
                            for addr_ in addrs:
                                if addr_.family == netifaces.AF_LINK:
                                    mac_addr = addr_.address
                                    break
                        network_info[interface] = {
                            "IP地址": addr.address,
                            "MAC地址": mac_addr
                        }

        # 获取启动时间
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        boot_time = bt.strftime("%Y-%m-%d %H:%M:%S")

        # 汇总信息
        info = {
            "系统信息": system_info,
            "CPU信息": cpu_info,
            "内存信息": memory_info,
            "温度信息": temperature_info,
            "网络信息": network_info,
            "启动时间": boot_time,
        }
        return info

    except Exception as e:
        print(f"Error while gathering system information: {e}")
        return {}

def update_info():
    info = get_system_info()
    for category, details in info.items():
        text = f"{category}:\n"
        if isinstance(details, dict):
            for key, value in details.items():
                text += f"  {key}: {value}\n"
        else:
            text += "  无法获取详细信息\n"
        info_labels[category].config(text=text)
    root.after(1500, update_info)  # 每5秒更新一次信息

root = tk.Tk()
root.title("系统信息监控")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

info_labels = {}

categories = ["系统信息", "CPU信息", "内存信息", "温度信息", "网络信息", "启动时间"]
for idx, category in enumerate(categories):
    label = ttk.Label(frame, text="", justify="left", padding="5")
    label.grid(row=idx, column=0, sticky=(tk.W, tk.E))
    info_labels[category] = label

update_info()  # 初始调用以获取信息

root.mainloop()

