from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # Тип тренировки
    duration: float  # Длительность
    distance: float  # Дистанция в км
    speed: float  # Ср. скорость
    calories: float  # Кол-во килокалорий
    message: str = ('Тип тренировки: {training_type};'
                    ' Длительность: {duration:.3f} ч.;'
                    ' Дистанция: {distance:.3f} км;'
                    ' Ср. скорость: {speed:.3f} км/ч;'
                    ' Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # М в км
    MIN_IN_H: int = 60  # Мин в ч
    LEN_STEP: float = 0.65  # Длина шага

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,  # Длительность
                 weight: float,  # Вес
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18  # Коэф 1
    coeff_calorie_2: int = 20  # Коэф 2

    def get_spent_calories(self) -> float:
        dur_in_min = self.duration * self.MIN_IN_H  # Длительность в мин

        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * dur_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035  # Коэф 1
    coeff_calorie_2: float = 0.029  # Коэф 2

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,  # Длительность
                 weight: float,  # Вес
                 height: float,  # Рост
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        dur_in_min = self.duration * self.MIN_IN_H  # Длительность в мин
        return (self.coeff_calorie_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_2 * self.weight) * dur_in_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Длина шага
    coeff_calorie_1: float = 1.1  # Коэф 1
    coeff_calorie_2: int = 2  # Коэф 2

    def __init__(self,
                 action: int,  # Кол-во действий
                 duration: float,  # Длительность
                 weight: float,  # Вес
                 length_pool: float,  # Длина бассейна
                 count_pool: float,  # Кол-во заплывов
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_1)
                * self.coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking
                                                   }
    return type_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
