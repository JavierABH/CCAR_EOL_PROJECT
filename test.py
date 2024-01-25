import clr

dll = r'C:\CCAR_EOL_Project\Dlls\WSConnector.dll'
clr.AddReference(dll)

from WSConnector import Connector

connector = Connector() 

def main():    
    datee = ""
    rp = connector.CIMP_GetDateTimeStr(datee)
    print(rp)

if __name__ == "__main__":
    main()
