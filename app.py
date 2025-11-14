from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Arquivo para armazenar os pacientes
ARQUIVO_PACIENTES = 'pacientes.json'

# Função para carregar pacientes do arquivo
def carregar_pacientes():
    if os.path.exists(ARQUIVO_PACIENTES):
        with open(ARQUIVO_PACIENTES, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

# Função para salvar pacientes no arquivo
def salvar_pacientes(pacientes):
    with open(ARQUIVO_PACIENTES, 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, ensure_ascii=False, indent=4)

# Rota principal - Formulário de cadastro
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastrar paciente
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    telefone = request.form.get('telefone')
    
    # Carregar pacientes existentes
    pacientes = carregar_pacientes()
    
    # Adicionar novo paciente
    novo_paciente = {
        'id': len(pacientes) + 1,
        'nome': nome,
        'idade': idade,
        'telefone': telefone
    }
    
    pacientes.append(novo_paciente)
    
    # Salvar no arquivo
    salvar_pacientes(pacientes)
    
    return redirect(url_for('listar_pacientes'))

# Rota para listar pacientes
@app.route('/pacientes')
def listar_pacientes():
    pacientes = carregar_pacientes()
    return render_template('pacientes.html', pacientes=pacientes)

# Rota para deletar paciente
@app.route('/deletar/<int:paciente_id>')
def deletar(paciente_id):
    pacientes = carregar_pacientes()
    pacientes = [p for p in pacientes if p['id'] != paciente_id]
    salvar_pacientes(pacientes)
    return redirect(url_for('listar_pacientes'))

if __name__ == '__main__':
    app.run(debug=True)