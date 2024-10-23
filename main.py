"""Gitlab Fetch Projects and Download"""
from services.gitlab_service import GitlabExporter

if __name__ == "__main__":
    project_name_to_export = input("Project name: ")
    exporter = GitlabExporter(project_name_to_export)
    exporter.export_project_by_name()
