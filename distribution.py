class Device():
    def __init__(self, message, device_cpu, device_mem):
        self.load = []
        self.remain_cpu = device_cpu
        self.remain_mem = device_mem

    def load_flavor(self, flavor_name, v_cpu , v_mem):
        self.load.append(flavor_name)
        self.remain_cpu = self.remain_cpu - v_cpu
        self.remain_mem = self.remain_mem - v_mem

class Flavors:
    def __init__(self, name, amount_cpu, amount_mem):
        self.name = name
        self.amount_cpu = amount_cpu
        self.amount_mem = amount_mem

def process(flavors, devices):
    coiunt=0
    for flavor_cur in flavors:
        coiunt+=1
        flag = 0
        for device_cur in devices:
            if device_cur.remain_cpu >= flavor_cur.amount_cpu and device_cur.remain_mem >= flavor_cur.amount_mem and flag==0:
                device_cur.load_flavor(flavor_cur.name, flavor_cur.amount_cpu, flavor_cur.amount_mem)
                flag = 1
        if flag==0:
            devices.append(Device('', device_cpu, device_mem))
            devices[len(devices)-1].load_flavor(flavor_cur.name, flavor_cur.amount_cpu, flavor_cur.amount_mem)
    return devices

def distribute(count_predict, dict_input_cpu, dict_input_mem, cpu_device, mem_device,target):
    global device_cpu
    global device_mem
    device_cpu=cpu_device
    device_mem=mem_device
    flavors = []
    # sorted(dict_input_cpu.items(), key=lambda e: e[1], reverse=True)
    if target=='CPU':
        for i in sorted(dict_input_cpu.items(), key=lambda e: e[1], reverse=True):
            for j in range(count_predict[i[0]]):
                flavors.append(Flavors(i[0], dict_input_cpu[i[0]], dict_input_mem[i[0]]))
    if target=='MEM':
        for i in sorted(dict_input_mem.items(), key=lambda e: e[1], reverse=True):
            for j in range(count_predict[i[0]]):
                flavors.append(Flavors(i[0], dict_input_cpu[i[0]], dict_input_mem[i[0]]))
    #xiang zi init 1
    devices = []
    devices.append(Device('', device_cpu, device_mem))
    devices = process(flavors,devices)
    return devices
