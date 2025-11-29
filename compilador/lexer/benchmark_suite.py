"""
Suite de testes para medir performance e validar correção
do interpretador Coffee. Inclui programas de teste e comparações
com implementações equivalentes.
"""

import time
import sys
import os
import pandas as pd
from typing import Dict, List, Tuple, Any

# Importa o interpretador
sys.path.append(os.path.dirname(__file__))
from coffee_interpreter import *

class BenchmarkSuite:
    """Suite de benchmarks para o interpretador Coffee"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.test_programs = {
            'basic_operations': self._basic_operations_program(),
            'complex_filtering': self._complex_filtering_program(),
            'multiple_selects': self._multiple_selects_program(),
            'large_dataset': self._large_dataset_program()
        }
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Executa todos os benchmarks e retorna resultados"""
        print("="*60)
        print("EXECUTANDO SUITE DE BENCHMARKS COFFEE")
        print("="*60)
        
        for name, program in self.test_programs.items():
            print(f"\nBenchmark: {name}")
            print("-" * 40)
            
            result = self._run_benchmark(name, program)
            self.results.append(result)
            
            print(f"Tempo de execução: {result['execution_time']:.4f}s")
            print(f"Status: {'✓ SUCESSO' if result['success'] else '✗ FALHA'}")
            
            if not result['success']:
                print(f"Erro: {result['error']}")
        
        return self._generate_report()
    
    def _run_benchmark(self, name: str, program: str) -> Dict[str, Any]:
        """Executa um benchmark individual"""
        try:
            # Parse do programa
            coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
            lexer = Lexer(program, coffee_dfa)
            parser = Parser(lexer)
            ast = parser.parse()
            
            # Análise semântica
            analyzer = SemanticAnalyzer(debug=False)
            semantic_success, errors, _ = analyzer.analyze(ast)
            
            if not semantic_success:
                return {
                    'name': name,
                    'success': False,
                    'error': f"Erros semânticos: {[str(e) for e in errors]}",
                    'execution_time': 0
                }
            
            # Medição de tempo de execução
            start_time = time.time()
            
            interpreter = CoffeeInterpreter(debug=False)
            result = interpreter.interpret(ast)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            return {
                'name': name,
                'success': result['success'],
                'error': result.get('error', ''),
                'execution_time': execution_time,
                'statistics': result['statistics'],
                'environment': result.get('environment', {})
            }
            
        except Exception as e:
            return {
                'name': name,
                'success': False,
                'error': str(e),
                'execution_time': 0
            }
    
    def _basic_operations_program(self) -> str:
        """Programa básico com operações fundamentais"""
        return '''
dados = load "vendas.csv"
filtrados = filter dados where preco > 100
resultado = select filtrados (produto, preco)
display resultado
'''
    
    def _complex_filtering_program(self) -> str:
        """Programa com filtragem mais complexa"""
        return '''
vendas = load "vendas_grandes.csv"
vendas_altas = filter vendas where total >= 500
vendas_notebook = filter vendas_altas where produto == "Notebook"
relatorio = select vendas_notebook (produto, quantidade, total, vendedor)
display relatorio
'''
    
    def _multiple_selects_program(self) -> str:
        """Programa com múltiplas seleções"""
        return '''
dados1 = load "clientes.csv"
dados2 = load "produtos.csv"
clientes_jovens = filter dados1 where idade < 30
produtos_ativos = filter dados2 where status == "ativo"
contatos = select clientes_jovens (nome, email)
catalogo = select produtos_ativos (nome, preco)
display contatos
display catalogo
'''
    
    def _large_dataset_program(self) -> str:
        """Programa simulando dataset grande"""
        return '''
base_dados = load "dataset_grande.csv"
filtro1 = filter base_dados where valor > 1000
filtro2 = filter filtro1 where ativo == "sim"
final = select filtro2 (id, nome, valor)
display final
'''
    
    def _generate_report(self) -> Dict[str, Any]:
        """Gera relatório consolidado dos benchmarks"""
        successful_tests = [r for r in self.results if r['success']]
        failed_tests = [r for r in self.results if not r['success']]
        
        total_time = sum(r['execution_time'] for r in successful_tests)
        avg_time = total_time / len(successful_tests) if successful_tests else 0
        
        report = {
            'total_tests': len(self.results),
            'successful': len(successful_tests),
            'failed': len(failed_tests),
            'total_execution_time': total_time,
            'average_execution_time': avg_time,
            'results': self.results
        }
        
        self._print_summary_report(report)
        return report
    
    def _print_summary_report(self, report: Dict[str, Any]):
        """Imprime relatório resumido"""
        print("\n" + "="*60)
        print("RELATÓRIO DE BENCHMARKS")
        print("="*60)
        
        print(f"Total de testes: {report['total_tests']}")
        print(f"Sucessos: {report['successful']}")
        print(f"Falhas: {report['failed']}")
        print(f"Taxa de sucesso: {report['successful']/report['total_tests']*100:.1f}%")
        
        if report['successful'] > 0:
            print(f"Tempo total de execução: {report['total_execution_time']:.4f}s")
            print(f"Tempo médio por teste: {report['average_execution_time']:.4f}s")
        
        print("\nDetalhes por teste:")
        for result in report['results']:
            status = "✓" if result['success'] else "✗"
            time_str = f"{result['execution_time']:.4f}s" if result['success'] else "N/A"
            print(f"  {status} {result['name']}: {time_str}")
            
            if result['success'] and 'statistics' in result:
                stats = result['statistics']
                print(f"    → Datasets: {stats.get('datasets_loaded', 0)}, "
                      f"Operações: {stats.get('operations_executed', 0)}, "
                      f"Displays: {stats.get('displays_performed', 0)}")

