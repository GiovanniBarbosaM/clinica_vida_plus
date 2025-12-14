from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

ARQUIVO_PACIENTES = 'pacientes.json'

#  FUNÇÕES AUXILIARES 

def carregar_pacientes():
    if os.path.exists(ARQUIVO_PACIENTES):
        with open(ARQUIVO_PACIENTES, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def salvar_pacientes(pacientes):
    with open(ARQUIVO_PACIENTES, 'w', encoding='utf-8') as arquivo:
        json.dump(pacientes, arquivo, ensure_ascii=False, indent=4)

def gerar_novo_id(pacientes):
    return max([p['id'] for p in pacientes], default=0) + 1

#  CREATE 

@app.route('/api/pacientes', methods=['POST'])
def criar_paciente():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400

    nome = dados.get('nome')
    idade = dados.get('idade')
    telefone = dados.get('telefone')

    if not nome or not idade or not telefone:
        return jsonify({"erro": "Campos obrigatórios"}), 400

    pacientes = carregar_pacientes()

    novo_paciente = {
        "id": gerar_novo_id(pacientes),
        "nome": nome,
        "idade": idade,
        "telefone": telefone,
        "data_cadastro": datetime.now().strftime('%d/%m/%Y %H:%M')
    }

    pacientes.append(novo_paciente)
    salvar_pacientes(pacientes)

    return jsonify(novo_paciente), 201

#  READ 

@app.route('/api/pacientes', methods=['GET'])
def listar_pacientes():
    return jsonify(carregar_pacientes()), 200

@app.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
def buscar_paciente(paciente_id):
    pacientes = carregar_pacientes()
    paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404

    return jsonify(paciente), 200

# = UPDATE 

@app.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
def atualizar_paciente(paciente_id):
    dados = request.get_json()
    pacientes = carregar_pacientes()

    paciente = next((p for p in pacientes if p['id'] == paciente_id), None)
    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404

    paciente['nome'] = dados.get('nome', paciente['nome'])
    paciente['idade'] = dados.get('idade', paciente['idade'])
    paciente['telefone'] = dados.get('telefone', paciente['telefone'])

    salvar_pacientes(pacientes)
    return jsonify(paciente), 200

#  DELETE 

@app.route('/api/pacientes/<int:paciente_id>', methods=['DELETE'])
def deletar_paciente(paciente_id):
    pacientes = carregar_pacientes()
    paciente = next((p for p in pacientes if p['id'] == paciente_id), None)

    if not paciente:
        return jsonify({"erro": "Paciente não encontrado"}), 404

    pacientes = [p for p in pacientes if p['id'] != paciente_id]
    salvar_pacientes(pacientes)

    return '', 204

#  EXECUÇÃO 

if __name__ == '__main__':
    app.run(debug=True)
