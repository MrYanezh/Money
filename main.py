import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QPushButton, QSpacerItem,
    QSizePolicy, QTextEdit, QScrollArea, QSplitter, QHBoxLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QGuiApplication
from PyQt6.QtCore import Qt
 # тест для проверки коммитов
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учёт платежей участников")
        self.setGeometry(0, 0, 800, 1000)
        
        # Основной виджет и вертикальный layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        # Создаем сплиттер для разделения верхней и нижней частей
        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_layout.addWidget(self.splitter)
        
        # Верхний виджет (поля ввода)
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout(self.top_widget)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Виджет для ввода количества участников
        self.create_participant_count_input()
        
        # Кнопка подтверждения количества участников
        self.confirm_button = QPushButton("Подтвердить количество")
        self.confirm_button.clicked.connect(self.create_name_input_fields)
        self.top_layout.addWidget(self.confirm_button)
        
        # Виджеты для ввода данных участников
        self.input_widgets = []
        
        # Добавляем верхний виджет в сплиттер
        self.splitter.addWidget(self.top_widget)
        
        # Нижний виджет (результаты)
        self.bottom_widget = QWidget()
        self.bottom_layout = QVBoxLayout(self.bottom_widget)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        # Область для вывода результатов
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setStyleSheet("font-family: monospace;")
        
        scroll = QScrollArea()
        scroll.setWidget(self.results_area)
        scroll.setWidgetResizable(True)
        self.bottom_layout.addWidget(scroll)
        
        # Добавляем кнопку "Копировать" в нижнюю часть
        self.copy_button = QPushButton("Копировать результаты")
        self.copy_button.setStyleSheet("font-weight: bold; padding: 5px;")
        self.copy_button.clicked.connect(self.copy_results)
        
        # Создаем контейнер для кнопки (чтобы выровнять по правому краю)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_button)
        button_layout.setContentsMargins(0, 5, 0, 0)
        
        self.bottom_layout.addWidget(button_container)
        
        # Добавляем нижний виджет в сплиттер
        self.splitter.addWidget(self.bottom_widget)
        
        # Настройки сплиттера
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 3)
        self.splitter.setHandleWidth(5)
        
        # Устанавливаем начальные размеры
        self.splitter.setSizes([200, 400])
    
    def create_participant_count_input(self):
        """Создаёт поле для ввода количества участников"""
        self.count_label = QLabel("Введите количество участников:")
        self.count_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.top_layout.addWidget(self.count_label)
        
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Введите число от 1 до 100...")
        self.count_input.setValidator(QIntValidator(1, 100))
        self.top_layout.addWidget(self.count_input)
    
    def create_name_input_fields(self):
        """Создаёт поля для ввода данных участников"""
        # Удаляем только виджеты ввода данных участников
        for widget in self.input_widgets:
            self.top_layout.removeWidget(widget)
            widget.deleteLater()
        self.input_widgets.clear()
        
        # Получаем количество участников
        try:
            num_participants = int(self.count_input.text())
        except ValueError:
            return
        
        # Создаём заголовок для полей
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_layout.addWidget(QLabel("Имя участника"), stretch=2)
        header_layout.addWidget(QLabel("Сколько заплатил"), stretch=1)
        header_layout.addWidget(QLabel("Коэффициент"), stretch=1)
        
        self.top_layout.addWidget(header_widget)
        self.input_widgets.append(header_widget)
        
        # Создаём поля для ввода данных
        for i in range(1, num_participants + 1):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            # Поле для имени
            name_input = QLineEdit()
            name_input.setPlaceholderText(f"Участник {i}")
            row_layout.addWidget(name_input, stretch=2)
            
            # Поле для суммы платежа
            payment_input = QLineEdit()
            payment_input.setPlaceholderText("0.00")
            payment_input.setValidator(QDoubleValidator(0, 999999, 2))
            payment_input.setAlignment(Qt.AlignmentFlag.AlignRight)
            row_layout.addWidget(payment_input, stretch=1)
            
            # Поле для коэффициента
            coeff_input = QLineEdit()
            coeff_input.setPlaceholderText("1.0")
            coeff_input.setValidator(QDoubleValidator(0.1, 10, 2))
            coeff_input.setAlignment(Qt.AlignmentFlag.AlignRight)
            row_layout.addWidget(coeff_input, stretch=1)
            
            self.top_layout.addWidget(row_widget)
            self.input_widgets.append(row_widget)
    
        # Добавляем кнопку сохранения
        save_button = QPushButton("Посчитать")
        save_button.setStyleSheet("font-weight: bold; margin-top: 10px;")
        save_button.clicked.connect(self.save_data)
        self.top_layout.addWidget(save_button)
        self.input_widgets.append(save_button)
        
        # Добавляем спейсер, чтобы поля ввода не растягивались
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.top_layout.addSpacerItem(spacer)
        
    def copy_results(self):
        """Копирует содержимое results_area в буфер обмена"""
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.results_area.toPlainText())
        self.copy_button.setText("Скопировано!")
        self.copy_button.setStyleSheet("font-weight: bold; padding: 5px; background-color: #4CAF50; color: white;")
        
        # Возвращаем исходный текст кнопки через 2 секунды
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, self.reset_copy_button)
    
    def reset_copy_button(self):
        """Восстанавливает исходный вид кнопки копирования"""
        self.copy_button.setText("Копировать результаты")
        self.copy_button.setStyleSheet("font-weight: bold; padding: 5px;")
        
    def save_data(self):
        """Собирает и выводит введённые данные"""
        self.results_area.clear()  # Очищаем предыдущие результаты
        
        participants_data = []
        
        # Проходим по всем виджетам и собираем данные
        for i in range(1, len(self.input_widgets) - 1):  # Пропускаем заголовок и кнопку
            row_widget = self.input_widgets[i]
            row_layout = row_widget.layout()
            
            name = row_layout.itemAt(0).widget().text().strip()
            payment = row_layout.itemAt(1).widget().text().strip().replace(',', '.')
            coefficient = row_layout.itemAt(2).widget().text().strip().replace(',', '.')
            
            if name or payment or coefficient:
                try:
                    participants_data.append({
                        'name': name if name else f"Участник {i}",
                        'payment': float(payment) if payment else 0.0,
                        'coefficient': float(coefficient) if coefficient else 1.0
                    })
                except ValueError as e:
                    self.results_area.append(f"Ошибка преобразования данных для участника {i}: {e}")
                    continue
        
        self.results_area.append("<div style='font-size: 1.2em;'>Список участников с платежами:</div>")
        # Создаем HTML-таблицу
        html = """
        <table border="1" cellpadding="4" style="border-collapse: collapse; width: 100%; font-family: monospace;">
        <tr>
            <th align="left" style="font-weight: normal;">№</th>
            <th align="left" style="font-weight: normal;">Имя</th>
            <th align="right" style="font-weight: normal;">Платеж</th>
            <th align="right" style="font-weight: normal;">Коэффициент</th>
        </tr>
        """

        for i, data in enumerate(participants_data, 1):
            html += f"""
        <tr>
            <td>{i}</td>
            <td>{data['name']}</td>
            <td align="right">{data['payment']:.2f}</td>
            <td align="right">{data['coefficient']:.2f}</td>
        </tr>
        """

        html += "</table>"
        self.results_area.append(html)

        # Общая сумма 
        sum_money = sum(data['payment'] for data in participants_data)
        self.results_area.append(f"Всего заплатили: {sum_money:.2f}")

        # Общий коэффициент 
        sum_coef = sum(data['coefficient'] for data in participants_data)
        # self.results_area.append(f"\nСуммарный коэффициент: {sum_coef:.2f}")

        # Сколько стоит единица нашего коэффициента?
        unit = sum_money / sum_coef if sum_coef != 0 else 0
        self.results_area.append(f"Единица коэффициента стоит: {unit:.2f}")

        # Сколько должен был заплатить каждый?
        list_portion = [round(data['coefficient'] * unit, 2) for data in participants_data]
        self.results_area.append("Каждый должен был заплатить:")
        for i, (data, amount) in enumerate(zip(participants_data, list_portion), 1):
            self.results_area.append(f"{data['name']}: {amount:.2f}")

        # Кто в минусе или плюсе?
        list_difference = [round(list_portion[i] - data['payment'], 2) for i, data in enumerate(participants_data)]
        self.results_area.append("Разница у каждого:")
        for i, (data, diff) in enumerate(zip(participants_data, list_difference), 1):
            self.results_area.append(f"{data['name']}: {diff:+.2f}")

        # Создаём списки бедных и богатых
        positive_balances = []
        negative_balances = []
        for i, data in enumerate(participants_data):
            difference = list_difference[i]
            if difference > 0:
                positive_balances.append((data['name'], difference))
            elif difference < 0:
                negative_balances.append((data['name'], abs(difference)))

        self.results_area.append("Должны заплатить:")
        for name, amount in positive_balances:
            self.results_area.append(f"{name}: {amount:.2f}")

        self.results_area.append("Должны получить:")
        for name, amount in negative_balances:
            self.results_area.append(f"{name}: {amount:.2f}")

        # Выбираем кто и кому должен перевести
        transfers = []
        while positive_balances and negative_balances:
            debtor, debt_amount = positive_balances.pop()
            creditor, credit_amount = negative_balances.pop()
            transfer_amount = min(debt_amount, credit_amount)
            transfers.append((debtor, creditor, transfer_amount))
            
            if debt_amount > credit_amount:
                positive_balances.append((debtor, debt_amount - credit_amount))
            elif credit_amount > debt_amount:
                negative_balances.append((creditor, credit_amount - debt_amount))

        # Красивый вывод результатов переводов
        self.results_area.append("\n" + "="*50)
        self.results_area.append(" Кто кому переводит ".center(50, "="))
        self.results_area.append("="*50)

        if not transfers:
            self.results_area.append("\nВсе платежи сбалансированы, переводы не требуются")
        else:
            for i, (from_person, to_person, amount) in enumerate(transfers, 1):
                self.results_area.append(f"{i}. {from_person} → {to_person}: {amount:.2f}")

        # Прокрутка к началу результатов
        self.results_area.verticalScrollBar().setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())