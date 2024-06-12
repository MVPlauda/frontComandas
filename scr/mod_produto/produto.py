from flask import send_file
# from mod_produto.GeraPdf import PDF
from flask import Blueprint, render_template, request, jsonify
import requests
import base64
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_PRODUTO

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''
@bp_produto.route('/')
@validaToken
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        return render_template('FormListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('FormListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        
        valor_unitario = float(request.form['valor_unitario'].replace('R$', '').replace(',', '.'))

        # converte em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")

        # monta o JSON para envio à API
        payload = {'id': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}

        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = float(request.form['valor_unitario'].replace('R$', '').replace(',', '.'))
        print(valor_unitario)
        foto_file = request.files['foto']
        # valor_unitario = (valor_unitario)
 
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
       
        # converte em base64
        # foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")

        # monta o JSON para envio à API
        payload = {'id': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}

        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        # dados enviados via FORM
        id_produto = request.form['id_produto']

        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return jsonify(erro=False, msg=result[0])

    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
        
@bp_produto.route('/form-produto/', methods=['GET', 'POST'])
@validaToken
def formProduto():
    return render_template('FormProduto.html')

@bp_produto.route("/form-edit-produto/", methods=['POST', 'GET'])
@validaToken
def formEditProduto():
    try:
        # ID enviado via FORM
        id_produto = request.form['id']

        # executa o verbo GET da API buscando somente o produto selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        
        result = response.json()
        if (response.status_code != 200):
            
            raise Exception(result)

        # renderiza o form passando os dados retornados
        return render_template('FormProduto.html', result=result[0])

    except Exception as e:
        
        print(e)
        return render_template('FormListaProduto.html', msgErro=e.args[0])
