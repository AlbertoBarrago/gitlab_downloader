import os
import time

import requests

from dotenv import load_dotenv

load_dotenv()

# URI AND TOKEN
GITLAB_URL = os.getenv("GITLAB_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
EXPORT_FOLDER = os.getenv("EXPORT_FOLDER")

# Headers for the API request
headers = {
    "Private-Token": ACCESS_TOKEN
}


def start_project_export(project_id):
    """
    Start project export.
    :param project_id:
    :return:
    """
    export_url = f"{GITLAB_URL}/api/v4/projects/{project_id}/export"
    response = requests.post(export_url, headers=headers)
    if response.status_code == 202:
        print(f"Project export initiated for project ID {project_id}.")
        return True
    else:
        print(f"Failed to initiate export for project ID {project_id}: {response.text}")
        return False


def check_export_status(project_id):
    """
    Check export status.
    :param project_id:
    :return:
    """
    status_url = f"{GITLAB_URL}/api/v4/projects/{project_id}/export"
    response = requests.get(status_url, headers=headers)

    if response.status_code == 200:
        export_status = response.json().get("export_status", "none")
        if export_status == "finished":
            download_link = response.json().get("_links", {}).get("api_url")
            return {"status": "finished", "download_link": download_link}
        else:
            print(f"Current export status: {export_status}")
            return {"status": export_status}
    else:
        print(f"Failed to check export status for project ID {project_id}: {response.text}")
        return None


def download_export(project_id, project_name):
    """
    Download project export.
    :param project_id:
    :param project_name:
    :return:
    """
    download_url = f"{GITLAB_URL}/api/v4/projects/{project_id}/export/download"
    response = requests.get(download_url, headers=headers, stream=True)

    if response.status_code == 200:
        file_name = f"{EXPORT_FOLDER}/{project_name}_export.tar.gz"
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Project {project_name} exported and saved as {file_name}")
        return file_name
    else:
        print(f"Failed to download export for project {project_name}: {response.text}")
        return None


def export_project_by_name(project_name):
    """
    Export project by name.
    :param project_name:
    :return:
    """
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    project = get_project_by_name(project_name)
    if project:
        project_id = project["id"]
        project_name_safe = project["path_with_namespace"].replace("/", "_")

        if start_project_export(project_id):
            max_retries = 10
            retries = 0
            while retries < max_retries:
                status = check_export_status(project_id)
                if status and status["status"] == "finished":
                    download_export(project_id, project_name_safe)
                    break
                elif status["status"] in ["queued", "started"]:
                    time.sleep(30)
                    retries += 1
                else:
                    print("Export failed or timed out.")
                    break
            if retries == max_retries:
                print("Exceeded maximum retries for export status check.")
        else:
            print(f"Failed to start export for {project_name}.")


def get_project_by_name(project_name):
    """
    Get project by name.
    :param project_name:
    :return:
    """
    page = 1
    while True:
        response = requests.get(
            f"{GITLAB_URL}/api/v4/projects?search={project_name}&per_page=100&page={page}",
            headers=headers
        )
        if response.status_code != 200:
            print(f"Failed to fetch projects: {response.status_code} {response.text}")
            return None
        projects = response.json()
        if not projects:
            print(f"Project '{project_name}' not found.")
            return None
        for project in projects:
            if project["name"] == project_name or project["path_with_namespace"] == project_name:
                return project
        page += 1


if __name__ == "__main__":
    project_name_to_export = input("Project name: ")

    export_project_by_name(project_name_to_export)
