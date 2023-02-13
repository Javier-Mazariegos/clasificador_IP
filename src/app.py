from flask import Flask, url_for, request,redirect, abort
from jinja2 import Template, Environment, FileSystemLoader

environment="development"

app = Flask(__name__)


file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


bandera = 0
ip_guardada = None

@app.route('/')
def tiny():
    global bandera
    template = env.get_template("index.html")
    bandera = request.args.get('respuesta')
    ip_class = request.args.get('ip_class')
    class_name = request.args.get('class_name')
    ip_address = request.args.get('ip_address')
    if bandera == None:
        bandera = 0
    else:
        bandera = int(bandera)
    return template.render(bandera = bandera,ip_address = ip_address,ip_class=ip_class,class_name=class_name)


@app.route('/verificar', methods=['POST'])
def verificar():
    ip_class = ''
    class_name = ''
    if request.method == 'POST':
        ip_address = request.form['ip_verificar']
        respuesta = -1

        primer_octet = int(ip_address.split('.')[0])
        segundo_octet = int(ip_address.split('.')[1])
    
        if ip_address.startswith('10.'):
            ip_class = 'Privada'
            class_name = 'A'
        elif ip_address.startswith('172.') and (segundo_octet >= 16 and segundo_octet <= 31):
            ip_class = 'Privada'
            class_name = 'B'
        elif ip_address.startswith('192.168.'):
            ip_class = 'Privada'
            class_name = 'C'
        elif primer_octet >= 0 and primer_octet <= 126:
            ip_class = 'Publica'
            class_name = 'A'
        elif primer_octet >= 128 and primer_octet <= 191:
            ip_class = 'Publica'
            class_name = 'B'
        elif primer_octet >= 192 and primer_octet <= 223:
            ip_class = 'Publica'
            class_name = 'C'
        elif primer_octet >= 224 and primer_octet <= 239:
            ip_class = 'Publica'
            class_name = 'D'
        else:
            ip_class = 'Publica'
            class_name = 'E'
        
        return redirect(url_for('tiny',respuesta = respuesta, ip_address = ip_address,ip_class = ip_class, class_name = class_name), 301)

if __name__ == "__main__":
    debug=False
    if environment == "development" or environment == "local":
        debug=True
    print("Local change")
    app.run(host="localhost")