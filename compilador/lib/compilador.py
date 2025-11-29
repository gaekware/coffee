#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador Coffee - Classe Principal
Integra todos os componentes: Lexer, Parser, Semantic, Interpreter
"""

import os
import sys
from pathlib import Path

# Imports dos componentes do compilador
from lexer.analisador_lexico import AnalisadorLexico
from parser.parser import Parser
from semantic.analisador_semantico import AnalisadorSemantico
from codegen.gerador_codigo import GeradorCodigo

class CoffeeCompiler:
    """
    Compilador principal da linguagem Coffee
    Coordena todas as fases da compilação
    """
    
    def __init__(self):
        """Inicializa o compilador"""
        self.lexer = AnalisadorLexico()
        self.parser = Parser()
        self.semantic = AnalisadorSemantico()
        self.codegen = GeradorCodigo()
        
    def compile(self, source_code):
        """
        Compila código Coffee
        
        Args:
            source_code (str): Código fonte Coffee
            
        Returns:
            dict: Resultado da compilação com AST e símbolos
        """
        try:
            # Fase 1: Análise Léxica
            print("📝 Fase 1: Análise Léxica...")
            tokens = self.lexer.analisar(source_code)
            print(f"   ✅ {len(tokens)} tokens gerados")
            
            # Fase 2: Análise Sintática
            print("🔍 Fase 2: Análise Sintática...")
            ast = self.parser.parse(tokens)
            print(f"   ✅ AST construída com {len(ast.statements)} statements")
            
            # Fase 3: Análise Semântica
            print("🧠 Fase 3: Análise Semântica...")
            simbolos = self.semantic.analisar(ast)
            print(f"   ✅ {len(simbolos)} símbolos na tabela")
            
            # Fase 4: Geração de Código
            print("⚡ Fase 4: Geração de Código...")
            codigo = self.codegen.gerar(ast)
            print(f"   ✅ Código gerado com sucesso")
            
            return {
                'tokens': tokens,
                'ast': ast,
                'simbolos': simbolos,
                'codigo': codigo,
                'success': True
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def compile_and_run(self, source_code):
        """
        Compila e executa código Coffee
        
        Args:
            source_code (str): Código fonte Coffee
            
        Returns:
            Any: Resultado da execução
        """
        try:
            print("🚀 Iniciando compilação Coffee...")
            
            # Compilar
            result = self.compile(source_code)
            
            if not result['success']:
                raise Exception(result['error'])
            
            # Executar
            print("▶️  Executando código compilado...")
            output = self.codegen.executar(result['codigo'])
            
            print("✅ Compilação e execução concluídas!")
            return output
            
        except Exception as e:
            print(f"❌ Erro na compilação: {e}")
            raise

def main():
    """Função principal para teste"""
    compiler = CoffeeCompiler()
    
    # Código de teste
    test_code = """dados = load("exemplo.csv")
resultado = select dados columns: nome, idade
display resultado"""
    
    print("=== TESTE DO COMPILADOR COFFEE ===")
    print(f"Código: {test_code}")
    
    try:
        result = compiler.compile_and_run(test_code)
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
