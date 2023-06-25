from flask import Flask, render_template, request
import os
import psutil

app = Flask(__name__)

@app.route("/")
def index():

    ram = psutil.virtual_memory()
    cpu = psutil.cpu_freq()

    req_headers = {}
    for header in request.headers:
        req_headers[header[0]] = header[1]
    data = {
        "os_info": os.uname(),
        "resource_info": {
            "total_ram": f"{ram.total / (1024 ** 3):.2f} GB",
            "available_ram": f"{ram.available / (1024 ** 3):.2f} GB",
            "current_cpu_freq": f"{cpu.current:.2f} MHz",
            "min_cpu_freq": f"{cpu.min:.2f} MHz",
            "max_cpu_freq": f"{cpu.max:.2f} MHz"
        },
        "env_vars": os.environ,
        "req_headers": req_headers
    }
    return render_template("index.html", **data)

if __name__ == "__main__":
	app.run(debug=True)
