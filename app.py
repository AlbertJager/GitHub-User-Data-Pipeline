from github import Github, GithubException, Auth
import json
from pathlib import Path
import argparse
import dotenv
import os

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def get_userdata(username: str):
    '''Returns dictionary of user data'''
    
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN не найден. Проверь .env файл.")
    
    g = (
        Github(auth=Auth.Token(GITHUB_TOKEN))
    )  # No authentication has limits: 60 requests per hour, 10 requests per minute
    try:
        user = g.get_user(username)
    except GithubException as e:
        raise ValueError(f"Error {e.status}. {e.message}")
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
    
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)
        print("The file was written successfully")

def main():
    '''Main function'''
    
    path = Path(__file__).resolve().parent            
    args = parser_engine()
    user_data = get_userdata(args.userlogin)    
    write_json(path, user_data)


if __name__ == "__main__":
    main()