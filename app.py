from flask import Flask, render_template, request, json

app = Flask(__name__)
import hostdetection
import checkport
import osdetect

#import graph


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/port-scan', methods=['GET', 'POST'])
def portScan():
    if request.method == 'POST':
        domain = request.form.get('domain')
        minrange = int(request.form.get('minrange'))
        maxrange = int(request.form.get('maxrange'))
        L = checkport.check_range(domain, minrange, maxrange)

        L = (json.dumps(L)).split(",")
        L_index = [x for x in range(1, len(L) + 1)]
        zipped = zip(L, L_index)
        return render_template("scanport.html", zipped=zipped)

    return render_template("scanport.html")


@app.route('/os-informations', methods=['GET', 'POST'])
def osInfo():
    if request.method == 'POST':
        domain = request.form.get('domain')
        resp = osdetect.osdetection(domain).replace(":", ",").split(",")
        list1 = [resp[0][1:], resp[2][1:], resp[4][1:], resp[6][1:], resp[8][1:]]
        list2 = [resp[1], resp[3], resp[5], resp[7], resp[9][:len(resp[9]) - 1]]
        zipped = zip(list1, list2)
        return render_template("os_info.html", zipped=zipped)
        # return osdetect.osdetection(domain)

    return render_template("os_info.html")


@app.route('/host-detection', methods=['GET', 'POST'])
def host():
    if request.method == 'POST':
        domain = request.form.get('domain')
        resp = json.dumps({'active hosts': hostdetection.activeHosts(domain)}).split(",")
        index = [x for x in range(1, len(resp))]
        zipped = zip(resp[1:], index)
        return render_template("host.html", zipped=zipped)

    return render_template("host.html")


@app.route('/firewall-detail')
def firewallDetails():
    return render_template("firewall.html")



if __name__ == "__main__":
    app.run(debug=True)
