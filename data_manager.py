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
        # Initialize time entries file
        if not os.path.exists(self.time_entries_file):
            pd.DataFrame(columns=[
                'date', 'client', 'matter', 'duration', 'narrative'
            ]).to_csv(self.time_entries_file, index=False)

        # Initialize clients file with sample data
        if not os.path.exists(self.clients_file):
            sample_clients = pd.DataFrame({
                'client_name': ['Sample Client']
            })
            sample_clients.to_csv(self.clients_file, index=False)

        # Initialize matters file with sample data
        if not os.path.exists(self.matters_file):
            sample_matters = pd.DataFrame({
                'client_name': ['Sample Client'],
                'matter_name': ['General']
            })
            sample_matters.to_csv(self.matters_file, index=False)

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
        try:
            df = pd.read_csv(self.clients_file)
            return df['client_name'].tolist() if not df.empty else []
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return []

    def get_matters(self, client):
        """Get matters for a specific client"""
        try:
            if not client:
                return []
            df = pd.read_csv(self.matters_file)
            return df[df['client_name'] == client]['matter_name'].tolist()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return []

    def add_client(self, client_name):
        """Add a new client"""
        if not client_name:
            return False, "Client name cannot be empty"

        try:
            df = pd.read_csv(self.clients_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['client_name'])

        if client_name in df['client_name'].values:
            return False, "Client already exists"

        df = pd.concat([df, pd.DataFrame([{'client_name': client_name}])], ignore_index=True)
        df.to_csv(self.clients_file, index=False)
        return True, f"Added client: {client_name}"

    def add_matter(self, client_name, matter_name):
        """Add a new matter for a client"""
        if not client_name or not matter_name:
            return False, "Client and matter name cannot be empty"

        try:
            df = pd.read_csv(self.matters_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=['client_name', 'matter_name'])

        # Check if matter already exists for this client
        if not df.empty and ((df['client_name'] == client_name) & (df['matter_name'] == matter_name)).any():
            return False, "Matter already exists for this client"

        new_matter = {'client_name': client_name, 'matter_name': matter_name}
        df = pd.concat([df, pd.DataFrame([new_matter])], ignore_index=True)
        df.to_csv(self.matters_file, index=False)
        return True, f"Added matter: {matter_name} for client: {client_name}"

    def get_report_data(self, start_date, end_date):
        """Get time entries between dates for reporting"""
        df = pd.read_csv(self.time_entries_file)
        mask = (df['date'] >= start_date.strftime('%Y-%m-%d')) & (df['date'] <= end_date.strftime('%Y-%m-%d'))
        return df[mask]