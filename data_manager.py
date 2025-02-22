import pandas as pd
from datetime import datetime
import os

class DataManager:
    def __init__(self):
        self.time_entries_file = "time_entries.csv"
        self.clients_file = "clients.csv"
        self.matters_file = "matters.csv"
        self._initialize_files()
        
    def _initialize_files(self):
        """Initialize CSV files if they don't exist"""
        if not os.path.exists(self.time_entries_file):
            pd.DataFrame(columns=[
                'date', 'client', 'matter', 'duration', 'narrative'
            ]).to_csv(self.time_entries_file, index=False)
            
        if not os.path.exists(self.clients_file):
            pd.DataFrame(columns=['client_name']).to_csv(self.clients_file, index=False)
            
        if not os.path.exists(self.matters_file):
            pd.DataFrame(columns=['client_name', 'matter_name']).to_csv(self.matters_file, index=False)
    
    def add_time_entry(self, entry):
        """Add a new time entry"""
        df = pd.read_csv(self.time_entries_file)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        df.to_csv(self.time_entries_file, index=False)
    
    def get_daily_entries(self, date):
        """Get all entries for a specific date"""
        df = pd.read_csv(self.time_entries_file)
        return df[df['date'] == date.strftime('%Y-%m-%d')]
    
    def get_clients(self):
        """Get list of all clients"""
        df = pd.read_csv(self.clients_file)
        return df['client_name'].tolist()
    
    def get_matters(self, client):
        """Get matters for a specific client"""
        df = pd.read_csv(self.matters_file)
        return df[df['client_name'] == client]['matter_name'].tolist()
    
    def add_client(self, client_name):
        """Add a new client"""
        df = pd.read_csv(self.clients_file)
        if client_name not in df['client_name'].values:
            df = pd.concat([df, pd.DataFrame([{'client_name': client_name}])], ignore_index=True)
            df.to_csv(self.clients_file, index=False)
    
    def add_matter(self, client_name, matter_name):
        """Add a new matter for a client"""
        df = pd.read_csv(self.matters_file)
        new_matter = {'client_name': client_name, 'matter_name': matter_name}
        df = pd.concat([df, pd.DataFrame([new_matter])], ignore_index=True)
        df.to_csv(self.matters_file, index=False)
    
    def get_report_data(self, start_date, end_date):
        """Get time entries between dates for reporting"""
        df = pd.read_csv(self.time_entries_file)
        mask = (df['date'] >= start_date.strftime('%Y-%m-%d')) & (df['date'] <= end_date.strftime('%Y-%m-%d'))
        return df[mask]
