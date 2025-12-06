from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_123'

ARQUIVO_PACIENTES = 'pacientes.json'

# ============================
# FUNÇÕES AUXILIARES
# ============================
def carregar_pacientes():
    if os.path.exists(ARQUIVO_PACIENTES):
        with open(ARQUIVO_PACIENTES, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def salvar_pacientes(pacientes):
    with open(ARQUIVO_PACIENTES, 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, ensure_ascii=False, indent=4)

def calcular_estatisticas():
    pacientes = carregar_pacientes()
    
    if not pacientes:
        return {
            'total': 0,
            'media_idade': 0,
            'mais_jovem': None,
            'mais_velho': None
        }
    
    idades = [int(p['idade']) for p in pacientes]
    
    return {
        'total': len(pacientes),
        'media_idade': round(sum(idades) / len(idades), 1),
        'mais_jovem': min(idades),
        'mais_velho': max(idades)
    }


# ROTAS (SEPARADAS!)

#Página Inicial
@app.route('/')
def index():
    return render_template('index.html')


#Formulário de cadastro
@app.route('/cadastrar-form', methods=['GET'])
def cadastrar_form():
    return render_template('cadastrar.html')


#Processar cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    telefone = request.form.get('telefone')

    if not nome or not idade or not telefone:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('cadastrar_form'))

    pacientes = carregar_pacientes()

    novo_paciente = {
        'id': len(pacientes) + 1,
        'nome': nome,
        'idade': idade,
        'telefone': telefone,
        'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M')
    }

    pacientes.append(novo_paciente)
    salvar_pacientes(pacientes)

    flash(f'Paciente {nome} cadastrado com sucesso!', 'success')
    return redirect(url_for('listar_pacientes'))


#Página de estatísticas
@app.route('/estatisticas')
def estatisticas():
    stats = calcular_estatisticas()
    return render_template('estatisticas.html', stats=stats)


#Exibir página de busca
@app.route('/buscar', methods=['GET'])
def buscar_get():
    return render_template('buscar.html', resultado=None, termo='')


#Processar busca 
@app.route('/buscar', methods=['POST'])
def buscar_post():
    termo_busca = request.form.get('busca', '').lower()
    pacientes = carregar_pacientes()

    resultado = [
        p for p in pacientes 
        if termo_busca in p['nome'].lower() or termo_busca == str(p['id'])
    ]

    return render_template('buscar.html', resultado=resultado, termo=termo_busca)


#Listar todos
@app.route('/pacientes')
def listar_pacientes():
    pacientes = carregar_pacientes()
    return render_template('pacientes.html', pacientes=pacientes)


#Deletar paciente
@app.route('/deletar/<int:paciente_id>')
def deletar(paciente_id):
    pacientes = carregar_pacientes()
    paciente_deletado = None

    for p in pacientes:
        if p['id'] == paciente_id:
            paciente_deletado = p['nome']
            break

    pacientes = [p for p in pacientes if p['id'] != paciente_id]
    salvar_pacientes(pacientes)

    if paciente_deletado:
        flash(f'Paciente {paciente_deletado} foi removido!', 'success')

    return redirect(url_for('listar_pacientes'))


#Formulário de edição
@app.route('/editar/<int:paciente_id>', methods=['GET'])
def editar_get(paciente_id):
    pacientes = carregar_pacientes()
    paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

    if not paciente:
        flash('Paciente não encontrado!', 'error')
        return redirect(url_for('listar_pacientes'))

    return render_template('editar.html', paciente=paciente)


#Processar edição 
@app.route('/editar/<int:paciente_id>', methods=['POST'])
def editar_post(paciente_id):
    pacientes = carregar_pacientes()
    paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

    if not paciente:
        flash('Paciente não encontrado!', 'error')
        return redirect(url_for('listar_pacientes'))

    paciente['nome'] = request.form.get('nome')
    paciente['idade'] = request.form.get('idade')
    paciente['telefone'] = request.form.get('telefone')

    salvar_pacientes(pacientes)

    flash(f'Dados de {paciente["nome"]} atualizados!', 'success')
    return redirect(url_for('listar_pacientes'))


# RUN
if __name__ == '__main__':
    app.run(debug=True)
