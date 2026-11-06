import psutil
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)
def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent  
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent
def get_cpu_all_cores():
    return psutil.cpu_count(logical=True) and psutil.cpu_count(logical=False)

