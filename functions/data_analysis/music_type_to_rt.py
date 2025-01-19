import matplotlib.pyplot as plt
import pandas as pd


def plot_avg_rt_by_music_type(trial_combined_path: str) -> None:
    """Функция для построения графика среднего времени реакции (RT) для каждого участника по типу музыки.

    Параметры:
    file_path (str): Путь к Excel файлу, содержащему данные с колонками 'music type', 'id participant', и 'RT'.
    """
    # Шаг 1: Чтение данных из Excel файла
    df = pd.read_excel(trial_combined_path)

    # Шаг 2: Группировка данных по участникам и типам музыки
    # Для каждого участника для каждого типа музыки вычисляем среднее значение RT
    grouped = df.groupby(["participant_id", "music_type"])["RT"].mean().unstack()

    # Шаг 3: Построение графика
    # Для каждого участника выводим 3 значения RT (для каждого типа музыки)
    grouped.plot(kind="bar", figsize=(10, 6))

    # Добавляем подписи и заголовок
    plt.title("Среднее время реакции по участникам и типам музыки")
    plt.xlabel("ID участника")
    plt.ylabel("Среднее время реакции (RT)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Шаг 4: Отображаем график
    plt.show()
