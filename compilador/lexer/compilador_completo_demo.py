"""
DEMONSTRAÇÃO DE INTEGRAÇÃO COMPLETA - COMPILADOR COFFEE
=====================================================

Este arquivo demonstra o funcionamento integrado de todas as fases
do compilador Coffee: Lexer → Parser → Semantic Analyzer → Interpreter

Execução: python compilador_completo_demo.py
"""

import sys
import os
import time
from typing import Dict, Any

# Importa todos os componentes do compilador
sys.path.append(os.path.dirname(__file__))
from parser import DFA, DFA_TRANSITIONS, DFA_ACCEPTING_STATES, Lexer, Parser
from semantic_analyzer import SemanticAnalyzer
from coffee_interpreter import CoffeeInterpreter

class CompiladorCompleto:
    """Demonstração do compilador completo funcionando end-to-end"""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.stats = {
            'tempo_lexer': 0,
            'tempo_parser': 0, 
            'tempo_semantico': 0,
            'tempo_interpretador': 0,
            'tokens_gerados': 0,
            'nos_ast': 0,
            'variaveis_criadas': 0,
            'operacoes_executadas': 0
        }
    
    def compilar_e_executar(self, codigo_fonte: str, nome_programa: str = "programa") -> Dict[str, Any]:
        """
        Executa todo o pipeline de compilação:
        Código → Tokens → AST → Verificação → Execução → Resultado
        """
        
        if self.debug:
            print("="*80)
            print(f"COMPILADOR COFFEE - EXECUÇÃO COMPLETA: {nome_programa}")
            print("="*80)
            print(f"Código fonte ({len(codigo_fonte)} caracteres):")
            print("-" * 50)
            print(codigo_fonte)
            print("-" * 50)
        
        resultado = {
            'sucesso_geral': False,
            'fase_atual': 'inicio',
            'tempo_total': 0,
            'estatisticas': {},
            'resultado_execucao': None,
            'erros': []
        }
        
        tempo_inicio = time.time()
        
        try:
            # FASE 1: ANÁLISE LÉXICA
            if self.debug:
                print("\n1️⃣  FASE: ANÁLISE LÉXICA")
                print("   Tokenizando código fonte...")
            
            inicio_lexer = time.time()
            coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
            lexer = Lexer(codigo_fonte, coffee_dfa)
            
            # Conta tokens gerados
            tokens = []
            while True:
                token = lexer.next_token()
                tokens.append(token)
                if token.type == 'EOF':
                    break
            
            self.stats['tokens_gerados'] = len(tokens) - 1  # -1 para EOF
            self.stats['tempo_lexer'] = time.time() - inicio_lexer
            
            if self.debug:
                print(f"   ✅ {self.stats['tokens_gerados']} tokens gerados em {self.stats['tempo_lexer']:.4f}s")
                print(f"   Tokens: {[f'{t.type}({t.value})' for t in tokens[:5]]}...")
            
            resultado['fase_atual'] = 'lexer_completo'
            
            # FASE 2: ANÁLISE SINTÁTICA
            if self.debug:
                print("\n2️⃣  FASE: ANÁLISE SINTÁTICA")
                print("   Construindo Árvore Sintática Abstrata...")
            
            inicio_parser = time.time()
            # Recria lexer para parsing (reset)
            lexer = Lexer(codigo_fonte, coffee_dfa)
            parser = Parser(lexer)
            ast = parser.parse()
            
            self.stats['tempo_parser'] = time.time() - inicio_parser
            self.stats['nos_ast'] = self._contar_nos_ast(ast)
            
            if self.debug:
                print(f"   ✅ AST criada com {self.stats['nos_ast']} nós em {self.stats['tempo_parser']:.4f}s")
                print(f"   Estrutura: {type(ast).__name__} com {len(ast.statements)} statements")
            
            resultado['fase_atual'] = 'parser_completo'
            
            # FASE 3: ANÁLISE SEMÂNTICA
            if self.debug:
                print("\n3️⃣  FASE: ANÁLISE SEMÂNTICA")
                print("   Verificando tipos, escopo e semântica...")
            
            inicio_semantico = time.time()
            analyzer = SemanticAnalyzer(debug=False)
            semantico_sucesso, erros_semanticos, info_semantica = analyzer.analyze(ast)
            
            self.stats['tempo_semantico'] = time.time() - inicio_semantico
            
            if not semantico_sucesso:
                if self.debug:
                    print(f"   ❌ Erros semânticos encontrados:")
                    for erro in erros_semanticos:
                        print(f"      • {erro}")
                
                resultado['erros'] = [str(e) for e in erros_semanticos]
                resultado['fase_atual'] = 'semantico_falhou'
                return resultado
            
            self.stats['variaveis_criadas'] = len(info_semantica['symbol_table'])
            
            if self.debug:
                print(f"   ✅ Verificação completa em {self.stats['tempo_semantico']:.4f}s")
                print(f"   Símbolos: {list(info_semantica['symbol_table'].keys())}")
            
            resultado['fase_atual'] = 'semantico_completo'
            
            # FASE 4: EXECUÇÃO (INTERPRETADOR)
            if self.debug:
                print("\n4️⃣  FASE: EXECUÇÃO/INTERPRETAÇÃO")
                print("   Executando programa...")
            
            inicio_interpretador = time.time()
            interpreter = CoffeeInterpreter(debug=False)
            resultado_execucao = interpreter.interpret(ast)
            
            self.stats['tempo_interpretador'] = time.time() - inicio_interpretador
            self.stats['operacoes_executadas'] = resultado_execucao['statistics']['operations_executed']
            
            if not resultado_execucao['success']:
                if self.debug:
                    print(f"   ❌ Erro durante execução: {resultado_execucao['error']}")
                
                resultado['erros'] = [resultado_execucao['error']]
                resultado['fase_atual'] = 'execucao_falhou'
                return resultado
            
            if self.debug:
                print(f"   ✅ Execução completa em {self.stats['tempo_interpretador']:.4f}s")
                print(f"   Operações: {self.stats['operacoes_executadas']} executadas")
            
            # SUCESSO TOTAL
            tempo_total = time.time() - tempo_inicio
            self.stats['tempo_total'] = tempo_total
            
            resultado.update({
                'sucesso_geral': True,
                'fase_atual': 'completo',
                'tempo_total': tempo_total,
                'estatisticas': self.stats.copy(),
                'resultado_execucao': resultado_execucao,
                'info_semantica': info_semantica
            })
            
            if self.debug:
                self._imprimir_resumo_final(resultado)
            
            return resultado
            
        except Exception as e:
            if self.debug:
                print(f"\n❌ ERRO NA FASE {resultado['fase_atual']}: {e}")
            
            resultado['erros'] = [str(e)]
            return resultado
    
    def _contar_nos_ast(self, node) -> int:
        """Conta recursivamente os nós da AST"""
        count = 1
        
        # Conta nós filhos baseado no tipo
        if hasattr(node, 'statements'):  # ProgramNode
            for stmt in node.statements:
                count += self._contar_nos_ast(stmt)
        elif hasattr(node, 'expression'):  # AssignmentStatementNode
            count += self._contar_nos_ast(node.expression)
        elif hasattr(node, 'condition'):  # FilterExpressionNode
            count += self._contar_nos_ast(node.condition)
        elif hasattr(node, 'left') and hasattr(node, 'right'):  # RelationalExpressionNode
            count += self._contar_nos_ast(node.left)
            count += self._contar_nos_ast(node.right)
        
        return count
    
    def _imprimir_resumo_final(self, resultado: Dict[str, Any]):
        """Imprime resumo detalhado da execução"""
        stats = resultado['estatisticas']
        
        print("\n" + "="*80)
        print("🎉 COMPILAÇÃO E EXECUÇÃO BEM-SUCEDIDAS!")
        print("="*80)
        
        print("📊 ESTATÍSTICAS DETALHADAS:")
        print(f"   ⏱️  Tempo Total: {stats['tempo_total']:.4f}s")
        print(f"   🔤 Análise Léxica: {stats['tempo_lexer']:.4f}s ({stats['tokens_gerados']} tokens)")
        print(f"   🌳 Análise Sintática: {stats['tempo_parser']:.4f}s ({stats['nos_ast']} nós AST)")
        print(f"   🔍 Análise Semântica: {stats['tempo_semantico']:.4f}s ({stats['variaveis_criadas']} variáveis)")
        print(f"   ⚡ Execução: {stats['tempo_interpretador']:.4f}s ({stats['operacoes_executadas']} operações)")
        
        # Distribução de tempo
        tempo_total = stats['tempo_total']
        print(f"\n📈 DISTRIBUIÇÃO DE TEMPO:")
        print(f"   Lexer:       {stats['tempo_lexer']/tempo_total*100:.1f}%")
        print(f"   Parser:      {stats['tempo_parser']/tempo_total*100:.1f}%") 
        print(f"   Semântico:   {stats['tempo_semantico']/tempo_total*100:.1f}%")
        print(f"   Execução:    {stats['tempo_interpretador']/tempo_total*100:.1f}%")
        
        # Performance
        operacoes_por_segundo = stats['operacoes_executadas'] / stats['tempo_interpretador']
        print(f"\n⚡ PERFORMANCE:")
        print(f"   Operações/segundo: {operacoes_por_segundo:.0f}")
        print(f"   Throughput: {stats['tokens_gerados']/tempo_total:.0f} tokens/s")
        
        print("\n✅ COMPILADOR COFFEE FUNCIONANDO PERFEITAMENTE!")
        print("="*80)

