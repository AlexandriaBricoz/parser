import csv
import bs4

def csv_reader(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        vacancies = list(reader)
    return headers, vacancies


def csv_filter(reader, list_naming):
    headers, vacancies = reader
    vacancies_dict = [dict(zip(headers, vacancy)) for vacancy in vacancies]
    for vacancy in vacancies_dict:
        for key in list_naming:
            if key in vacancy:
                vacancy[list_naming[key]] = vacancy.pop(key)
                if vacancy[list_naming[key]] == 'True':
                    vacancy[list_naming[key]] = 'Да'
                if vacancy[list_naming[key]] == 'False':
                    vacancy[list_naming[key]] = 'Нет'

    return vacancies_dict


def print_vacancies(data_vacancies, dic_naming):
    for vacancy in data_vacancies:
        for key in vacancy:
            if key == "Навыки":
                # Join skills with commas and print
                skills = vacancy[key].split()
                skills = ', '.join(skills)
                print(f"{key}: {skills}")
            elif key == "Описание":
                soup = bs4.BeautifulSoup(vacancy[key], 'html.parser')
                text_without_tags = soup.get_text()
                print(f"{key}: {text_without_tags}")
            else:
                print(f"{key}: {vacancy[key]}")
        print('\n')




# Создание словаря с русскоязычными названиями полей
dic_naming = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада",
    "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада",
    "area_name": "Название региона",
    "published_at": "Дата и время публикации вакансии"
}

# Чтение данных из CSV-файла
reader = csv_reader("/Users/aleksey/parser/vacancies_for_learn_demo.csv")

# Фильтрация данных
data_vacancies = csv_filter(reader, dic_naming)

# Вывод данных
print_vacancies(data_vacancies, dic_naming)
