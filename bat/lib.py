from requests import get
from .conf import get_config

def hello_world():
    return "Hello World!"

def check_assignment(courseid: str, assignmentid: str, token: str):
    # TODO: get instance and credentials from config
    headers = {"Authorization": f"Bearer {token}"}
    r = get(f"https://utexas.instructure.com/api/v1/courses/{courseid}/assignments/{assignmentid}", headers=headers)
    # TODO: handle 401 unauthorized error, or other unknown error
    if r.status_code == 200:
        return "Assignment exists"
    if r.status_code == 404:
        return "Assignment does not exist"

# config needs to include args, if present
def check_assignment_cfg():
    cfg = get_config()
    return check_assignment(courseid=cfg.courseid, assignmentid=cfg.assignmentid, token=cfg.token)

