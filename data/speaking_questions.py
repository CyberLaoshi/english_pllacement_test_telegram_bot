speaking_questions_set = [
    "Introduce yourself. Tell me about your hobbies and interests. What are your likes and dislikes?",
    "Think about a movie that you have recently seen. What happened in it? Did you enjoy it? Why or why not?",
    "Think about a popular restaurant near your home. Have you ever been there? What kind of food does it serve? How is the atmosphere of the restaurant? Describe it in as much detail as possible.",
    "Tell a story about an interesting experience. It can be something that you have personally experienced, or it can be made up. Describe this story in as much detail as possible."
]
task_questions = ""

for i, quest in enumerate(speaking_questions_set):
    task_questions = task_questions + f"✅ {i + 1}. {quest}\n"

speaking_task = f'''
Для выхода 👉 /exit 

Проводим устный тест. <b>Прочтите вопросы ниже:</b>
{task_questions}
Подготовьте ответы на максимально возможное количество вопросов. <b>Запишите свой ответ на аудио <a href='vocaroo.com'>здесь</a> и пришлите нам ссылку в сообщении. </b>
'''
