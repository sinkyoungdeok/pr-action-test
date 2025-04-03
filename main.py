import os
import json

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH 환경변수가 설정되어 있지 않습니다.")
        return

    with open(event_path, "r") as f:
        event_data = json.load(f)

    pull_request = event_data.get("pull_request")
    if pull_request:
        pr_number = pull_request.get("number")
        print(f"Pull Request 번호: {pr_number}")
    else:
        print("이 이벤트는 pull_request 이벤트가 아닙니다.")

if __name__ == "__main__":
    main()