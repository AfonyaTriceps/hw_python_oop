from dataclasses import dataclass
from typing import Dict, Type
from typing import Final


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: Final[int] = 1000
    MIN_IN_H: Final[int] = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,
                 weight: float,
                 ) -> None:
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
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )

    def duration_min(self):
        """Вернуть время тренировки в минутах."""
        return self.duration_h * self.MIN_IN_H


class Running(Training):
    """Тренировка: бег."""
    CALORIE_RATE_MULTIPLIER: Final[int] = 18
    CALORIE_RATE_SHIFT: Final[int] = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIE_RATE_MULTIPLIER * self.get_mean_speed()
                - self.CALORIE_RATE_SHIFT
            )
            * self.weight_kg
            / self.M_IN_KM
            * self.duration_min()
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_RATE_MULTIPLIER: Final[float] = 0.035
    CALORIE_RATE_SHIFT: Final[float] = 0.029

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,
                 weight: float,
                 height: float,
                 ):
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        return (
            self.CALORIE_RATE_MULTIPLIER * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_m)
            * self.CALORIE_RATE_SHIFT
            * self.weight_kg
        ) * self.duration_min()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIE_RATE_MULTIPLIER: Final[float] = 1.1
    CALORIE_RATE_SHIFT: Final[int] = 2

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,  # Кол-во заплывов
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (
            self.length_pool_m
            * self.count_pool
            / self.M_IN_KM
            / self.duration_h
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIE_RATE_MULTIPLIER)
            * self.CALORIE_RATE_SHIFT
            * self.weight_kg
        )


TRAININGS: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return TRAININGS[workout_type](*data)
    except KeyError:
        raise KeyError('Тренировка не найдена')
    except TypeError:
        raise TypeError("Превышено количество аргументов")


def main(training: Training) -> None:
    """Главная функция."""
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
