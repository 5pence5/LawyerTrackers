import streamlit as st
import hashlib
import pandas as pd
import os

class ClientAuth:
    def __init__(self):
        self.clients_auth_file = "client_auth.csv"
        self._initialize_auth_file()
    
    def _initialize_auth_file(self):
        """Initialize the client authentication file if it doesn't exist"""
        if not os.path.exists(self.clients_auth_file):
            pd.DataFrame(columns=[
                'client_name', 'username', 'password_hash'
            ]).to_csv(self.clients_auth_file, index=False)
    
    def _hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_client(self, client_name, username, password):
        """Register a new client with login credentials"""
        try:
            df = pd.read_csv(self.clients_auth_file)
            
            # Check if username already exists
            if not df.empty and username in df['username'].values:
                return False, "Username already exists"
            
            # Add new client credentials
            new_client = {
                'client_name': client_name,
                'username': username,
                'password_hash': self._hash_password(password)
            }
            
            df = pd.concat([df, pd.DataFrame([new_client])], ignore_index=True)
            df.to_csv(self.clients_auth_file, index=False)
            return True, "Client registered successfully"
            
        except Exception as e:
            return False, f"Error registering client: {str(e)}"
    
    def authenticate_client(self, username, password):
        """Authenticate a client's login credentials"""
        try:
            df = pd.read_csv(self.clients_auth_file)
            if df.empty:
                return False, None
            
            client_row = df[df['username'] == username]
            if client_row.empty:
                return False, None
            
            if client_row.iloc[0]['password_hash'] == self._hash_password(password):
                return True, client_row.iloc[0]['client_name']
                
            return False, None
            
        except Exception:
            return False, None
