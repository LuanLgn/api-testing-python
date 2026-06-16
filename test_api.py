import requests
import pytest
from jsonschema import validate

BASE_URL = 'https://reqres.in/api'

# Schema para validação de contrato do usuário
USUARIO_SCHEMA = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'id': {'type': 'number'},
                'email': {'type': 'string'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'},
                'avatar': {'type': 'string'}
            },
            'required': ['id', 'email', 'first_name', 'last_name']
        }
    },
    'required': ['data']
}

def test_get_usuario_com_sucesso():
    ''Valida a busca de um usuário existente (ID 2)''
    response = requests.get(f'{BASE_URL}/users/2')
    assert response.status_code == 200
    
    dados = response.json()
    validate(instance=dados, schema=USUARIO_SCHEMA)
    assert dados['data']['id'] == 2

def test_usuario_nao_encontrado():
    ''Valida o status 404 para um usuário inexistente''
    response = requests.get(f'{BASE_URL}/users/23')
    assert response.status_code == 404

def test_criar_usuario():
    ''Valida a criação de um novo usuário''
    payload = {
        'name': 'Luan Tolosa',
        'job': 'QA Automation Engineer'
    }
    response = requests.post(f'{BASE_URL}/users', json=payload)
    assert response.status_code == 201
    
    dados = response.json()
    assert dados['name'] == payload['name']
    assert dados['job'] == payload['job']
    assert 'id' in dados
