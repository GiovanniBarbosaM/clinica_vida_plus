# API de Cadastro de Pacientes – Flask

Este projeto é uma **API simples com interface HTML** desenvolvida em **Flask**, utilizada para **cadastrar, listar, editar, excluir e buscar pacientes**, além de **gerar estatísticas básicas**.

Os dados são armazenados localmente em um arquivo **JSON**, sendo ideal para fins **educacionais**, **prototipação** e **aprendizado de CRUD, Flask e MVC simplificado**.

---

## Funcionalidades

* ✅ Cadastro de pacientes
* 📋 Listagem de pacientes
* ✏️ Edição de dados do paciente
* ❌ Exclusão de paciente
* 🔍 Busca por nome ou ID
* 📊 Estatísticas:

  * Total de pacientes
  * Média de idade
  * Paciente mais jovem
  * Paciente mais velho
* 💾 Persistência de dados em arquivo JSON
* 🌐 Interface HTML integrada

---

## Tecnologias Utilizadas

* Python 3.x
* Flask
* HTML + Jinja2
* JSON (armazenamento de dados)

---

## Estrutura do Projeto

```text
project/
│
├── app.py                 # Arquivo principal da aplicação
├── pacientes.json         # Banco de dados em JSON (gerado automaticamente)
│
├── templates/
│   ├── index.html
│   ├── cadastrar.html
│   ├── pacientes.html
│   ├── editar.html
│   ├── buscar.html
│   └── estatisticas.html
│
└── static/ (opcional)
```

---

## ▶️ Como Executar o Projeto

### 1️⃣ Criar ambiente virtual (opcional, recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2️⃣ Instalar dependências

```bash
pip install flask
```

### 3️ Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Rotas da Aplicação

### Rotas HTML

| Rota            | Método | Descrição              |
| --------------- | ------ | ---------------------- |
| `/`             | GET    | Página inicial         |
| `/cadastrar`    | GET    | Formulário de cadastro |
| `/pacientes`    | GET    | Listagem de pacientes  |
| `/editar/<id>`  | GET    | Formulário de edição   |
| `/buscar`       | GET    | Busca por nome ou ID   |
| `/estatisticas` | GET    | Estatísticas gerais    |

---

### Rotas de Ação (POST)

| Rota                      | Método     | Função               |
| ------------------------- | ---------- | -------------------- |
| `/cadastrar/salvar`       | POST       | Salvar novo paciente |
| `/editar/<id>/salvar`     | POST       | Atualizar paciente   |
| `/deletar/<id>/confirmar` | GET / POST | Remover paciente     |

---

## 📦 Estrutura do Paciente (JSON)

```json
{
  "id": 1,
  "nome": "João Silva",
  "idade": "30",
  "telefone": "11999999999",
  "data_cadastro": "14/12/2025 10:30"
}
```

---

## Conceitos Aplicados

* CRUD (Create, Read, Update, Delete)
* Separação de responsabilidades
* Manipulação de arquivos JSON
* Rotas Flask
* Validação de formulários
* Flash messages
* MVC simplificado

---


## 📌 Próximos Passos 

* 🔐 Autenticação e login
* 🗄️ Migrar JSON para banco de dados (SQLite / PostgreSQL)
* 🌍 Criar versão REST (JSON puro)
* 🎨 Melhorar UI com Bootstrap ou Tailwind
* 📱 Tornar responsivo

---

## Autor

Desenvolvido por **Giovanni**

Projeto educacional para estudo de **Flask, APIs e CRUD**.

---
