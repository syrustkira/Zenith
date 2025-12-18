
import os
import json
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class PersistencePod:
    def __init__(self, credentials_path="credentials.json", folder_id=None):
        self.creds_path = credentials_path
        self.folder_id = folder_id or os.getenv("DRIVE_FOLDER_ID")
        self.scopes = ['https://www.googleapis.com/auth/drive.file']
        self.service = self._init_drive()

    def _init_drive(self):
        """Initializes the Google Drive API service."""
        if not os.path.exists(self.creds_path):
            print(f"[!] Warning: {self.creds_path} not found. Cloud persistence disabled.")
            return None
        creds = service_account.Credentials.from_service_account_file(
            self.creds_path, scopes=self.scopes)
        return build('drive', 'v3', credentials=creds)

    def log_local(self, session_data: dict):
        """Saves a timestamped JSON log to the local logs/ directory."""
        if not os.path.exists("logs"):
            os.makedirs("logs")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/zenith_session_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)
        return filename

    def upload_to_drive(self, local_path):
        """Uploads the local log to the scoped Google Drive folder."""
        if not self.service:
            return None

        file_metadata = {
            'name': os.path.basename(local_path),
            'parents': [self.folder_id] if self.folder_id else []
        }
        
        media = MediaFileUpload(local_path, mimetype='application/json')
        
        try:
            file = self.service.files().create(
                body=file_metadata, 
                media_body=media, 
                fields='id'
            ).execute()
            print(f"[+] Cloud Persistence: https://drive.google.com/open?id={file.get('id')}")
            return file.get('id')
        except Exception as e:
            print(f"[!] Cloud Upload Failed: {str(e)}")
            return None

# --- TELEMETRY MODULE ---
class ZenithTelemetry:
    @staticmethod
    def calculate_cost(usage_stats: dict):
        """
        Calculates session cost based on OpenRouter pricing.
        Adjust rates based on your selected models.
        """
        # Example rates per 1M tokens (DeepSeek-R1)
        prompt_rate = 0.55 
        completion_rate = 2.19
        
        p_tokens = usage_stats.get("prompt_tokens", 0)
        c_tokens = usage_stats.get("completion_tokens", 0)
        
        cost = ((p_tokens / 1_000_000) * prompt_rate) + ((c_tokens / 1_000_000) * completion_rate)
        return round(cost, 4)