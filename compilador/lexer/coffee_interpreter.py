"""
Funcionalidades:
- Execução direta de ASTs verificadas semanticamente
- Gerenciamento de datasets em memória (CSV, JSON)
- Operações de filtragem, seleção e exibição
- Ambiente de execução com escopo de variáveis
- Sistema de tipos em runtime
"""

import sys
import os
import csv
import json
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Importa classes do parser e analisador semântico
sys.path.append(os.path.dirname(__file__))
from parser import *
from semantic_analyzer import SemanticAnalyzer, DataType

@dataclass
class RuntimeValue:
    """Representa um valor em tempo de execução"""
    value: Any
    type: DataType
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class RuntimeError(Exception):
    """Exceção para erros em tempo de execução"""
    def __init__(self, message: str, context: str = ""):
        self.message = message
        self.context = context
        super().__init__(f"Runtime Error: {message}" + (f" (Context: {context})" if context else ""))

class Environment:
    """Ambiente de execução que gerencia variáveis e escopos"""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.variables: Dict[str, RuntimeValue] = {}
    
    def define(self, name: str, value: RuntimeValue) -> None:
        """Define uma nova variável no escopo atual"""
        self.variables[name] = value
    
    def get(self, name: str) -> RuntimeValue:
        """Busca uma variável no escopo atual ou nos pais"""
        if name in self.variables:
            return self.variables[name]
        
        if self.parent:
            return self.parent.get(name)
        
        raise RuntimeError(f"Variável '{name}' não foi definida", name)
    
    def exists(self, name: str) -> bool:
        """Verifica se uma variável existe"""
        return name in self.variables or (self.parent and self.parent.exists(name))

