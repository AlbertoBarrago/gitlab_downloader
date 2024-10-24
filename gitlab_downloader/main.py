"""Gitlab Projects Downloader"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
EXPORT_FOLDER = os.getenv("EXPORT_FOLDER")

headers = {
    "Private-Token": ACCESS_TOKEN
}


class GitlabExporter:
    """
    Gitlab Exporter
    """
    def __init__(self, project_name):
        self.version = 1.0
        self.project_name = project_name
        self.project_id = None
        self.project_name_safe = None

    def start_project_export(self):
        """
        Start project export.
        :return:
        """
        export_url = f"{GITLAB_URL}/api/v4/projects/{self.project_id}/export"
        response = requests.post(export_url, headers=headers, timeout=10)
        if response.status_code == 202:
            print(f"Project export initiated for project ID {self.project_id}.")
            return True

        print(f"Failed to initiate export for project ID {self.project_id}: {response.text}")
        return False

    def check_export_status(self):
        """
        Check export status.
        :return:
        """
        status_url = f"{GITLAB_URL}/api/v4/projects/{self.project_id}/export"
        response = requests.get(status_url, headers=headers, timeout=10)

        if response.status_code == 200:
            export_status = response.json().get("export_status", "none")
            if export_status == "finished":
                download_link = response.json().get("_links", {}).get("api_url")
                return {"status": "finished", "download_link": download_link}

            print(f"Current export status: {export_status}")
            return {"status": export_status}

        print(f"Failed to check export status for project ID {self.project_id}: {response.text}")
        return None

    def download_export(self):
        """
        Download project export.
        :return:
        """
        download_url = f"{GITLAB_URL}/api/v4/projects/{self.project_id}/export/download"
        response = requests.get(download_url, headers=headers, stream=True, timeout=10)

        if response.status_code == 200:
            file_name = f"{EXPORT_FOLDER}/{self.project_name}_export.tar.gz"
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Project {self.project_name} exported and saved as {file_name}")
            return file_name

        print(f"Failed to download export for project {self.project_name}: {response.text}")
        return None

    def get_project_by_name(self):
        """
        Get project by name.
        :return:
        """
        page = 1
        while True:
            response = requests.get(
                f"{GITLAB_URL}/api/v4/projects?search={self.project_name}&per_page=100&page={page}",
                headers=headers,
                timeout=10
            )
            if response.status_code != 200:
                print(f"Failed to fetch projects: {response.status_code} {response.text}")
                return None
            projects = response.json()
            if not projects:
                print(f"Project '{self.project_name}' not found.")
                return None
            for project in projects:
                if self.project_name in (project["name"], project["path_with_namespace"]):
                    return project
            page += 1

    def export_project_by_name(self):
        """
        Export project by name.
        :return:
        """
        if not os.path.exists(EXPORT_FOLDER):
            os.makedirs(EXPORT_FOLDER)

        project = self.get_project_by_name()
        if project:
            self.project_id = project["id"]
            self.project_name_safe = project["path_with_namespace"].replace("/", "_")

            if self.start_project_export():
                max_retries = 10
                retries = 0
                while retries < max_retries:
                    status = self.check_export_status()
                    if status and status["status"] == "finished":
                        self.download_export()
                        break
                    if status["status"] in ["queued", "started"]:
                        time.sleep(30)
                        retries += 1
                    else:
                        print("Export failed or timed out.")
                        break
                if retries == max_retries:
                    print("Exceeded maximum retries for export status check.")
