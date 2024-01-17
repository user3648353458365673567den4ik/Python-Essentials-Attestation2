# реализация класса Singleton для возможности ограничения создания instance'ов классов
class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)

        return cls.instance


# создание класса, который будет являться интерфейсом взаимодействия с файлами
class FileWorker(Singleton):
    def __init__(self, input_filename: str = "input.txt", output_filename: str = "output.txt", logging: bool = True):
        """
        FileWorker constructor
        :param input_filename: Input file name or file name as path (str)
        :param output_filename: Output file name or file name as path (str)
        :param logging: Param that show, will class print logs or no (bool)
        """

        # обработка исключения для типа данных входящих аргументов
        assert isinstance(input_filename, str)
        assert isinstance(output_filename, str)
        assert isinstance(logging, bool)

        self.input_file = input_filename
        self.output_file = output_filename
        self.logging = logging

        self.all_numbers: list[int] = []  # список всех валидных чисел в файле
        self.sum_of_numbers: int = 0  # сумма всех валидных чисел

    def __str__(self):  # обработка текстовой версии класса
        return f"File interface class for {self.input_file}"

    def __print_log(self, text):
        if not self.logging:
            return
        print(f"[FileWorker Logger] {text}")

    # служебный метод для чтения и записи всех валидных чисел из файла в поле класса
    def __get_all_numbers_from_file(self):
        """
        Method that realises file read functional and write it to a class variable
        :return: Method doesn't return anything
        """
        self.__print_log("File open process (get_all_numbers_from_file) has started.")
        with open(self.input_file, 'r') as file:  # открытие файла для чтения с помощью менеджера контекста
            self.all_numbers = []
            file_end = False

            while not file_end:  # итерация всех строчек файла
                number = file.readline()
                if not number:  # условие, существует ли строка
                    file_end = True
                    break

                try:
                    number = int(number)  # конвертация в int
                except ValueError:
                    self.__print_log("Incorrect value to convert to int, continued...")
                    continue

                self.__print_log(f"Number was added to list: {number}")
                self.all_numbers.append(number)  # добавление числа в поле класса

            self.__print_log("File open process (get_all_numbers_from_file) has stopped.")

    # служебный метод для сохранения текущего сохраненного результата в выходной файл
    def __save_result(self, update_data=False):
        """
        Method that saves last data about sum of all nums from input file
        :param update_data: Will method call __get_all_numbers_from_file() to update data
        :return: Method doesn't return anything
        """

        if update_data:  # повторное получение новых данныъ если мы передаем соответствующий параметр в метод
            self.__get_all_numbers_from_file()
            self.__print_log("save_result: data updated because of update parameter")

        self.__print_log("File open process (update_data) has started")
        with open(self.output_file, 'w+') as file:  # открытие/создание выходного файла с помощью менеджера контекста
            file.write(str(self.sum_of_numbers))  # запись значения из поля
            self.__print_log(f"Result has written to {self.output_file}: {self.sum_of_numbers}")

        self.__print_log("File open process (update_data) has stopped")

    def sum_all_numbers(self):  # метод для получения и сохранения суммы всех валидных чисел из входного файла
        self.__get_all_numbers_from_file()
        if not self.all_numbers:  # если в списке нет чисел - вернуть 0
            return 0

        self.sum_of_numbers = sum(self.all_numbers)  # суммируем все элементы списка
        self.__save_result()  # сохраняем результат

        return self.sum_of_numbers  # возвращаем результат


file_worker = FileWorker() # используйте FileWorker(logging=False) чтобы выключить логгер
file_worker.sum_all_numbers()
print(f"Класс для взаимодействия с файлами: {file_worker}")
print(f"Результат суммирования: {file_worker.sum_of_numbers}")
