"""Это программный модуль фитнес-трекера.

Он обрабатывает данные для трехвидов тренировок:
для бега, спортивной ходьбы и плавания.
"""

from dataclasses import dataclass
from typing import Dict, Type, List


@dataclass
class InfoMessage:
    """
    Информационное сообщение о тренировке.

    Attributes
    ----------
    training_type : str
        Имя класса тренировки
    duration : float
        Длительность тренировки в часах
    distance : float
        Дистанция в км
    speed : float
        Средняя скорость
    calories : float
        Количество израсходованных килокалорий.

    Methods
    -------
    get_message()
        Возвращает строку сообщения с данными о тренировке.
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть строку сообщения с данными о тренировке."""
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration:.3f} ч.;'
            f' Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч;'
            f' Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки.

    Attributes
    ----------
    M_IN_KM : int
        Количество метров в одном километре
    MIN_IN_H : int
        Количество минут в одном часе
    LEN_STEP : float
        Длина одного шага или гребка
    action : int
        Количество действий(шагов или гребков)
    duration_h : float
        Длительность тренировки
    weight_kg : float
        Вес спортсмена.

    Methods
    -------
    get_distance() : float
        Расчёт дистанции, которую пользователь преодолел за тренировку
    get_mean_speed() : float
        Расчёт средней скорости движения во время тренировки
    get_spent_calories() : float
        Расчёт количества потраченных калорий за тренировку
    show_training_info() : InfoMessage
        Создание объекта сообщения о результатах тренировки
    duration_min() : int
        Перевод длительности тренировки из часов в минуты.
    """

    M_IN_KM = 1000
    MIN_IN_H = 60
    LEN_STEP = 0.65

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        """
        Метод инициализации.

        Parameters
        ----------
        action : int
            Количество действий(шагов или гребков)
        duration : float
            Длительность тренировки
        weight : float
            Вес спортсмена.
        """
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.

        Raises
        ------
        NotImplementedError
            Если не определен метод get_spent_calories().
        """
        raise NotImplementedError(
            f'Определить get_spent_calories() в {self.__class__.__name__}',
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )

    def duration_min(self) -> int:
        """Вернуть время тренировки в минутах."""
        return self.duration_h * self.MIN_IN_H


class Running(Training):
    """Тренировка: бег.

    Attributes
    ----------
    CALORIES_AVG_SPEED_MULTIPLIER : int
        Множитель средней скорости для расчета калорий
    CALORIES_AVG_SPEED_SHIFT : int
        Сдвиг средней скорости для расчета калорий.

    Methods
    -------
    get_spent_calories() : float
        Расчёт количества потраченных калорий за тренировку.
    """

    CALORIES_AVG_SPEED_MULTIPLIER = 18
    CALORIES_AVG_SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_AVG_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_AVG_SPEED_SHIFT
            )
            * self.weight_kg
            / self.M_IN_KM
            * self.duration_min()
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Attributes
    ----------
    height_m : float
        Рост спортсмена в метрах
    CALORIES_WEIGHT_MULTIPLIER : int
        Множитель веса для расчета калорий
    CALORIES_AVG_SPEED_AND_WEIGHT_MULTIPLIER : int
        Множитель средней скорости и веса для расчета калорий.

    Methods
    -------
    get_spent_calories() : float
        Расчёт количества потраченных калорий за тренировку.
    """

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_AVG_SPEED_AND_WEIGHT_MULTIPLIER = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ):
        """
        Метод инициализации.

        Parameters
        ----------
        action : int
            Количество действий(шагов или гребков)
        duration : float
            Длительность тренировки
        weight: float
            Вес спортсмена
        height : float
            Рост спортсмена в метрах.
        """
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_m)
            * self.CALORIES_AVG_SPEED_AND_WEIGHT_MULTIPLIER
            * self.weight_kg
        ) * self.duration_min()


class Swimming(Training):
    """Тренировка: плавание.

    Attributes
    ----------
    LEN_STEP : float
        Длина одного гребка
    CALORIES_AVG_SPEED_SHIFT : float
        Сдвиг средней скорости для расчета калорий
    CALORIES_WEIGHT_MULTIPLIER : int
        Множитель веса для расчета калорий
    length_pool_m : float
        Длина бассейна в метрах
    count_pool : int
        Количество заплывов, совершенных спортсменом.

    Methods
    -------
    get_mean_speed() : float
        Расчёт средней скорости движения во время тренировки
    get_spent_calories() : float
        Расчёт количества потраченных калорий за тренировку.
    """

    LEN_STEP = 1.38
    CALORIES_AVG_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        """
        Метод инициализации.

        Parameters
        ----------
        action : int
            Количество действий(шагов или гребков)
        duration : float
            Длительность тренировки
        length_pool : float
            Длина бассейна в метрах
        count_pool : float
            Количество заплывов, совершенных спортсменом.
        """
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool_m
            * self.count_pool
            / self.M_IN_KM
            / self.duration_h
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.CALORIES_AVG_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight_kg
        )


class InputDataError(Exception):
    """Неправильные входные данные."""

    pass


TRAININGS: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков.

    Raises
    ------
    InputDataError
        Если поступили неправильные данные.
    """
    try:
        return TRAININGS[workout_type](*data)
    except (KeyError, TypeError):
        raise InputDataError('Неправильные входные данные')


def main(training: Training) -> None:
    """Напечатать строку сообщений с данными о тренировке."""
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
