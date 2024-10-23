"""Gitlab Fetch Projects and Download"""
from gitlab_downloader.main import GitlabExporter


def main():
    """
    Main function
    :return:
    """
    project_name_to_export = input("Project name: ")
    exporter = GitlabExporter(project_name_to_export)
    exporter.export_project_by_name()

if __name__ == "__main__":
    main()
