import json

from bs4 import BeautifulSoup

# Открываем файл
with open('Mvideo.html') as f:
    # Парсим HTML-файл
    soup = BeautifulSoup(f, 'html.parser')

    # Ищем все элементы с нужными классами
    vacancy = soup.find(class_='vacancy').get_text(strip=True)
    salary = [value.get_text(strip=True) for value in soup.find_all(class_='salary')]
    # Счет курса валют
    if salary[1] == '₽':
        k = 1.0
    elif salary[1] == '$':
        k = 100.0
    elif salary[1] == '€':
        k = 105.0
    elif salary[1] == '₸':
        k = 0.210
    elif salary[1] == 'Br':
        k = 30.0
    if '-' in salary[0]:
        lower_bound, upper_bound = map(int, salary[0].split('-'))
        salary_rub = f'{lower_bound * k}-{upper_bound * k}'
    else:
        salary_rub = int(salary[0]) * k
    salary = salary_rub
    experience = [value.get_text(strip=True) for value in soup.find_all(class_='experience')]
    if len(experience) == 4:
        experience = f'{experience[1]}-{experience[3]}'
    else:
        experience = experience[1]
    company = soup.find(class_='company').get_text(strip=True)
    description = soup.find(class_='description').get_text(strip=True)
    skills = ', '.join(skill.get_text(strip=True) for skill in soup.find_all(class_='skills'))
    created_at = soup.find(class_='created_at').get_text(strip=True).replace('\xa0', ' ')

    # Создаем словарь с информацией
    job_info = {
        'vacancy': vacancy,
        'salary': salary,
        'experience': experience,
        'company': company,
        'description': description,
        'skills': skills,
        'created_at': created_at
    }

    # Преобразуем словарь в JSON
    job_info_json = json.dumps(job_info, ensure_ascii=False)

    print(job_info_json)
