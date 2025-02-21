import requests
from datetime import datetime, timedelta, timezone
from getters import get_last_comment

def get_done_today_issues(API_KEY, USER_ID):
    today = datetime.now().strftime('%Y-%m-%d')


    headers = {
        'X-API-Key': API_KEY
    }

    # Получаем список проектов в рабочем пространстве
    projects_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/'
    response = requests.get(projects_url, headers=headers)
    if response.status_code != 200:
        print(f'Ошибка при получении проектов: {response.status_code}')
        exit()

    projects = response.json()

    # Открываем файл для записи
    output_file = 'fact_output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        # Записываем заголовок таблицы
        file.write('| Статус | Проект | Идентификатор задачи | Название задачи | Последний комментарий |\n')
        file.write('|-----|--------|----------------------|-----------------|-----------------------|\n')

        # Перебираем проекты и получаем задачи
        for project in projects['results']:
            project_id = project['id']
            issues_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/{project_id}/issues/'
            response = requests.get(issues_url, headers=headers)
            if response.status_code != 200:
                print(f'Ошибка при получении задач для проекта {project["name"]}: {response.status_code}')
                continue

            issues = response.json()

            # Фильтруем задачи, завершенные сегодня и назначенные на нужного пользователя
            closed_issues = [
                issue for issue in issues['results']
                if issue['state'] in ['1beeea67-fdd2-4a98-abd1-12bd64437158',
                                      '3a472e6e-c890-4ab5-9431-15755a872ab5',
                                      '31641b73-3414-4f9f-89a9-6c6faa508328',
                                      '93d2df03-f970-4073-984f-75fe673c3d9e',
                                      '0cc6336a-1b25-46cc-b4b8-af30b853bf7d',
                                      '07db8838-d8a2-44ef-be52-b0d473c0cfa8',
                                      '4fbb19f4-7d05-4b8c-9d51-2c75c55018b8',
                                      'ead72496-7a0f-457b-9ace-3e97ff33d195'] and
                   issue['completed_at'] and
                   issue['completed_at'].startswith(today) and
                   USER_ID in [assignee for assignee in issue.get('assignees', [])]
            ]

            if closed_issues:
                for issue in closed_issues:
                    comment = get_last_comment(project_id, issue, headers)
                    issue_link = (f'https://plane.it4retail.tech/it4retail/projects/{project_id}/issues/{issue["id"]}')
                    # Формируем строку для записи в файл
                    line = f'| :white_check_mark: | {project["name"]} | [{project["identifier"]}-{issue["sequence_id"]}]({issue_link}) | {issue["name"]} | {comment} |\n'
                    file.write(line)

def get_inwork_issues_alltime(API_KEY, USER_ID):
    headers = {
        'X-API-Key': API_KEY
    }

    # Список статусов для фильтрации
    STATUSES = [
        '158af1cd-3e6e-4667-966f-7deca46e15a6',
        'dce82d51-eb15-4735-9df9-2afb419901f8',
        '69f7b460-70ad-49bc-8953-9dd97581d188',
        'd36fce3c-501e-4df0-84c5-86cd64fd93f8',
        '2045fef5-9c62-4275-b586-6998e227b1ec',
        'd61c3f92-3eae-4590-97b1-e1b29c5ef9c8',
        '8888f57c-3f54-4129-862a-4adb8c1b333a',
        'a932229e-1e88-4264-a9bb-375f45cae27b'
    ]
        # Получаем список проектов в рабочем пространстве
    projects_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/'
    response = requests.get(projects_url, headers=headers)
    if response.status_code != 200:
        print(f'Ошибка при получении проектов: {response.status_code}')
        exit()
    projects = response.json()
    # Открываем файл для записи
    output_file = 'plan_output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        # Записываем заголовок таблицы
        file.write('| Статус | Проект | Идентификатор задачи | Название задачи | Последний комментарий |\n')
        file.write('|---|--------|----------------------|-----------------|-----------------------|\n')
        # Перебираем проекты и получаем задачи
        for project in projects['results']:
            project_id = project['id']
            issues_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/{project_id}/issues/'
            response = requests.get(issues_url, headers=headers)
            if response.status_code != 200:
                print(f'Ошибка при получении задач для проекта {project["name"]}: {response.status_code}')
                continue
            issues = response.json()
            # Фильтруем задачи по статусам и назначенному пользователю
            filtered_issues = [
                issue for issue in issues['results']
                if issue['state'] in STATUSES and
                   USER_ID in [assignee for assignee in issue.get('assignees', [])]
            ]
            if filtered_issues:
                for issue in filtered_issues:
                    comment = get_last_comment(project_id, issue, headers)
                    issue_link = (f'https://plane.it4retail.tech/it4retail/projects/{project_id}/issues/{issue["id"]}')
                    # Формируем строку для записи в файл
                    line = f'| :large_yellow_circle: | {project["name"]} | [{project["identifier"]}-{issue["sequence_id"]}]({issue_link}) | {issue["name"]} | {comment} |\n'
                    file.write(line)

