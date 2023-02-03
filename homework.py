from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_TEMPLATE: ClassVar[str] = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        """Вернуть сообщение с параметрами тренировки."""
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """
    Базовый класс тренировки.
    Содержит константы для перевода километров в метры и часов в минуты,
    а также длину шага в метрах.
    Принимает количество шагов, время тренировки в часах, вес в килограммах.
    """

    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию тренировки в километрах."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в километрах в час."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "В дочерних классах не описан метод get_spent_calories."
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть объект, содержащий информацию о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """
    Тренировка: бег.
    Добавлены специальные константы для вычисления затраченных калорий.
    """

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.
    Добавлены константы для перевода километров в час в метры в секундах,
    метров в сантиметры.
    Добавлены специальные константы для вычисления затраченных калорий.
    Дополнительно принимает рост в сантиметрах.
    """

    MSEC_IN_KMHOUR: float = 0.278
    SM_IN_M: int = 100
    CALORIES_WEIGHT_FIRST_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_SECOND_MULTIPLIER: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CALORIES_WEIGHT_FIRST_MULTIPLIER * self.weight
                + (self.get_mean_speed() * self.MSEC_IN_KMHOUR) ** 2
                / self.height * self.SM_IN_M
                * self.CALORIES_WEIGHT_SECOND_MULTIPLIER
                * self.weight
            )
            * self.duration * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """
    Тренировка: плавание.
    Переопределена константа длины шага: изменена на длину гребка в метрах.
    Добавлены специальные константы для вычисления затраченных калорий.
    Дополнительно принимает длину бассейна в метрах и количество заплывов.
    """

    LEN_STEP: float = 1.38
    CALORIES_SPEED_SHIFT: float = 1.1
    CALORIES_SPEED_MULTIPLIER: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в километрах в час."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.CALORIES_SPEED_SHIFT)
            * self.CALORIES_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        "RUN": Running,
        "WLK": SportsWalking,
        "SWM": Swimming
    }
    if workout_type not in training_types:
        raise ValueError("Неправильный тип тренировки.")
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
