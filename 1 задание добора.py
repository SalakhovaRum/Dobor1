import requests
import json


def get_random_questions(questions_number):
    questions = []
    response = requests.get(f"http://jservice.io/api/random?count={questions_number}")
    questions_json = json.loads(response.text)
    for i in questions_json:
        questions.append(i["question"].replace("\\", ""))
    return questions


def get_questions(category_id, questions_number):
    questions = []
    response = requests.get(f"http://jservice.io/api/clues?category={category_id}")
    questions_json = json.loads(response.text)
    if not questions_json:
        print("В данной категории не найдено вопросов. Получаем " + str(questions_number) + " случайных вопросов")
        return get_random_questions(questions_number)
    elif len(questions_json) < questions_number:
        print("В данной категории присутствует только " + str(len(questions_json)) + " вопросов. Получим их.")
        for i in range(len(questions_json)):
            questions.append((questions_json[i])["question"].replace("\\", ""))
    else:
        for i in range(questions_number):
            questions.append((questions_json[i])["question"].replace("\\", ""))
    # print(questions)
    return questions


def get_category_list(n=100):
    category_lists = []
    response = requests.get(f"https://jservice.io/api/categories?count={n}")
    data = json.loads(response.text)
    for i in data:
        if len(i["title"]) > 3:
            category_lists.append(i)

    category_lists.sort(key=lambda x: x["id"])
    for category in category_lists:
        print(str(category["id"]) + ". " + category["title"])

    return category_lists


def get_category_by_id(category_lists):
    while True:
        category_id = int(
            input("Пожалуйста, введите идентификатор одной из категорий для дальнейшего получения вопросов: "))
        try:
            category = next(category for category in category_lists if category["id"] == category_id)
            break;
        except StopIteration:
            print("Категории с таким идентификатором не существует")

    print("Вы выбрали категорию " + category["title"] + ". Отличный выбор!\n")
    return category


def write_questions_to_file(questions):
    with open('result.txt', 'w') as f:
        for line in questions:
            f.write(f"{line}\n")
    print("Вопросы успешно записаны и находятся в файле result.txt")


def main():
    print('Доброе пожаловать в консольное приложение - викторину!\n')
    n = int(input("Введите количество категорий, которое вы хотите отобразить (максимум - 100 категорий): "))
    print("Список категорий, состоящий из идентификатора категории и названия категории: ")
    category_lists = get_category_list(n)
    category = get_category_by_id(category_lists)
    n = int(input("Введите количество вопросов, которое хотите получить "))
    questions = get_questions(category["id"], n)
    write_questions_to_file(questions)


if __name__ == '__main__':
    main()