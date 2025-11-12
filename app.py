from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de pacientes armazenada em memória
pacientes = []


@app.route('/')
def index():
    # Página inicial (formulário de cadastro)
    return render_template('index.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = int(request.form['idade'])
        telefone = request.form['telefone']

        paciente = {'nome': nome, 'idade': idade, 'telefone': telefone}
        pacientes.append(paciente)

        # ✅ Redireciona para a lista de pacientes
        return redirect(url_for('listar'))

    return redirect(url_for('index'))


@app.route('/pacientes')
def listar():
    total = len(pacientes)
    idade_media = sum(p['idade'] for p in pacientes) / total if total > 0 else 0
    mais_velho = max(pacientes, key=lambda x: x['idade']) if pacientes else None

    return render_template(
        'lista.html',
        pacientes=pacientes,
        total=total,
        idade_media=round(idade_media, 1),
        mais_velho=mais_velho
    )


if __name__ == '__main__':
    app.run(debug=True)
