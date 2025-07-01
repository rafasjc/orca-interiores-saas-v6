"""
Sistema de Autenticação - Orca Interiores
Versão limpa sem credenciais expostas
"""

import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class AuthManager:
    """Gerenciador de autenticação"""
    
    def __init__(self, db_path: str = "usuarios.db"):
        """Inicializa o gerenciador de autenticação"""
        self.db_path = db_path
        self.criar_banco()
        self.criar_usuarios_demo()
    
    def criar_banco(self):
        """Cria banco de dados de usuários"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                plano TEXT NOT NULL DEFAULT 'basico',
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_login TIMESTAMP,
                orcamentos_usados INTEGER DEFAULT 0,
                limite_orcamentos INTEGER DEFAULT 5
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                acao TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def criar_usuarios_demo(self):
        """Cria usuários demo"""
        
        usuarios_demo = [
            {
                'nome': 'Usuário Demo',
                'email': 'demo@orcainteriores.com',
                'senha': 'demo123',
                'plano': 'profissional',
                'limite_orcamentos': 50
            },
            {
                'nome': 'Arquiteto Teste',
                'email': 'arquiteto@teste.com',
                'senha': 'arq123',
                'plano': 'basico',
                'limite_orcamentos': 5
            },
            {
                'nome': 'Marceneiro Teste',
                'email': 'marceneiro@teste.com',
                'senha': 'marc123',
                'plano': 'empresarial',
                'limite_orcamentos': 999999
            }
        ]
        
        for usuario in usuarios_demo:
            self.criar_usuario(
                nome=usuario['nome'],
                email=usuario['email'],
                senha=usuario['senha'],
                plano=usuario['plano'],
                limite_orcamentos=usuario['limite_orcamentos']
            )
    
    def hash_senha(self, senha: str) -> str:
        """Gera hash seguro da senha"""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def criar_usuario(self, nome: str, email: str, senha: str, 
                     plano: str = 'basico', limite_orcamentos: int = 5) -> bool:
        """Cria novo usuário"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return False
            
            senha_hash = self.hash_senha(senha)
            cursor.execute('''
                INSERT INTO usuarios (nome, email, senha_hash, plano, limite_orcamentos)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, email, senha_hash, plano, limite_orcamentos))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False
    
    def fazer_login(self, email: str, senha: str) -> Optional[Dict]:
        """Realiza login do usuário"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_senha(senha)
            cursor.execute('''
                SELECT id, nome, email, plano, ativo, orcamentos_usados, limite_orcamentos
                FROM usuarios 
                WHERE email = ? AND senha_hash = ? AND ativo = 1
            ''', (email, senha_hash))
            
            usuario = cursor.fetchone()
            
            if usuario:
                cursor.execute('''
                    UPDATE usuarios 
                    SET ultimo_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (usuario[0],))
                
                cursor.execute('''
                    INSERT INTO logs_acesso (usuario_id, acao)
                    VALUES (?, 'login')
                ''', (usuario[0],))
                
                conn.commit()
                conn.close()
                
                return {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'plano': usuario[3],
                    'ativo': usuario[4],
                    'orcamentos_usados': usuario[5],
                    'limite_orcamentos': usuario[6]
                }
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Erro no login: {e}")
            return None
    
    def verificar_limite_orcamentos(self, usuario_id: int) -> bool:
        """Verifica se usuário pode fazer mais orçamentos"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT orcamentos_usados, limite_orcamentos
                FROM usuarios 
                WHERE id = ?
            ''', (usuario_id,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                usados, limite = resultado
                return usados < limite
            
            return False
            
        except Exception as e:
            print(f"Erro ao verificar limite: {e}")
            return False
    
    def incrementar_orcamento(self, usuario_id: int) -> bool:
        """Incrementa contador de orçamentos do usuário"""
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE usuarios 
                SET orcamentos_usados = orcamentos_usados + 1
                WHERE id = ?
            ''', (usuario_id,))
            
            cursor.execute('''
                INSERT INTO logs_acesso (usuario_id, acao)
                VALUES (?, 'orcamento_gerado')
            ''', (usuario_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Erro ao incrementar orçamento: {e}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    auth = AuthManager()
    print("✅ Sistema de autenticação criado!")
    
    usuario = auth.fazer_login("demo@orcainteriores.com", "demo123")
    if usuario:
        print(f"✅ Login bem-sucedido: {usuario['nome']}")
    else:
        print("❌ Falha no login")

