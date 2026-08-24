from github import Github, GithubException, Auth
import json
from pathlib import Path
import argparse
import dotenv
import os
"""
Требования без изменений:

Работает с одним username
Корректно обрабатывает отсутствие пользователя
Красивый JSON с отступами
Код разбит минимум на функции
README с инструкцией запуска
Репозиторий на GitHub
"""

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
def get_path():
    '''Returns path to the script'''
    path = Path(__file__).resolve().parent 
    return path


def get_userdata(username: str):
    '''Returns dictionary of user data'''
    g = (
        Github(auth=Auth.Token(GITHUB_TOKEN))
    )  # No authentication has limits: 60 requests per hour, 10 requests per minute
    try:
        user = g.get_user(username)
    except GithubException as e:
        raise ValueError(f"Error {e.status}. User '{username}' not found.")
    else:
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
    

def parser_engine():
    '''Creates parser and returns arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("userlogin", type=str, help="Github userlogin")
    
    args = parser.parse_args()
    return args


def write_json(path, user_data):
    '''Writes data to file'''
    json_file = (path / f'{user_data["login"]}.json').resolve()
    
    if json_file.parent == path:
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)
    else:
        raise ValueError(fr"Invalid userlogin. Maybe it contains '\': {user_data["login"]}")    


def main():
    '''Main function'''
    path = get_path()
            
    args = parser_engine()
    user_data = get_userdata(args.userlogin)    
    write_json(path, user_data)


if __name__ == "__main__":
    main()