class DatasetOperations:
    """Operações para manipulação de datasets"""
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Carrega arquivo CSV"""
        try:
            # Remove aspas do caminho
            clean_path = file_path.strip('"')
            
            # Para demonstração, cria dados fictícios se o arquivo não existir
            if not os.path.exists(clean_path):
                print(f"Aviso: Arquivo '{clean_path}' não encontrado. Criando dados de demonstração.")
                return DatasetOperations._create_demo_data(clean_path)
            
            return pd.read_csv(clean_path)
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar arquivo CSV '{file_path}': {e}", file_path)
    
    @staticmethod
    def load_json(file_path: str) -> pd.DataFrame:
        """Carrega arquivo JSON"""
        try:
            clean_path = file_path.strip('"')
            
            if not os.path.exists(clean_path):
                print(f"Aviso: Arquivo '{clean_path}' não encontrado. Criando dados de demonstração.")
                return DatasetOperations._create_demo_data(clean_path)
            
            with open(clean_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Converte para DataFrame
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                return pd.DataFrame([data])
            else:
                raise RuntimeError(f"Formato JSON inválido em '{file_path}'")
                
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar arquivo JSON '{file_path}': {e}", file_path)
    
    @staticmethod
    def _create_demo_data(file_path: str) -> pd.DataFrame:
        """Cria dados de demonstração baseados no nome do arquivo"""
        filename = os.path.basename(file_path).lower()
        
        if 'vendas' in filename:
            return pd.DataFrame({
                'produto': ['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Headset'],
                'quantidade': [2, 10, 5, 1, 3],
                'preco': [2500.00, 50.00, 150.00, 800.00, 200.00],
                'total': [5000.00, 500.00, 750.00, 800.00, 600.00],
                'vendedor': ['Ana', 'Carlos', 'Ana', 'Bruno', 'Carlos']
            })
        elif 'clientes' in filename or 'cliente' in filename:
            return pd.DataFrame({
                'nome': ['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa'],
                'email': ['joao@email.com', 'maria@email.com', 'pedro@email.com', 'ana@email.com'],
                'idade': [30, 25, 35, 28],
                'cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador']
            })
        elif 'produtos' in filename or 'produto' in filename:
            return pd.DataFrame({
                'nome': ['Notebook Pro', 'Mouse Gamer', 'Teclado Mecânico', 'Monitor 4K'],
                'categoria': ['Computadores', 'Periféricos', 'Periféricos', 'Monitores'],
                'preco': [3500.00, 80.00, 300.00, 1200.00],
                'status': ['ativo', 'ativo', 'inativo', 'ativo'],
                'estoque': [15, 50, 0, 8]
            })
        else:
            # Dados genéricos
            return pd.DataFrame({
                'id': [1, 2, 3, 4, 5],
                'nome': ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
                'valor': [100, 200, 300, 400, 500],
                'ativo': [True, True, False, True, False]
            })
    
    @staticmethod
    def filter_dataset(df: pd.DataFrame, column: str, operator: str, value: Any) -> pd.DataFrame:
        """Aplica filtro em dataset"""
        try:
            if column not in df.columns:
                available_cols = ', '.join(df.columns.tolist())
                raise RuntimeError(f"Coluna '{column}' não existe. Colunas disponíveis: {available_cols}", column)
            
            if operator == '>':
                return df[df[column] > value]
            elif operator == '<':
                return df[df[column] < value]
            elif operator == '>=':
                return df[df[column] >= value]
            elif operator == '<=':
                return df[df[column] <= value]
            elif operator == '==':
                return df[df[column] == value]
            elif operator == '!=':
                return df[df[column] != value]
            else:
                raise RuntimeError(f"Operador '{operator}' não suportado", operator)
                
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise
            raise RuntimeError(f"Erro ao filtrar dataset: {e}", f"{column} {operator} {value}")
    
    @staticmethod
    def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Seleciona colunas específicas do dataset"""
        try:
            # Verifica se todas as colunas existem
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                available_cols = ', '.join(df.columns.tolist())
                raise RuntimeError(f"Colunas não encontradas: {', '.join(missing_cols)}. "
                                 f"Colunas disponíveis: {available_cols}", str(missing_cols))
            
            return df[columns]
            
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise
            raise RuntimeError(f"Erro ao selecionar colunas: {e}", str(columns))
    
    @staticmethod
    def display_dataset(df: pd.DataFrame, name: str = "") -> None:
        """Exibe dataset formatado"""
        print(f"\n{'='*60}")
        if name:
            print(f"DATASET: {name}")
        else:
            print("RESULTADO")
        print(f"{'='*60}")
        print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
        print(f"Colunas: {', '.join(df.columns.tolist())}")
        print("-" * 60)
        
        # Exibe até 20 linhas para não poluir a saída
        if len(df) > 20:
            print(df.head(10).to_string(index=False))
            print(f"... ({len(df) - 20} linhas omitidas) ...")
            print(df.tail(10).to_string(index=False))
        else:
            print(df.to_string(index=False))
        
        print(f"{'='*60}\n")