class PerformanceComparator:
    """Compara performance Coffee vs implementações equivalentes"""
    
    def __init__(self):
        self.comparison_results = []
    
    def compare_with_python_pandas(self, iterations: int = 100) -> Dict[str, Any]:
        """Compara operações Coffee com pandas puro"""
        print("\n" + "="*60)
        print("COMPARAÇÃO DE PERFORMANCE: Coffee vs Python+Pandas")
        print("="*60)
        
        # Operação Coffee
        coffee_program = '''
dados = load "vendas.csv"
filtrados = filter dados where preco > 100
resultado = select filtrados (produto, preco)
'''
        
        coffee_times = []
        pandas_times = []
        
        for i in range(iterations):
            # Tempo Coffee
            start = time.time()
            try:
                coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
                lexer = Lexer(coffee_program, coffee_dfa)
                parser = Parser(lexer)
                ast = parser.parse()
                
                analyzer = SemanticAnalyzer(debug=False)
                analyzer.analyze(ast)
                
                interpreter = CoffeeInterpreter(debug=False)
                interpreter.interpret(ast)
                
                coffee_times.append(time.time() - start)
            except:
                pass
            
            # Tempo pandas equivalente
            start = time.time()
            try:
                # Simula operação equivalente
                df = DatasetOperations.load_csv('"vendas.csv"')
                filtered = df[df['preco'] > 100]
                result = filtered[['produto', 'preco']]
                
                pandas_times.append(time.time() - start)
            except:
                pass
        
        coffee_avg = sum(coffee_times) / len(coffee_times) if coffee_times else 0
        pandas_avg = sum(pandas_times) / len(pandas_times) if pandas_times else 0
        
        speedup = pandas_avg / coffee_avg if coffee_avg > 0 else 0
        
        print(f"Iterações: {iterations}")
        print(f"Coffee (média): {coffee_avg:.6f}s")
        print(f"Pandas (média): {pandas_avg:.6f}s")
        print(f"Overhead Coffee: {speedup:.2f}x" if speedup >= 1 else f"Speedup Coffee: {1/speedup:.2f}x")
        
        return {
            'iterations': iterations,
            'coffee_avg_time': coffee_avg,
            'pandas_avg_time': pandas_avg,
            'overhead_factor': speedup,
            'coffee_times': coffee_times,
            'pandas_times': pandas_times
        }

