netsh advfirewall firewall add rule name="LabPing" dir=in action=allow protocol=icmpv4
http://<IP_DE_TU_PORTATIL>:8080/trabajo?id=0&n=1000&mb=1
netsh advfirewall firewall add rule name="LabRedes" dir=in action=allow protocol=TCP localport=8080
