import nidaqmx

def turn_on_UUT(device_name, port, line):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(f"{device_name}/port{port}/line{line}")
        task.write(True, auto_start=True)

def turn_off_UTT(device_name, port, line):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(f"{device_name}/port{port}/line{line}")
        task.write(False, auto_start=True)