from flask import Blueprint, render_template, request, redirect, url_for, jsonify,send_file
from reportlab.pdfgen import canvas
import requests
from mod_login.login import validaToken
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO
import os

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''
@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaToken
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])


@bp_funcionario.route('/form-funcionario/', methods=['GET'])
@validaToken
def formFuncionario():

    return render_template('formFuncionario.html')

@bp_funcionario.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = 0
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = int(request.form['grupo'])
        senha = Funcoes.get_password_hash(request.form['senha'])

        # monta o JSON para envio a API
        payload = {
            'id': id_funcionario,
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }

        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code)  # 200

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))

    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
@validaToken
def formEditFuncionario():
    try:
        # ID enviado via FORM
        id_funcionario = request.form['id']
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result)
            # renderiza o form passando os dados retornados

        return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.get_password_hash(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'id': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()
        print(result)
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_funcionario.route('/pdf', methods=['GET'])
@validaToken
def generate_pdf():   
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()
        # Create a new PDF document
        pdf = canvas.Canvas("scr\media_files\Relatorio_funcionario.pdf")

        # Set the font and font size
        pdf.setFont("Helvetica", 12)

        # Write the text
        pdf.drawString(100, 700, "Relatório de Funcionários")
        pdf.drawString(100, 680, "-----------------------------------------")

        # Write the table headers
        pdf.drawString(100, 660, "ID")
        pdf.drawString(200, 660, "Nome")
        pdf.drawString(300, 660, "Matrícula")
        pdf.drawString(400, 660, "CPF")
        pdf.drawString(500, 660, "Telefone")
        pdf.drawString(600, 660, "Grupo")
    
        # Write the data rows
        y = 640  # starting y-coordinate for the first row
        for funcionario in result[0]:
            pdf.drawString(100, y, str(funcionario['id']))
            pdf.drawString(200, y, funcionario['nome'])
            pdf.drawString(300, y, funcionario['matricula'])
            pdf.drawString(400, y, funcionario['cpf'])
            pdf.drawString(500, y, funcionario['telefone'])
            pdf.drawString(600, y, str(funcionario['grupo']))
            y -= 20  # decrement y-coordinate for the next row

        # Save the PDF document
        pdf.save()

        # Return the PDF file for download
        return send_file("media_files/Relatorio_funcionario.pdf", as_attachment=True)
    except Exception as e:
        print(e)
        return render_template('formListaFuncionario.html', msgErro=e.args[0])