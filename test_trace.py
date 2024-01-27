from report.kimball import Kimball_Trace
def obtener_valor(info, clave):
    for tupla in info:
        if clave in tupla[1]:
            return tupla[1][clave]
    return None

def main():
    serial_number = '000047752400001240090008005664'    
    trace = Kimball_Trace('TRIDENT_DISPLAY')
    # trace.valid_serial(serial_number)
    # trace.valid_partnumber(serial_number)
    # print(trace.start_test())
    data = trace.case_settings_lst
    valor_gps_fw = int(obtener_valor(data, 'gps_fw'))
    print('➡ test_trace.py:16 valor_gps_fw type:', type(valor_gps_fw))
    print('➡ test_trace.py:16 valor_gps_fw:', valor_gps_fw)
    
if __name__ == "__main__":
    main()