# функция для вывода уровня языка
def level_assessment(correct_total_num):
    score_level_scale = {
        "Elementary": "0-16",
        "Pre-intermediate": "17-25",
        "Intermediate": "26-33",
        "Upper intermediate": "34-42",
        "Advanced": "43-48"}

    for level, interval in score_level_scale.items():
        min_max_score = interval.split("-")
        # print(min_max_score)
        min_score, max_score = map(lambda x: int(x), min_max_score)  # нижнее и верхнее пороговые значения интервалов
        # print(f"min: {min_score}, max: {max_score}")
        if min_score <= correct_total_num <= max_score:
            return level
    return "Произошла ошибка в ходе проверки теста. Пожалуйста, обратитесь в поддержку."
