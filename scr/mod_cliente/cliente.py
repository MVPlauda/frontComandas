from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_CLIENTE
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/')
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        # para teste
        print(result)
        print(response.status_code)

        if response.status_code != 200:
            raise Exception(result)

        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])



@bp_cliente.route('/form-cliente/', methods=['GET'])
def formCliente():
    return render_template('formCliente.html')
#Rota antiga de app...
#@app.route('/funcionario/')
#def formListaFuncionario():
# return "<h1>Rota da página de Funcionários da nossa WEB APP</h1>", 200
#return render_template('formListaFuncionario.html'), 200