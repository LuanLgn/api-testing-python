import requests
import pytest
from jsonschema import validate

BASE_URL = 'https://jsonplaceholder.typicode.com'

# Schema para validação de contrato de Post
POST_SCHEMA = {
    'type': 'object',
    'properties': {
        'userId': {'type': 'number'},
        'id': {'type': 'number'},
        'title': {'type': 'string'},
        'body': {'type': 'string'}
    },
    'required': ['userId', 'id', 'title', 'body']
}

def test_get_post_com_sucesso():
    # Valida a busca de um post existente (ID 1)
    session = requests.Session()
    session.trust_env = False
    response = session.get(f'{BASE_URL}/posts/1')
    assert response.status_code == 200
    
    dados = response.json()
    validate(instance=dados, schema=POST_SCHEMA)
    assert dados['id'] == 1

def test_post_nao_encontrado():
    # Valida o status 404 para um post inexistente
    session = requests.Session()
    session.trust_env = False
    response = session.get(f'{BASE_URL}/posts/999')
    assert response.status_code == 404

def test_criar_post():
    # Valida a criação de um novo post
    payload = {
        'title': 'QA Automation',
        'body': 'Testando com Python e Pytest',
        'userId': 1
    }
    session = requests.Session()
    session.trust_env = False
    response = session.post(f'{BASE_URL}/posts', json=payload)
    assert response.status_code == 201
    
    dados = response.json()
    assert dados['title'] == payload['title']
    assert dados['userId'] == payload['userId']
    assert 'id' in dados
