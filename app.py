from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_123'  # Necessário para usar flash messages

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

# Função para calcular estatísticas
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

# ROTA 1: Página Principal com Menu
@app.route('/')
def index():
    return render_template('index.html')

# ROTA 2: Formulário de Cadastro
@app.route('/cadastrar-form')
def cadastrar_form():
    return render_template('cadastrar.html')

# ROTA 3: Processar Cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    idade = request.form.get('idade')
    telefone = request.form.get('telefone')
    
    # Validação básica
    if not nome or not idade or not telefone:
        flash('Todos os campos são obrigatórios!', 'error')
        return redirect(url_for('cadastrar_form'))
    
    # Carregar pacientes existentes
    pacientes = carregar_pacientes()
    
    # Adicionar novo paciente
    novo_paciente = {
        'id': len(pacientes) + 1,
        'nome': nome,
        'idade': idade,
        'telefone': telefone,
        'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    
    pacientes.append(novo_paciente)
    
    # Salvar no arquivo
    salvar_pacientes(pacientes)
    
    flash(f'Paciente {nome} cadastrado com sucesso!', 'success')
    return redirect(url_for('listar_pacientes'))

# ROTA 4: Ver Estatísticas
@app.route('/estatisticas')
def estatisticas():
    stats = calcular_estatisticas()
    return render_template('estatisticas.html', stats=stats)

# ROTA 5: Buscar Paciente
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    resultado = None
    termo_busca = ''
    
    if request.method == 'POST':
        termo_busca = request.form.get('busca', '').lower()
        pacientes = carregar_pacientes()
        
        # Buscar por nome ou ID
        resultado = [
            p for p in pacientes 
            if termo_busca in p['nome'].lower() or termo_busca == str(p['id'])
        ]
    
    return render_template('buscar.html', resultado=resultado, termo=termo_busca)

# ROTA 6: Listar todos os pacientes
@app.route('/pacientes')
def listar_pacientes():
    pacientes = carregar_pacientes()
    return render_template('pacientes.html', pacientes=pacientes)

# ROTA 7: Deletar paciente
@app.route('/deletar/<int:paciente_id>')
def deletar(paciente_id):
    pacientes = carregar_pacientes()
    paciente_deletado = None
    
    # Encontrar o nome do paciente antes de deletar
    for p in pacientes:
        if p['id'] == paciente_id:
            paciente_deletado = p['nome']
            break
    
    # Deletar
    pacientes = [p for p in pacientes if p['id'] != paciente_id]
    salvar_pacientes(pacientes)
    
    if paciente_deletado:
        flash(f'Paciente {paciente_deletado} foi removido!', 'success')
    
    return redirect(url_for('listar_pacientes'))

# ROTA 8: Editar paciente
@app.route('/editar/<int:paciente_id>', methods=['GET', 'POST'])
def editar(paciente_id):
    pacientes = carregar_pacientes()
    paciente = None
    
    # Encontrar o paciente
    for p in pacientes:
        if p['id'] == paciente_id:
            paciente = p
            break
    
    if not paciente:
        flash('Paciente não encontrado!', 'error')
        return redirect(url_for('listar_pacientes'))
    
    if request.method == 'POST':
        # Atualizar dados
        paciente['nome'] = request.form.get('nome')
        paciente['idade'] = request.form.get('idade')
        paciente['telefone'] = request.form.get('telefone')
        
        salvar_pacientes(pacientes)
        flash(f'Dados de {paciente["nome"]} atualizados!', 'success')
        return redirect(url_for('listar_pacientes'))
    
    return render_template('editar.html', paciente=paciente)

if __name__ == '__main__':
    app.run(debug=True)