class CoffeeInterpreter:
    """Interpretador principal para programas Coffee"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.global_env = Environment()
        self.current_env = self.global_env
        
        # Estatísticas de execução
        self.stats = {
            'datasets_loaded': 0,
            'operations_executed': 0,
            'variables_created': 0,
            'displays_performed': 0
        }
    
    def interpret(self, ast: ProgramNode) -> Dict[str, Any]:
        """
        Interpreta um programa Coffee a partir da AST
        
        Args:
            ast: Árvore sintática abstrata verificada semanticamente
            
        Returns:
            Dict com informações sobre a execução
        """
        if self.debug:
            print("Iniciando execução do programa Coffee...")
        
        try:
            self.visit(ast)
            
            result = {
                'success': True,
                'environment': self._serialize_environment(),
                'statistics': self.stats
            }
            
            if self.debug:
                self._print_execution_summary()
            
            return result
            
        except RuntimeError as e:
            if self.debug:
                print(f"Erro durante execução: {e}")
            
            return {
                'success': False,
                'error': str(e),
                'statistics': self.stats
            }
    
    def visit(self, node: ASTNode) -> RuntimeValue:
        """Padrão Visitor para interpretar nós da AST"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> RuntimeValue:
        """Método genérico para nós não implementados"""
        raise RuntimeError(f"Interpretador não implementado para: {type(node).__name__}")
    
    # ===== VISITORS PARA CADA TIPO DE NÓ =====
    
    def visit_ProgramNode(self, node: ProgramNode) -> RuntimeValue:
        """Executa o programa principal"""
        if self.debug:
            print(f"Executando programa com {len(node.statements)} statements")
        
        last_value = None
        for statement in node.statements:
            last_value = self.visit(statement)
        
        return last_value or RuntimeValue(None, DataType.UNKNOWN)
    
    def visit_AssignmentStatementNode(self, node: AssignmentStatementNode) -> RuntimeValue:
        """Executa atribuições"""
        if self.debug:
            print(f"Executando atribuição: {node.identifier}")
        
        # Avalia a expressão do lado direito
        value = self.visit(node.expression)
        
        # Define a variável no ambiente
        self.current_env.define(node.identifier, value)
        self.stats['variables_created'] += 1
        
        if self.debug:
            print(f"Variável '{node.identifier}' definida com valor do tipo {value.type.value}")
        
        return value
    
    def visit_DisplayStatementNode(self, node: DisplayStatementNode) -> RuntimeValue:
        """Executa comandos display"""
        if self.debug:
            print(f"Executando display: {node.identifier}")
        
        # Busca a variável no ambiente
        variable = self.current_env.get(node.identifier)
        
        if variable.type != DataType.DATASET:
            raise RuntimeError(f"Display só pode ser usado com datasets. "
                             f"'{node.identifier}' é do tipo {variable.type.value}")
        
        # Exibe o dataset
        DatasetOperations.display_dataset(variable.value, node.identifier)
        self.stats['displays_performed'] += 1
        
        return RuntimeValue(None, DataType.UNKNOWN)
    
    def visit_LoadExpressionNode(self, node: LoadExpressionNode) -> RuntimeValue:
        """Executa operações de load"""
        if self.debug:
            print(f"Executando load: {node.file_path}")
        
        file_path = node.file_path.strip('"')
        
        try:
            # Determina o tipo de arquivo e carrega apropriadamente
            if file_path.endswith('.csv'):
                df = DatasetOperations.load_csv(node.file_path)
            elif file_path.endswith('.json'):
                df = DatasetOperations.load_json(node.file_path)
            else:
                # Assume CSV por padrão
                df = DatasetOperations.load_csv(node.file_path)
            
            self.stats['datasets_loaded'] += 1
            self.stats['operations_executed'] += 1
            
            if self.debug:
                print(f"Dataset carregado: {len(df)} linhas, {len(df.columns)} colunas")
            
            return RuntimeValue(df, DataType.DATASET, {'file_path': file_path})
            
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar arquivo '{file_path}': {e}")
    
    def visit_FilterExpressionNode(self, node: FilterExpressionNode) -> RuntimeValue:
        """Executa operações de filter"""
        if self.debug:
            print(f"Executando filter no dataset: {node.dataset}")
        
        # Busca o dataset no ambiente
        dataset_var = self.current_env.get(node.dataset)
        
        if dataset_var.type != DataType.DATASET:
            raise RuntimeError(f"Filter só pode ser aplicado a datasets")
        
        # Avalia a condição (deve ser uma expressão relacional)
        if not isinstance(node.condition, RelationalExpressionNode):
            raise RuntimeError("Condição do filter deve ser uma comparação")
        
        # Extrai componentes da comparação
        left_term = node.condition.left
        operator = node.condition.operator
        right_term = node.condition.right
        
        # Por simplicidade, assume que o lado esquerdo é sempre uma coluna
        if not isinstance(left_term, TermNode) or left_term.type != 'IDENTIFIER':
            raise RuntimeError("Lado esquerdo da comparação deve ser um nome de coluna")
        
        column_name = left_term.value
        
        # Avalia o lado direito
        right_value = self._evaluate_term(right_term)
        
        # Aplica o filtro
        filtered_df = DatasetOperations.filter_dataset(
            dataset_var.value, column_name, operator, right_value
        )
        
        self.stats['operations_executed'] += 1
        
        if self.debug:
            original_rows = len(dataset_var.value)
            filtered_rows = len(filtered_df)
            print(f"Filter aplicado: {original_rows} -> {filtered_rows} linhas")
        
        return RuntimeValue(filtered_df, DataType.DATASET)
    
    def visit_SelectExpressionNode(self, node: SelectExpressionNode) -> RuntimeValue:
        """Executa operações de select"""
        if self.debug:
            print(f"Executando select no dataset: {node.dataset}")
        
        # Busca o dataset no ambiente
        dataset_var = self.current_env.get(node.dataset)
        
        if dataset_var.type != DataType.DATASET:
            raise RuntimeError(f"Select só pode ser aplicado a datasets")
        
        # Seleciona as colunas
        selected_df = DatasetOperations.select_columns(dataset_var.value, node.columns)
        
        self.stats['operations_executed'] += 1
        
        if self.debug:
            print(f"Select executado: {len(node.columns)} colunas selecionadas")
        
        return RuntimeValue(selected_df, DataType.DATASET, 
                          {'selected_columns': node.columns})
    
    def _evaluate_term(self, term: TermNode) -> Any:
        """Avalia um termo e retorna seu valor"""
        if term.type == 'NUMBER':
            try:
                # Tenta converter para int primeiro, depois float
                if '.' in term.value:
                    return float(term.value)
                else:
                    return int(term.value)
            except ValueError:
                raise RuntimeError(f"Valor numérico inválido: {term.value}")
        
        elif term.type == 'STRING':
            # Remove aspas
            return term.value.strip('"')
        
        elif term.type == 'IDENTIFIER':
            # Busca variável no ambiente
            var = self.current_env.get(term.value)
            return var.value
        
        else:
            raise RuntimeError(f"Tipo de termo não suportado: {term.type}")
    
    def _serialize_environment(self) -> Dict[str, Any]:
        """Serializa o ambiente para retorno"""
        result = {}
        for name, value in self.current_env.variables.items():
            if value.type == DataType.DATASET:
                result[name] = {
                    'type': 'dataset',
                    'rows': len(value.value),
                    'columns': list(value.value.columns),
                    'metadata': value.metadata
                }
            else:
                result[name] = {
                    'type': value.type.value,
                    'value': str(value.value),
                    'metadata': value.metadata
                }
        return result
    
    def _print_execution_summary(self):
        """Imprime resumo da execução"""
        print("\n" + "="*50)
        print("RESUMO DA EXECUÇÃO")
        print("="*50)
        print(f"Datasets carregados: {self.stats['datasets_loaded']}")
        print(f"Operações executadas: {self.stats['operations_executed']}")
        print(f"Variáveis criadas: {self.stats['variables_created']}")
        print(f"Displays realizados: {self.stats['displays_performed']}")
        
        print(f"\nVariáveis no ambiente:")
        for name, info in self._serialize_environment().items():
            print(f"  • {name}: {info['type']}")
        
        print("="*50)

