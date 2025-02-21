import requests
from bs4 import BeautifulSoup

def remove_html_tags(text):
    """Удаляет HTML-теги из строки с помощью BeautifulSoup."""
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator=" ").strip()
    return clean_text

def get_last_comment(project_id, issue, headers):
    link = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/{project_id}/issues/{issue["id"]}/comments'
    response = requests.get(link, headers=headers)
    
    # Проверка статуса ответа
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code} - {response.text}")
        return None
    
    # Проверка, что ответ не пустой
    if not response.text:
        print("Пустой ответ от сервера")
        return None
    
    try:
        comments = response.json()
        if comments.get("results"):
            comment_html = comments["results"][0]["comment_html"]
            # Удаляем HTML-теги
            clean_comment = remove_html_tags(comment_html)
            # Удаляем символы '|'
            clean_comment = clean_comment.replace('|', '')
            # Обрезаем комментарий, если он слишком длинный
            if len(clean_comment) > 300:
                clean_comment = clean_comment[:300] + " (...) *комментарий слишком длинный, откройте задачу, чтобы посмотреть его полностью*"
            return clean_comment
        else:
            print("Нет комментариев в ответе")
            return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")
        print(f"Ответ сервера: {response.text}")
        return None