def demonstrar_compilador_completo():
    """Função principal de demonstração"""
    
    print("DEMONSTRAÇÃO: COMPILADOR COFFEE COMPLETO")
    print("="*80)
    print("Este programa demonstra todas as fases do compilador funcionando em conjunto.")
    print()
    
    compilador = CompiladorCompleto(debug=True)
    
    # Programa de exemplo complexo
    programa_exemplo = """
# Análise completa de vendas e clientes
vendas_2025 = load "vendas_primeiro_trimestre.csv"
clientes_vip = load "base_clientes_premium.json"

# Filtrar vendas significativas  
vendas_altas = filter vendas_2025 where total >= 1000
vendas_notebooks = filter vendas_altas where produto == "Notebook"

# Análise de clientes
clientes_jovens = filter clientes_vip where idade < 35
clientes_sp = filter clientes_jovens where cidade == "São Paulo"

# Relatórios finais
relatorio_vendas = select vendas_notebooks (produto, quantidade, total, vendedor)
relatorio_clientes = select clientes_sp (nome, email, idade)

# Exibir resultados
display relatorio_vendas
display relatorio_clientes
"""
    
    # Executa compilação completa
    resultado = compilador.compilar_e_executar(programa_exemplo, "DemoCompleta")
    
    # Resultado final
    if resultado['sucesso_geral']:
        print("\n🎊 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("   Todas as fases do compilador funcionaram perfeitamente.")
        print("   O sistema está pronto para uso em produção acadêmica.")
    else:
        print(f"\n💥 DEMONSTRAÇÃO FALHOU NA FASE: {resultado['fase_atual']}")
        print(f"   Erros: {resultado['erros']}")
    
    return resultado['sucesso_geral']

if __name__ == '__main__':
    sucesso = demonstrar_compilador_completo()
    sys.exit(0 if sucesso else 1)