def main():
    """Função principal do interpretador"""
    if len(sys.argv) != 2:
        print("Uso: python coffee_interpreter.py <arquivo.coffee>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # Lê o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"Executando programa Coffee: {file_path}")
        print("="*60)
        
        # Fase 1: Análise Léxica e Sintática
        print("1. ANÁLISE SINTÁTICA")
        print("-" * 30)
        
        coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
        lexer = Lexer(code, coffee_dfa)
        parser = Parser(lexer)
        ast = parser.parse()
        
        print("AST construída com sucesso!")
        
        # Fase 2: Análise Semântica
        print("\n2. ANÁLISE SEMÂNTICA")
        print("-" * 30)
        
        analyzer = SemanticAnalyzer(debug=False)
        semantic_success, errors, _ = analyzer.analyze(ast)
        
        if not semantic_success:
            print("Erros semânticos encontrados:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print("Análise semântica bem-sucedida!")
        
        # Fase 3: Interpretação/Execução
        print("\n3. EXECUÇÃO DO PROGRAMA")
        print("-" * 30)
        
        interpreter = CoffeeInterpreter(debug=True)
        result = interpreter.interpret(ast)
        
        if result['success']:
            print("\nPrograma executado com sucesso!")
        else:
            print(f"\nErro durante execução: {result['error']}")
            sys.exit(1)
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante compilação/execução: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()