service_mapping = {
    "nginx": {
        "stop":   "nginx -s stop",
        "start":  "nginx",
        "reload": "nginx -s reload",
        "check":  "nginx -t",
        "status": ""
    }
}
function_mapping = {
    "info": "uptime",
}

from src.cmd.machine_info import FabricConnection

def CmdRes():
    host = '39.105.101.140'
    user = 'admin'
    password = 'asdf1234!'
    port = 17890
    ssh = FabricConnection(host, user, password, port)
    ssh.execute_command("uptime")

CmdRes()


