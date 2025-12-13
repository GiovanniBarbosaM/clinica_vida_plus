from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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


# ============================
# ROTAS DE INTERFACE WEB (HTML)
# ============================

# Página Inicial
@app.route('/')
def index():
    return render_template('index.html'), 200


# Formulário de cadastro
@app.route('/cadastrar')
def cadastrar_form():
    return render_template('cadastrar.html'), 200


# Página de estatísticas
@app.route('/estatisticas')
def estatisticas():
    try:
        stats = calcular_estatisticas()
        return render_template('estatisticas.html', stats=stats), 200
    except Exception as e:
        flash('Erro ao carregar estatísticas!', 'error')
        return redirect(url_for('index')), 500


# Página de busca e resultado
@app.route('/buscar')
def buscar_pagina():
    termo_busca = request.args.get('q', '').lower()
    
    if not termo_busca:
        return render_template('buscar.html', resultado=None, termo=''), 200
    
    try:
        pacientes = carregar_pacientes()
        resultado = [
            p for p in pacientes 
            if termo_busca in p['nome'].lower() or termo_busca == str(p['id'])
        ]
        return render_template('buscar.html', resultado=resultado, termo=termo_busca), 200
    except Exception as e:
        flash('Erro ao buscar pacientes!', 'error')
        return redirect(url_for('index')), 500


# Listar todos os pacientes (interface web)
@app.route('/pacientes')
def listar_pacientes():
    try:
        pacientes = carregar_pacientes()
        return render_template('pacientes.html', pacientes=pacientes), 200
    except Exception as e:
        flash('Erro ao listar pacientes!', 'error')
        return redirect(url_for('index')), 500


# Formulário de edição
@app.route('/editar/<int:paciente_id>')
def editar_form(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

        if not paciente:
            flash('Paciente não encontrado!', 'error')
            return redirect(url_for('listar_pacientes')), 404

        return render_template('editar.html', paciente=paciente), 200
    except Exception as e:
        flash('Erro ao carregar dados do paciente!', 'error')
        return redirect(url_for('listar_pacientes')), 500


# ============================
# API REST (JSON)
# ============================

# GET - Listar todos os pacientes
@app.route('/api/pacientes', methods=['GET'])
def api_listar_pacientes():
    try:
        pacientes = carregar_pacientes()
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao listar pacientes'}), 500


# GET - Buscar paciente por ID
@app.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
def api_buscar_paciente(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)
        
        if not paciente:
            return jsonify({'erro': 'Paciente não encontrado'}), 404
        
        return jsonify(paciente), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao buscar paciente'}), 500


# GET - Buscar pacientes por nome
@app.route('/api/pacientes/buscar', methods=['GET'])
def api_buscar_por_nome():
    try:
        termo_busca = request.args.get('q', '').lower()
        pacientes = carregar_pacientes()

        resultado = [
            p for p in pacientes 
            if termo_busca in p['nome'].lower()
        ]

        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao buscar pacientes'}), 500


# POST - Criar novo paciente
@app.route('/api/pacientes', methods=['POST'])
def api_criar_paciente():
    try:
        dados = request.get_json()
        
        nome = dados.get('nome')
        idade = dados.get('idade')
        telefone = dados.get('telefone')

        if not nome or not idade or not telefone:
            return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

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

        return jsonify(novo_paciente), 201
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar paciente'}), 500


# PUT - Atualizar paciente
@app.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
def api_atualizar_paciente(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

        if not paciente:
            return jsonify({'erro': 'Paciente não encontrado'}), 404

        dados = request.get_json()
        
        paciente['nome'] = dados.get('nome', paciente['nome'])
        paciente['idade'] = dados.get('idade', paciente['idade'])
        paciente['telefone'] = dados.get('telefone', paciente['telefone'])

        salvar_pacientes(pacientes)

        return jsonify(paciente), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar paciente'}), 500


# DELETE - Deletar paciente
@app.route('/api/pacientes/<int:paciente_id>', methods=['DELETE'])
def api_deletar_paciente(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

        if not paciente:
            return jsonify({'erro': 'Paciente não encontrado'}), 404

        pacientes = [p for p in pacientes if p['id'] != paciente_id]
        salvar_pacientes(pacientes)

        return jsonify({'mensagem': f'Paciente {paciente["nome"]} deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao deletar paciente'}), 500


# ============================
# ROTAS HÍBRIDAS (para formulários HTML)
# ============================

# Processar cadastro via formulário (compatibilidade HTML)
@app.route('/cadastrar/salvar', methods=['POST'])
def cadastrar():
    try:
        nome = request.form.get('nome')
        idade = request.form.get('idade')
        telefone = request.form.get('telefone')

        if not nome or not idade or not telefone:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('cadastrar_form')), 400

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
        return redirect(url_for('listar_pacientes')), 201
    except Exception as e:
        flash('Erro ao cadastrar paciente!', 'error')
        return redirect(url_for('cadastrar_form')), 500





# Processar edição via formulário (compatibilidade HTML)
@app.route('/editar/<int:paciente_id>/salvar', methods=['POST'])
def editar(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

        if not paciente:
            flash('Paciente não encontrado!', 'error')
            return redirect(url_for('listar_pacientes')), 404

        paciente['nome'] = request.form.get('nome')
        paciente['idade'] = request.form.get('idade')
        paciente['telefone'] = request.form.get('telefone')

        salvar_pacientes(pacientes)

        flash(f'Dados de {paciente["nome"]} atualizados!', 'success')
        return redirect(url_for('listar_pacientes')), 200
    except Exception as e:
        flash('Erro ao atualizar paciente!', 'error')
        return redirect(url_for('listar_pacientes')), 500


# Deletar via formulário (compatibilidade HTML)
@app.route('/deletar/<int:paciente_id>/confirmar', methods=['GET', 'POST'])
def deletar(paciente_id):
    try:
        pacientes = carregar_pacientes()
        paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

        if not paciente:
            flash('Paciente não encontrado!', 'error')
            return redirect(url_for('listar_pacientes')), 404

        pacientes = [p for p in pacientes if p['id'] != paciente_id]
        salvar_pacientes(pacientes)

        flash(f'Paciente {paciente["nome"]} foi removido!', 'success')
        return redirect(url_for('listar_pacientes')), 200
    except Exception as e:
        flash('Erro ao deletar paciente!', 'error')
        return redirect(url_for('listar_pacientes')), 500


# ============================
# RUN
# ============================
if __name__ == '__main__':
    app.run(debug=True)