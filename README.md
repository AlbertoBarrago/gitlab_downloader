# Information
Download from gitlab your projects with v4 API refer to: 
https://docs.gitlab.com/ee/api/rest/

_Motivation_

Every day someone ask me to export something from X and import into Y (gitlab env) so...

##### ENV 
```dotenv
GITLAB_URL=""
ACCESS_TOKEN=""
EXPORT_FOLDER="./gitlab_exports"
```

##### START SCRIPT 
After set `.env`
```bash 
python3 gitlab-exporter
```

_Instructions_
- Write the name of the projects that you want download. 
- When download it's ready you get file `.tgz` in `gitlab_exports`

🍕 ENJOY 