def run_correctness_tests() -> bool:
    """Executa testes de correção para validar o interpretador"""
    print("="*60)
    print("TESTES DE CORREÇÃO")
    print("="*60)
    
    tests = [
        {
            'name': 'Teste Básico de Load',
            'program': 'dados = load "test.csv"\ndisplay dados',
            'expected_vars': ['dados']
        },
        {
            'name': 'Teste Filter Numérico',
            'program': 'dados = load "test.csv"\nfiltrados = filter dados where valor > 200\ndisplay filtrados',
            'expected_vars': ['dados', 'filtrados']
        },
        {
            'name': 'Teste Select Múltiplas Colunas',
            'program': 'dados = load "test.csv"\nresult = select dados (nome, valor)\ndisplay result',
            'expected_vars': ['dados', 'result']
        }
    ]
    
    all_passed = True
    
    for test in tests:
        print(f"\nExecutando: {test['name']}")
        
        try:
            coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
            lexer = Lexer(test['program'], coffee_dfa)
            parser = Parser(lexer)
            ast = parser.parse()
            
            analyzer = SemanticAnalyzer(debug=False)
            semantic_success, errors, _ = analyzer.analyze(ast)
            
            if not semantic_success:
                print(f"  ✗ Falha na análise semântica: {errors}")
                all_passed = False
                continue
            
            interpreter = CoffeeInterpreter(debug=False)
            result = interpreter.interpret(ast)
            
            if not result['success']:
                print(f"  ✗ Falha na execução: {result['error']}")
                all_passed = False
                continue
            
            # Verifica se as variáveis esperadas existem
            env_vars = list(result['environment'].keys())
            missing_vars = [v for v in test['expected_vars'] if v not in env_vars]
            
            if missing_vars:
                print(f"  ✗ Variáveis ausentes: {missing_vars}")
                all_passed = False
            else:
                print(f"  ✓ Sucesso - Variáveis criadas: {env_vars}")
        
        except Exception as e:
            print(f"  ✗ Exceção: {e}")
            all_passed = False
    
    print(f"\nResultado geral: {'✓ TODOS OS TESTES PASSARAM' if all_passed else '✗ ALGUNS TESTES FALHARAM'}")
    return all_passed

def main():
    """Função principal para executar benchmarks"""
    print("SISTEMA DE BENCHMARKS E TESTES - INTERPRETADOR COFFEE")
    print("="*60)
    
    # Testes de correção
    correctness_passed = run_correctness_tests()
    
    if not correctness_passed:
        print("\nInterrompendo benchmarks devido a falhas nos testes de correção.")
        return
    
    # Benchmarks de performance
    benchmark_suite = BenchmarkSuite()
    benchmark_results = benchmark_suite.run_all_benchmarks()
    
    # Comparação de performance
    comparator = PerformanceComparator()
    comparison_results = comparator.compare_with_python_pandas(iterations=10)
    
    # Relatório final
    print("\n" + "="*60)
    print("RELATÓRIO FINAL")
    print("="*60)
    
    print(f"Testes de correção: {'✓ PASSOU' if correctness_passed else '✗ FALHOU'}")
    print(f"Benchmarks executados: {benchmark_results['total_tests']}")
    print(f"Taxa de sucesso: {benchmark_results['successful']/benchmark_results['total_tests']*100:.1f}%")
    
    if comparison_results['coffee_avg_time'] > 0:
        overhead = comparison_results['overhead_factor']
        print(f"Overhead vs Pandas: {overhead:.2f}x")
        
        if overhead < 5:
            print("Performance: EXCELENTE (overhead < 5x)")
        elif overhead < 10:
            print("Performance: BOA (overhead < 10x)")
        elif overhead < 20:
            print("Performance: ACEITÁVEL (overhead < 20x)")
        else:
            print("Performance: PRECISA MELHORAR (overhead > 20x)")

if __name__ == '__main__':
    main()