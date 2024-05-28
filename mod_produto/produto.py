from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_PRODUTO
bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/')
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        # para teste
        print(result)
        print(response.status_code)

        if response.status_code != 200:
            raise Exception(result)

        return render_template('FormListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('FormListaProduto.html', msgErro=e.args[0])


@bp_produto.route('/form-produto/', methods=['GET'])
def formProduto():
    return render_template('FormProduto.html')


#Rota antiga de app...
#@app.route('/funcionario/')
#def formListaFuncionario():
# return "<h1>Rota da página de Funcionários da nossa WEB APP</h1>", 200
#return render_template('formListaFuncionario.html'), 200