def get_recently_updated_issues(API_KEY, USER_ID):
    # Получаем текущее время и время за 24 часа назад
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)

    headers = {
        'X-API-Key': API_KEY
    }

    # Список статусов для фильтрации (в работе и закрыта)
    STATUSES = [
        '1beeea67-fdd2-4a98-abd1-12bd64437158',  # Закрыта
        '3a472e6e-c890-4ab5-9431-15755a872ab5',  # Закрыта
        '31641b73-3414-4f9f-89a9-6c6faa508328',  # Закрыта
        '93d2df03-f970-4073-984f-75fe673c3d9e',  # Закрыта
        '0cc6336a-1b25-46cc-b4b8-af30b853bf7d',  # Закрыта
        '07db8838-d8a2-44ef-be52-b0d473c0cfa8',  # Закрыта
        '4fbb19f4-7d05-4b8c-9d51-2c75c55018b8',  # Закрыта
        'ead72496-7a0f-457b-9ace-3e97ff33d195',  # Закрыта
        '158af1cd-3e6e-4667-966f-7deca46e15a6',  # В работе
        'dce82d51-eb15-4735-9df9-2afb419901f8',  # В работе
        '69f7b460-70ad-49bc-8953-9dd97581d188',  # В работе
        'd36fce3c-501e-4df0-84c5-86cd64fd93f8',  # В работе
        '2045fef5-9c62-4275-b586-6998e227b1ec',  # В работе
        'd61c3f92-3eae-4590-97b1-e1b29c5ef9c8',  # В работе
        '8888f57c-3f54-4129-862a-4adb8c1b333a',  # В работе
        'a932229e-1e88-4264-a9bb-375f45cae27b'   # В работе
    ]

    # Получаем список проектов в рабочем пространстве
    projects_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/'
    response = requests.get(projects_url, headers=headers)
    if response.status_code != 200:
        print(f'Ошибка при получении проектов: {response.status_code}')
        exit()
    projects = response.json()

    # Открываем файл для записи
    output_file = 'actual_output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        # Записываем заголовок таблицы
        file.write('| Статус | Проект | Идентификатор задачи | Название задачи | Последний комментарий |\n')
        file.write('|---|--------|----------------------|-----------------|-----------------------|\n')
        
        # Перебираем проекты и получаем задачи
        for project in projects['results']:
            project_id = project['id']
            issues_url = f'https://plane.it4retail.tech/api/v1/workspaces/it4retail/projects/{project_id}/issues/'
            response = requests.get(issues_url, headers=headers)
            if response.status_code != 200:
                print(f'Ошибка при получении задач для проекта {project["name"]}: {response.status_code}')
                continue
            issues = response.json()
            
            # Фильтруем задачи по статусам, времени обновления и пользователю, обновившему задачу
            filtered_issues = [
                issue for issue in issues['results']
                if issue['state'] in STATUSES and
                   USER_ID in [assignee for assignee in issue.get('assignees', [])] and
                   issue.get('updated_by') == USER_ID and
                   issue.get('updated_at') and
                   one_day_ago <= datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00')) <= now
            ]
            
            if filtered_issues:
                for issue in filtered_issues:
                    comment = get_last_comment(project_id, issue, headers)
                    issue_link = f'https://plane.it4retail.tech/it4retail/projects/{project_id}/issues/{issue["id"]}'
                    
                    # Определяем эмодзи для статуса
                    status_emoji = ':white_check_mark:' if issue['state'] in [
                        '1beeea67-fdd2-4a98-abd1-12bd64437158',
                        '3a472e6e-c890-4ab5-9431-15755a872ab5',
                        '31641b73-3414-4f9f-89a9-6c6faa508328',
                        '93d2df03-f970-4073-984f-75fe673c3d9e',
                        '0cc6336a-1b25-46cc-b4b8-af30b853bf7d',
                        '07db8838-d8a2-44ef-be52-b0d473c0cfa8',
                        '4fbb19f4-7d05-4b8c-9d51-2c75c55018b8',
                        'ead72496-7a0f-457b-9ace-3e97ff33d195'
                    ] else ':large_yellow_circle:'
                    
                    # Формируем строку для записи в файл
                    line = f'| {status_emoji} | {project["name"]} | [{project["identifier"]}-{issue["sequence_id"]}]({issue_link}) | {issue["name"]} | {comment} |\n'
                    file.write(line)