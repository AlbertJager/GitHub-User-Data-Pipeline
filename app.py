from github import Github, GithubException, Auth, NamedUser
import json
from pathlib import Path
import argparse
import dotenv
import os

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_user(username: str) -> NamedUser:
    """Returns user"""
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN не найден. Проверь .env файл.")

    g = Github(
        auth=Auth.Token(GITHUB_TOKEN)
    )  # No authentication has limits: 60 requests per hour, 10 requests per minute
    try:
        user = g.get_user(username)
    except GithubException as e:
        raise ValueError(f"Error {e.status}. {e.message}")
    else:
        return user


def get_user_data(user: NamedUser) -> dict:
    """Returns dictionary of user data"""

    user_data = {
        "login": user.login,
        "id": user.id,
        "name": user.name,
        "bio": user.bio,
        "location": user.location,
        "company": user.company,
        "blog": user.blog,
        "public_repos": user.public_repos,
        "followers": user.followers,
        "following": user.following,
        "created_at": str(user.created_at),
        "avatar_url": user.avatar_url,
        "html_url": user.html_url,
    }
    return user_data


def get_user_repos(user: NamedUser) -> list:
    """Returns dictionary of user's repos"""

    repos = user.get_repos()
    user_repos = []

    for repo in repos:
        repo_data = {
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "stargazers_count": repo.stargazers_count,
            "forks_count": repo.forks_count,
            "html_url": repo.html_url,
            "created_at": str(repo.created_at),
            "updated_at": str(repo.updated_at),
        }
        
        user_repos.append(repo_data)
    return user_repos


def parser_engine() -> argparse.Namespace:
    """Creates parser and returns arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument("userlogin", type=str, help="Github userlogin")
    parser.add_argument(
        "--repos", action="store_true", help="Saves user's repository information."
    )

    args = parser.parse_args()
    return args


def write_user_data(path: Path, user_data: dict, login: str) -> None:
    """Writes user data to file"""

    json_file = (path / f"{login}.json").resolve()

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)
        print("User data was written successfully")


def write_user_repos(path: Path, user_repos: list, login: str) -> None:
    """Writes user repos to file"""

    json_file = (path / f"{login}_repos.json").resolve()
    
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(user_repos, file, indent=4, ensure_ascii=False)
        print("User repos were written successfully")


def main():
    """Main function"""

    path = Path(__file__).resolve().parent
    args = parser_engine()

    user = get_user(args.userlogin)
    user_data = get_user_data(user)

    write_user_data(path, user_data, user.login)

    if args.repos:
        user_repos = get_user_repos(user)

        if not user_repos:
            print("User has no repositories")
        
        write_user_repos(path, user_repos, user.login)


if __name__ == "__main__":
    main()
