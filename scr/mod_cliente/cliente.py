from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
import requests
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_CLIENTE
from funcoes import Funcoes
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')
from reportlab.pdfgen import canvas
import os

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

    
@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_cliente = 0
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        print(request.form)
        login = request.form['login']
        senha = Funcoes.get_password_hash(request.form['senha'])

        # monta o JSON para envio a API
        payload = {
            'id': id_cliente,
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'login': login, # 'login': 'teste
            'senha': senha
        }

        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code)  # 200

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route("/form-edit-cliente", methods=['POST'])
def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result)
            # renderiza o form passando os dados retornados
        return render_template('formCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit', methods=['POST'])
def edit():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        login = request.form['login']
        senha = Funcoes.get_password_hash(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'id': id_cliente, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'login': login, 'senha': senha}
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])


@bp_cliente.route('/delete', methods=['POST'])
def delete():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()
        print(result)
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])


@bp_cliente.route('/pdf', methods=['GET'])
@validaToken
def generate_pdf():   
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()

        # Create a new PDF document
        pdf = canvas.Canvas("scr\media_files\Relatorio_cliente.pdf")

        # Set the font and font size
        pdf.setFont("Helvetica", 12)

        # Write the text
        pdf.drawString(100, 700, "Relatório de Clientes")
        pdf.drawString(100, 680, "-----------------------------------------")

        # Write the table headers
        pdf.drawString(100, 660, "ID")
        pdf.drawString(200, 660, "Nome")
        pdf.drawString(300, 660, "Matrícula")
        pdf.drawString(400, 660, "CPF")
        pdf.drawString(500, 660, "Telefone")
    
        # Write the data rows
        y = 640  # starting y-coordinate for the first row
        for cliente in result[0]:
            pdf.drawString(100, y, str(cliente['id']))
            pdf.drawString(200, y, cliente['nome'])
            pdf.drawString(300, y, cliente['matricula'])
            pdf.drawString(400, y, cliente['cpf'])
            pdf.drawString(500, y, cliente['telefone'])
            y -= 20  # decrement y-coordinate for the next row

        # Save the PDF document
        pdf.save()

        # Return the PDF file for download
        return send_file("media_files/Relatorio_cliente.pdf", as_attachment=True)
    except Exception as e:
        print(e)
        return render_template('formListacliente.html', msgErro=e.args[0])