from flask import Flask, render_template, request
import os
import psutil
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    # Request info
    req_headers = {}
    for header in request.headers:
        req_headers[header[0]] = header[1]
    # Resource info
    ram = psutil.virtual_memory()
    cpu = psutil.cpu_freq()
    # # Disk usage
    l = "<b>{:10} | {:11} | {} </b>".format("Used/Total", "Device", "Mountpoint").replace(" ", "&nbsp;")
    disk_usage = [l]
    for partition in sorted(psutil.disk_partitions(all=True), key=lambda x: psutil.disk_usage(x.mountpoint).total, reverse=True):
        device = partition.device
        mountpoint = partition.mountpoint
        total = f"{psutil.disk_usage(partition.mountpoint).total / (1024 ** 3):.2f} GB"
        used = f"{psutil.disk_usage(partition.mountpoint).used / (1024 ** 3):.2f} GB"
        tmp = f"{used}/{total}"
        disk_usage.append(f"{tmp:21} | {device:11} | {mountpoint}".replace(" ", "&nbsp;"))

    # Data to be sent to the template
    data = {
        "fqdn": subprocess.check_output(["hostname", "-f"]).decode("utf-8"),
        "os_info": os.uname(),
        "request_info": {
            "type": request.method,
            "path": request.path,
            "full_url": request.url,
            "query_parameters": request.args
        },
        "resource_info": {
            "total_ram": f"{ram.total / (1024 ** 3):.2f} GB",
            "used_ram": f"{ram.used / (1024 ** 3):.2f} GB",
            "current_cpu_freq": f"{cpu.current:.2f} MHz",
            "min_cpu_freq": f"{cpu.min:.2f} MHz",
            "max_cpu_freq": f"{cpu.max:.2f} MHz",
            "disk_usage": disk_usage
        },
        "env_vars": os.environ,
        "req_headers": req_headers
    }


    return render_template("index.html", **data)

@app.route("/ping")
def pingCheck():
    query = request.args.get("q")
    if query:
        try:
            # ping with query
            result = subprocess.check_output(["timeout", "2s", "ping", "-c", "1", query])
            return {
                "success": True,
                "message": "Ping successful",
                "data": result.decode("utf-8").splitlines()
            }
        except Exception as e:
            return {
                "success": False,
                "message": "Ping failed",
                "data": []
            }
    return {
        "success": False,
        "message": "No query provided",
        "data": []
    }

@app.route("/dns")
def dnsCheck():
    query = request.args.get("q")
    if query:
        try:
            # ping with query
            result = subprocess.check_output(["timeout", "2s", "nslookup", query])
            return {
                "success": True,
                "message": "DNS lookup successful",
                "data": result.decode("utf-8").splitlines()
            }
        except Exception as e:
            return {
                "success": False,
                "message": "DNS lookup failed",
                "data": ""
            }
    return {
        "success": False,
        "message": "No query provided",
        "data": ""
    }

@app.route("/routetable")
def routeTable():
    format = request.args.get("format")
    try:
        # ping with query
        if format == "tabular":
            result = subprocess.check_output(["route"])
        else :
            result = subprocess.check_output(["ip", "route", "show"])
        return {
            "success": True,
            "message": "Routing table fetched",
            "data": [x.replace(" ","&nbsp;") for x in result.decode("utf-8").splitlines()]
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to fetch route table",
            "data": ""
        }
    
@app.route("/network_interfaces")
def networkInterfaces():
    try:
        # ping with query
        result = subprocess.check_output(["ip", "addr", "show"])
        return {
            "success": True,
            "message": "Network interfaces fetched",
            "data": [x.replace(" ","&nbsp;") for x in result.decode("utf-8").splitlines()]
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Failed to fetch network interfaces",
            "data": ""
        }
    
@app.route("/fqdn")
def fqdn():
    try:
        # ping with query
        result = subprocess.check_output(["hostname", "-f"])
        return result.decode("utf-8")
    except Exception as e:
        return "Failed to fetch FQDN"

if __name__ == "__main__":
	app.run(debug=False, port=3000, host="0.0.0.0")
