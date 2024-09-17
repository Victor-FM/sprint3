import logging
from flask import Flask, request, jsonify, render_template
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Adiciona suporte para CORS, se necessário

# Configurações de logging
logging.basicConfig(level=logging.DEBUG)

# Configurações de conexão com o banco de dados
server = 'srvbancosprint.database.windows.net'
database = 'bancosprint'
username = 'adm'
password = 'A1d3ministrador'
driver = '{ODBC Driver 17 for SQL Server}'

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(conn_str)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET'])
def get_clientes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Clientes')
        rows = cursor.fetchall()
        conn.close()
        clientes = [{'ClienteID': row.ClienteID, 'Nome': row.Nome, 'Email': row.Email, 'DataNascimento': row.DataNascimento.strftime('%Y-%m-%d')} for row in rows]
        return jsonify(clientes)
    except Exception as e:
        logging.error(f"Erro ao obter clientes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clientes', methods=['POST'])
def add_cliente():
    try:
        data = request.json
        nome = data.get('Nome')
        email = data.get('Email')
        data_nascimento = data.get('DataNascimento')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Clientes (Nome, Email, DataNascimento) VALUES (?, ?, ?)', (nome, email, data_nascimento))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente adicionado com sucesso!'}), 201
    except Exception as e:
        logging.error(f"Erro ao adicionar cliente: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    try:
        data = request.json
        nome = data.get('Nome')
        email = data.get('Email')
        data_nascimento = data.get('DataNascimento')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Clientes SET Nome = ?, Email = ?, DataNascimento = ? WHERE ClienteID = ?', (nome, email, data_nascimento, id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente atualizado com sucesso!'})
    except Exception as e:
        logging.error(f"Erro ao atualizar cliente: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Clientes WHERE ClienteID = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cliente excluído com sucesso!'})
    except Exception as e:
        logging.error(f"Erro ao excluir cliente: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
