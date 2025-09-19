
import pytest
from lib.lexer.afds.afd_numero import AfdNumero
from lib.lexer.token import TokenType


@pytest.fixture
def afd_numero():
    return AfdNumero()

def test_reconhece_inteiro_simples(afd_numero):
    
    source = "123"
    token = afd_numero.process(source, 0)
    assert token is not None
    assert token.type == TokenType.NUMBER
    assert token.lexeme == "123"

def test_reconhece_ponto_flutuante(afd_numero):
    
    source = "50.75"
    token = afd_numero.process(source, 0)
    assert token is not None
    assert token.lexeme == "50.75"

def test_para_em_caractere_invalido(afd_numero):
    
    source = "100;"
    token = afd_numero.process(source, 0)
    assert token is not None
    assert token.lexeme == "100"

def test_falha_em_numero_mal_formado(afd_numero):
    
    source = "1.2.3"
    token = afd_numero.process(source, 0)
    assert token is not None
    
    assert token.lexeme == "1.2"

def test_falha_se_comecar_com_ponto(afd_numero):
    
    source = ".25"
    token = afd_numero.process(source, 0)
    assert token is None

def test_reconhece_inteiro_antes_de_ponto_sozinho(afd_numero):
    
    source = "42."
    token = afd_numero.process(source, 0)
    assert token is not None
    assert token.lexeme == "42"