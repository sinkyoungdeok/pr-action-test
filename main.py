import os
import json
import requests

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH 환경변수가 설정되어 있지 않습니다.")
        return

    with open(event_path, "r") as f:
        event_data = json.load(f)

    # pull_request 이벤트가 아니면 종료
    if "pull_request" not in event_data:
        print("이 이벤트는 pull_request 이벤트가 아닙니다.")
        return

    # PR 정보 추출
    pull_request = event_data["pull_request"]
    pr_number = pull_request.get("number")
    pr_description = pull_request.get("body", "")
    print("Pull Request 번호:", pr_number)
    print("PR Description:")
    print(pr_description)
    print("=" * 50)

    repository = os.environ.get("GITHUB_REPOSITORY")
    if not repository:
        print("GITHUB_REPOSITORY 환경변수가 설정되어 있지 않습니다.")
        return
    owner, repo = repository.split("/")

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN 환경변수가 설정되어 있지 않습니다.")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 1. PR에 변경된 파일 목록과 patch 정보 가져오기
    files_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(files_url, headers=headers)
    if response.status_code != 200:
        print("PR 파일 목록을 가져오는데 실패했습니다:", response.status_code, response.text)
    else:
        pr_files = response.json()
        print("\nPR에서 변경된 파일들:")
        for file in pr_files:
            filename = file.get("filename")
            patch = file.get("patch", "")
            print(f"\n파일: {filename}")
            print("Patch:")
            print(patch)
            print("-" * 40)

    # 2. PR의 커밋 목록 가져오기
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits"
    response = requests.get(commits_url, headers=headers)
    if response.status_code != 200:
        print("PR 커밋 목록을 가져오는데 실패했습니다:", response.status_code, response.text)
    else:
        pr_commits = response.json()
        print("\nPR 커밋 목록:")
        for commit in pr_commits:
            sha = commit.get("sha")
            message = commit.get("commit", {}).get("message")
            print(f"\n커밋: {sha}")
            print("메시지:")
            print(message)
            print("-" * 40)

        # 3. 최신 두 커밋 비교 (커밋이 2개 이상일 때)
        if len(pr_commits) >= 2:
            base_commit = pr_commits[-2]["sha"]
            head_commit = pr_commits[-1]["sha"]
            compare_url = f"https://api.github.com/repos/{owner}/{repo}/compare/{base_commit}...{head_commit}"
            response = requests.get(compare_url, headers=headers)
            if response.status_code != 200:
                print("최신 두 커밋 비교에 실패했습니다:", response.status_code, response.text)
            else:
                compare_data = response.json()
                print("\n최신 두 커밋 비교:")
                print("Base Commit:", base_commit)
                print("Head Commit:", head_commit)
                print("총 변경 커밋 수:", compare_data.get("total_commits"))
                print("\n비교된 파일들:")
                for file in compare_data.get("files", []):
                    print("\n파일명:", file.get("filename"))
                    print("상태:", file.get("status"))
                    print("변경된 라인 수:", file.get("changes"))
                    print("Patch:")
                    print(file.get("patch", ""))
                    print("-" * 40)
        else:
            print("비교할 커밋이 2개 이상 존재하지 않습니다.")

if __name__ == "__main__":
    main()