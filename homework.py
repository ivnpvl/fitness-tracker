class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, new_training: Training) -> None:
        self.training_type = new_training.__class__.__name__
        self.duration: float = round(new_training.duration, 3)
        self.distance: float = round(new_training.get_distance(), 3)
        self.speed: float = round(new_training.get_mean_speed(), 3)
        self.calories = new_training.get_spent_calories()
    
    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.)')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    KMHOUR_TO_MSEC: float = 1000 / 3600 
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.mean_speed = self.get_mean_speed()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_FIRST_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_SECOND_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height / 100

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_FIRST_MULTIPLIER * self.weight 
                + (self.CALORIES_WEIGHT_SECOND_MULTIPLIER * self.weight
                * (self.mean_speed * self.KMHOUR_TO_MSEC)**2 / self.height))
                * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

