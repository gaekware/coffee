import sys
import os
from enum import Enum
from typing import Dict, List, Optional, Any, Union

# Importa as classes AST do parser
sys.path.append(os.path.dirname(__file__))
from parser import *

class DataType(Enum):
    """Enumeração dos tipos de dados na linguagem Coffee"""
    DATASET = "dataset"
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    COLUMN = "column"
    UNKNOWN = "unknown"
    ERROR = "error"

class SemanticError:
    """Classe para representar erros semânticos"""
    def __init__(self, message: str, node_type: str = "", context: str = ""):
        self.message = message
        self.node_type = node_type
        self.context = context
    
    def __str__(self):
        if self.context:
            return f"[{self.node_type}] {self.message} (Contexto: {self.context})"
        return f"[{self.node_type}] {self.message}"

class Symbol:
    """Representa um símbolo na tabela de símbolos"""
    def __init__(self, name: str, data_type: DataType, is_initialized: bool = False, 
                 metadata: Dict[str, Any] = None):
        self.name = name
        self.type = data_type
        self.is_initialized = is_initialized
        self.metadata = metadata or {}
        self.usage_count = 0
    
    def __repr__(self):
        return f"Symbol({self.name}: {self.type.value}, init={self.is_initialized})"

class SymbolTable:
    """Tabela de símbolos para gerenciar variáveis e seus tipos"""
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
    
    def declare(self, name: str, data_type: DataType, metadata: Dict[str, Any] = None) -> bool:
        """Declara uma nova variável"""
        if name in self.symbols:
            return False  # Variável já declarada
        
        self.symbols[name] = Symbol(name, data_type, True, metadata)
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Busca uma variável na tabela"""
        symbol = self.symbols.get(name)
        if symbol:
            symbol.usage_count += 1
        return symbol
    
    def exists(self, name: str) -> bool:
        """Verifica se uma variável existe"""
        return name in self.symbols
    
    def get_type(self, name: str) -> DataType:
        """Retorna o tipo de uma variável"""
        symbol = self.lookup(name)
        return symbol.type if symbol else DataType.UNKNOWN
    
    def get_all_symbols(self) -> Dict[str, Symbol]:
        """Retorna todos os símbolos"""
        return self.symbols.copy()

class SemanticAnalyzer:
    """
    Analisador Semântico Principal
    
    Implementa análise semântica completa usando padrão Visitor
    para percorrer a AST e realizar verificações semânticas.
    """
    
    def __init__(self, debug: bool = False):
        self.symbol_table = SymbolTable()
        self.errors: List[SemanticError] = []
        self.warnings: List[str] = []
        self.debug = debug
        
        # Contadores para estatísticas
        self.stats = {
            'variables_declared': 0,
            'operations_validated': 0,
            'type_inferences': 0
        }
    
    def analyze(self, ast: ProgramNode) -> tuple[bool, List[SemanticError], Dict[str, Any]]:
        """
        Ponto de entrada para análise semântica
        
        Args:
            ast: Árvore sintática abstrata
            
        Returns:
            tuple: (sucesso, lista_de_erros, informações_adicionais)
        """
        if self.debug:
            print("Iniciando análise semântica...")
        
        # Visita o nó raiz
        self.visit(ast)
        
        # Análises pós-processamento
        self._post_analysis_checks()
        
        success = len(self.errors) == 0
        
        info = {
            'symbol_table': self.symbol_table.get_all_symbols(),
            'warnings': self.warnings,
            'statistics': self.stats
        }
        
        if self.debug:
            self._print_analysis_summary()
        
        return success, self.errors, info
    
    def visit(self, node: ASTNode) -> DataType:
        """Padrão Visitor para percorrer a AST"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode) -> DataType:
        """Método genérico para nós não implementados"""
        self._add_error(f"Nó não implementado: {type(node).__name__}", 
                       type(node).__name__)
        return DataType.ERROR
    
    # ===== VISITORS PARA CADA TIPO DE NÓ =====
    
    def visit_ProgramNode(self, node: ProgramNode) -> DataType:
        """Processa o programa principal"""
        if self.debug:
            print(f"Analisando programa com {len(node.statements)} statements")
        
        for statement in node.statements:
            self.visit(statement)
        
        return DataType.UNKNOWN  # Programa não tem tipo específico
    
    def visit_AssignmentStatementNode(self, node: AssignmentStatementNode) -> DataType:
        """Processa atribuições e declara variáveis"""
        if self.debug:
            print(f"Processando atribuição: {node.identifier}")
        
        # Analisa a expressão do lado direito
        expr_type = self.visit(node.expression)
        
        # Verifica se houve erro na expressão
        if expr_type == DataType.ERROR:
            self._add_error(f"Erro na expressão atribuída à variável '{node.identifier}'",
                           "AssignmentStatement", node.identifier)
            return DataType.ERROR
        
        # Declara a variável na tabela de símbolos
        if not self.symbol_table.declare(node.identifier, expr_type):
            self._add_error(f"Variável '{node.identifier}' já foi declarada",
                           "AssignmentStatement", node.identifier)
            return DataType.ERROR
        
        self.stats['variables_declared'] += 1
        
        if self.debug:
            print(f"Variável '{node.identifier}' declarada com tipo {expr_type.value}")
        
        return expr_type
    
    def visit_DisplayStatementNode(self, node: DisplayStatementNode) -> DataType:
        """Processa comandos display"""
        if self.debug:
            print(f"Processando display: {node.identifier}")
        
        # Verifica se a variável foi declarada
        symbol = self.symbol_table.lookup(node.identifier)
        if not symbol:
            self._add_error(f"Variável '{node.identifier}' não foi declarada",
                           "DisplayStatement", node.identifier)
            return DataType.ERROR
        
        # Display só funciona com datasets
        if symbol.type != DataType.DATASET:
            self._add_error(f"Display só pode ser usado com datasets. "
                           f"'{node.identifier}' é do tipo {symbol.type.value}",
                           "DisplayStatement", node.identifier)
            return DataType.ERROR
        
        if self.debug:
            print(f"Display válido para dataset '{node.identifier}'")
        
        return DataType.UNKNOWN
    
    def visit_LoadExpressionNode(self, node: LoadExpressionNode) -> DataType:
        """Processa operações de load"""
        if self.debug:
            print(f"Processando load: {node.file_path}")
        
        # Valida se é uma string (arquivo)
        if not node.file_path.startswith('"') or not node.file_path.endswith('"'):
            self._add_error("Load requer um caminho de arquivo como string",
                           "LoadExpression", node.file_path)
            return DataType.ERROR
        
        # Verifica extensão do arquivo (opcional, mas educativo)
        file_path_clean = node.file_path.strip('"')
        if not (file_path_clean.endswith('.csv') or file_path_clean.endswith('.json') or 
                file_path_clean.endswith('.txt')):
            self.warnings.append(f"Arquivo '{file_path_clean}' pode não ser um formato "
                               "de dados suportado (recomendado: .csv, .json, .txt)")
        
        self.stats['type_inferences'] += 1
        
        if self.debug:
            print(f"Load válido, retorna dataset")
        
        return DataType.DATASET
    
    def visit_FilterExpressionNode(self, node: FilterExpressionNode) -> DataType:
        """Processa operações de filter"""
        if self.debug:
            print(f"Processando filter no dataset: {node.dataset}")
        
        # Verifica se o dataset existe e é do tipo correto
        dataset_symbol = self.symbol_table.lookup(node.dataset)
        if not dataset_symbol:
            self._add_error(f"Dataset '{node.dataset}' não foi declarado",
                           "FilterExpression", node.dataset)
            return DataType.ERROR
        
        if dataset_symbol.type != DataType.DATASET:
            self._add_error(f"Filter só pode ser aplicado a datasets. "
                           f"'{node.dataset}' é do tipo {dataset_symbol.type.value}",
                           "FilterExpression", node.dataset)
            return DataType.ERROR
        
        # Analisa a condição
        condition_type = self.visit(node.condition)
        if condition_type != DataType.BOOLEAN and condition_type != DataType.ERROR:
            self._add_error("Condição do filter deve resultar em um valor booleano",
                           "FilterExpression", "condition")
            return DataType.ERROR
        
        self.stats['operations_validated'] += 1
        
        if self.debug:
            print(f"Filter válido, mantém tipo dataset")
        
        return DataType.DATASET
    
    def visit_SelectExpressionNode(self, node: SelectExpressionNode) -> DataType:
        """Processa operações de select"""
        if self.debug:
            print(f"Processando select no dataset: {node.dataset}")
        
        # Verifica se o dataset existe e é do tipo correto
        dataset_symbol = self.symbol_table.lookup(node.dataset)
        if not dataset_symbol:
            self._add_error(f"Dataset '{node.dataset}' não foi declarado",
                           "SelectExpression", node.dataset)
            return DataType.ERROR
        
        if dataset_symbol.type != DataType.DATASET:
            self._add_error(f"Select só pode ser aplicado a datasets. "
                           f"'{node.dataset}' é do tipo {dataset_symbol.type.value}",
                           "SelectExpression", node.dataset)
            return DataType.ERROR
        
        # Valida se há pelo menos uma coluna
        if not node.columns:
            self._add_error("Select deve especificar pelo menos uma coluna",
                           "SelectExpression", "columns")
            return DataType.ERROR
        
        # Armazena metadados sobre as colunas selecionadas
        metadata = {'selected_columns': node.columns}
        
        self.stats['operations_validated'] += 1
        
        if self.debug:
            print(f"Select válido com colunas: {', '.join(node.columns)}")
        
        return DataType.DATASET
    
    def visit_RelationalExpressionNode(self, node: RelationalExpressionNode) -> DataType:
        """Processa expressões relacionais (comparações)"""
        if self.debug:
            print(f"Processando comparação: {node.operator}")
        
        # Analisa os operandos
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Verifica erros nos operandos
        if left_type == DataType.ERROR or right_type == DataType.ERROR:
            return DataType.ERROR
        
        # Validação de tipos para comparação
        valid_comparisons = self._validate_comparison(left_type, right_type, node.operator)
        if not valid_comparisons:
            self._add_error(f"Comparação inválida: {left_type.value} {node.operator} {right_type.value}",
                           "RelationalExpression", node.operator)
            return DataType.ERROR
        
        self.stats['operations_validated'] += 1
        
        if self.debug:
            print(f"Comparação válida, retorna boolean")
        
        return DataType.BOOLEAN
    
    def visit_TermNode(self, node: TermNode) -> DataType:
        """Processa termos (folhas da AST)"""
        if node.type == 'IDENTIFIER':
            symbol = self.symbol_table.lookup(node.value)
            if not symbol:
                # Para identificadores em expressões, assume que são colunas
                if self.debug:
                    print(f"Assumindo '{node.value}' como referência de coluna")
                return DataType.COLUMN
            return symbol.type
        
        elif node.type == 'NUMBER':
            return DataType.NUMBER
        
        elif node.type == 'STRING':
            return DataType.STRING
        
        return DataType.UNKNOWN
    
    # ===== MÉTODOS AUXILIARES =====
    
    def _validate_comparison(self, left_type: DataType, right_type: DataType, 
                           operator: str) -> bool:
        """Valida se uma comparação entre dois tipos é válida"""
        # Regras de comparação
        numeric_ops = ['>', '<', '>=', '<=']
        equality_ops = ['==', '!=']
        
        if operator in numeric_ops:
            # Operadores numéricos: ambos devem ser números ou colunas
            return (left_type in [DataType.NUMBER, DataType.COLUMN] and
                   right_type in [DataType.NUMBER, DataType.COLUMN])
        
        elif operator in equality_ops:
            # Operadores de igualdade: tipos compatíveis
            return (left_type == right_type or 
                   DataType.COLUMN in [left_type, right_type])
        
        return False
    
    def _add_error(self, message: str, node_type: str = "", context: str = ""):
        """Adiciona um erro à lista"""
        error = SemanticError(message, node_type, context)
        self.errors.append(error)
        
        if self.debug:
            print(f"ERRO: {error}")
    
    def _post_analysis_checks(self):
        """Verificações após a análise principal"""
        # Verifica variáveis não utilizadas
        for name, symbol in self.symbol_table.get_all_symbols().items():
            if symbol.usage_count == 0:
                self.warnings.append(f"Variável '{name}' foi declarada mas nunca utilizada")
    
    def _print_analysis_summary(self):
        """Imprime resumo da análise"""
        print("\n" + "="*50)
        print("RESUMO DA ANÁLISE SEMÂNTICA")
        print("="*50)
        
        print(f"Variáveis declaradas: {self.stats['variables_declared']}")
        print(f"Operações validadas: {self.stats['operations_validated']}")
        print(f"Inferências de tipo: {self.stats['type_inferences']}")
        
        if self.errors:
            print(f"\nErros encontrados: {len(self.errors)}")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"\nAvisos: {len(self.warnings)}")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        print(f"\nTabela de Símbolos:")
        for name, symbol in self.symbol_table.get_all_symbols().items():
            print(f"  • {name}: {symbol.type.value} (usado {symbol.usage_count}x)")

def main():
    """Função principal para testar o analisador semântico"""
    if len(sys.argv) != 2:
        print("Uso: python semantic_analyzer.py <arquivo.coffee>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # Lê o arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        print(f"Analisando arquivo: {file_path}")
        print("="*50)
        
        # Fase 1: Análise Léxica e Sintática
        print("ANÁLISE SINTÁTICA")
        print("-" * 30)
        
        coffee_dfa = DFA(DFA_TRANSITIONS, DFA_ACCEPTING_STATES)
        lexer = Lexer(code, coffee_dfa)
        parser = Parser(lexer)
        ast = parser.parse()
        
        print("AST construída com sucesso!")
        
        # Fase 2: Análise Semântica
        print("\nANÁLISE SEMÂNTICA")
        print("-" * 30)
        
        analyzer = SemanticAnalyzer(debug=True)
        success, errors, info = analyzer.analyze(ast)
        
        # Resultado final
        print("\n" + "="*50)
        if success:
            print("COMPILAÇÃO BEM-SUCEDIDA!")
            print("   Programa semanticamente correto.")
        else:
            print("FALHA NA COMPILAÇÃO!")
            print(f"   Encontrados {len(errors)} erros semânticos.")
            
        print("="*50)
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante análise: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
