import flask
import json
import os
import time
from datetime import datetime

# Inicialização da aplicação Flask
app = flask.Flask(__name__)

# Validações de data
def validate_date(data):
    try:
        datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False
    
# Validações de data   
def validate_keys(data):
    array_key =['instruction_id', 'entity_name', 'entity_id', 'timestamp']
    result_key = []
    
    for key in data.keys():
        if key not in array_key:           
            result_key.append({'valid_key': False, 'value_key': key}) 
                
    return result_key

#Função de validação dos campos recebidos do cliente
def validate(data):
    valid = True
    errors = []
    if 'instruction_id' not in data or type(data["instruction_id"]) is not int:
        valid = False
        errors.append('instruction_id is invalid')
    if 'entity_name' not in data or type(data["entity_name"]) is not str:
        valid = False
        errors.append('entity_name is invalid')
    if 'entity_id' not in data or type(data["entity_id"]) is not int: 
        valid = False
        errors.append('entity_id is invalid')
    if type(data["timestamp"]) is not str or validate_date(data['timestamp']) is False:
        valid = False
        errors.append('timestamp is invalid')

    print(errors)
    return {'valid': valid, 'errors': errors}

# Para salvar os arquivos
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
def save_paylod(data):
    create_directory('00_sor')

    dt = datetime.now()
    ts = datetime.timestamp(dt)

    file_payload = open(f"00_sor/payload.json", "a")
    file_payload.write(json.dumps(ts) + ' - ')
    file_payload.write(json.dumps(data) + '\n')
    file_payload.close()

def save_log(data, mensagem):
    create_directory('00_logs')

    dt = datetime.now()
    ts = datetime.timestamp(dt)

    file_payload = open(f"00_logs/log.json", "a")
    file_payload.write(json.dumps(ts) + ' - ')
    file_payload.write(json.dumps(data) + ' ')
    file_payload.write(json.dumps(mensagem) + '\n')
    file_payload.close()      
     
# Definição da rota '/webhook' com suporte a requisições HTTP POST
@app.route('/', methods=["POST"])

def handle_webhook():

    # Recupera o conteúdo da requisição  como um dicionário de python
    data_request = flask.request.get_json()
    data = data_request['body']
    # Trata a requisição recebida: Nesse caso, apenas imprimimos os dados
    print(f'Received data: {data}.')
    
    return_code_error = 847
    
    valid_key = validate_keys(data)   
    if len(valid_key) > 0:
        json_valid_key = json.dumps(valid_key)
        save_log(data, json_valid_key)
        return json_valid_key, return_code_error
    
    result = validate(data)
    if result['valid'] == False:
        save_log(data, result['errors'])
        return f"Invalid Data: {result['errors']}", return_code_error
    
    save_paylod(data)
    
    # retornar uma resposta
    return_code = '200'
    return 'return_code'


# Verifica se o script esta sendo executado como um módulo principal
if __name__ == '__main__':

    # inicia a aplicação
    app.run(host="localhost", port=5001, debug=True)