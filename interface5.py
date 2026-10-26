"""Учебный интерфейс платформы онлайн-аукционов (PyQt5)."""
import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QDoubleSpinBox, QDateTimeEdit, QFrame, QMessageBox,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QSizePolicy,
)


GREEN = "#24765b"
INK = "#173c32"
MUTED = "#71847c"
BG = "#f4f7f3"


LOTS = [
    {"title": "Винтажная фотокамера Зенит-ЕТ", "category": "Техника", "price": 185, "start": 120, "step": 5, "ends": "Сегодня, 20:45", "emoji": "Т", "bids": 12, "seller": "Илья К."},
    {"title": "Керамическая ваза ручной работы", "category": "Дом и интерьер", "price": 72, "start": 45, "step": 2, "ends": "Завтра, 18:00", "emoji": "Д", "bids": 8, "seller": "Мария В."},
    {"title": "Коллекционное издание «Мастер и Маргарита»", "category": "Книги", "price": 96, "start": 60, "step": 3, "ends": "Завтра, 21:30", "emoji": "К", "bids": 5, "seller": "Александр П."},
    {"title": "Горный велосипед Trek Marlin", "category": "Спорт", "price": 430, "start": 350, "step": 10, "ends": "Через 2 дня", "emoji": "С", "bids": 17, "seller": "Денис Р."},
]


class AuctionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Платформа онлайн-аукционов")
        self.resize(1440, 960)
        self.setMinimumSize(1100, 760)
        self.user = "Гость"
        self.role = "Покупатель"
        self.selected = LOTS[0]
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.setStyleSheet(f"""
            QWidget {{ color:{INK}; font-family:'Arial'; font-size:16px; }}
            QMainWindow {{ background:{BG}; }}
            QFrame#card {{ background:white; border:1px solid #e5ebe5; border-radius:16px; }}
            QLabel#muted {{ color:{MUTED}; }} QLabel#hero {{ font-size:36px; font-weight:700; }}
            QLabel#title {{ font-size:25px; font-weight:700; }}
            QPushButton {{ background:{GREEN}; color:white; border:0; border-radius:9px; padding:14px 21px; font-weight:600; min-height:22px; }}
            QPushButton:hover {{ background:#1b6049; }} QPushButton#secondary {{ color:{GREEN}; background:#eaf3ee; }}
            QPushButton#secondary:hover {{ background:#dcece2; }}
            QLineEdit,QTextEdit,QComboBox,QDoubleSpinBox,QDateTimeEdit {{ background:white; border:1px solid #dce5dd; border-radius:8px; padding:13px; min-height:24px; }}
            QTableWidget {{ background:white; border:1px solid #e5ebe5; border-radius:12px; gridline-color:#edf1ed; }}
            QHeaderView::section {{ background:#edf4ef; padding:9px; border:0; font-weight:600; }}
        """)
        self.pages = {}
        self.add_page("auth", self.auth_page())
        self.add_page("register", self.register_page())
        self.add_page("catalog", self.catalog_page())
        self.add_page("seller", self.seller_page())
        self.add_page("lot", self.lot_page())
        self.add_page("create", self.create_page())
        self.add_page("admin", self.admin_page())
        self.add_page("results", self.results_page())
        self.go("auth")

    def add_page(self, key, page):
        self.pages[key] = page
        self.stack.addWidget(page)

    def go(self, key):
        self.stack.setCurrentWidget(self.pages[key])

    def page(self, title=None, subtitle=None, nav=True):
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        if nav:
            bar = QWidget()
            bar.setFixedHeight(76)
            bar.setStyleSheet("background:white; border-bottom:1px solid #e5ebe5;")
            row = QHBoxLayout(bar)
            row.setContentsMargins(34, 14, 34, 14)
            brand = QLabel("Платформа онлайн-аукционов")
            brand.setStyleSheet(f"color:{GREEN};font-size:22px;font-weight:700;")
            row.addWidget(brand)
            row.addSpacing(22)
            for label, key in (("Аукционы", "catalog"), ("Результаты", "results")):
                b = QPushButton(label); b.setObjectName("secondary"); b.clicked.connect(lambda _, k=key: self.go(k)); row.addWidget(b)
            row.addStretch()
            if self.role == "Продавец":
                b = QPushButton("Мои лоты"); b.setObjectName("secondary"); b.clicked.connect(lambda: self.go("seller")); row.insertWidget(3, b)
            if self.role in ("Продавец", "Администратор"):
                b = QPushButton("＋  Создать лот"); b.clicked.connect(lambda: self.go("create")); row.addWidget(b)
            if self.role == "Администратор":
                b = QPushButton("Панель администратора"); b.setObjectName("secondary"); b.clicked.connect(lambda: self.go("admin")); row.addWidget(b)
            who = QLabel(f"●  {self.user}"); who.setStyleSheet("color:#527568;padding:0 10px;"); row.addWidget(who)
            out = QPushButton("Выйти"); out.setObjectName("secondary"); out.clicked.connect(lambda: self.go("auth")); row.addWidget(out)
            outer.addWidget(bar)
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(44, 34, 44, 42)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignTop)
        if title:
            h = QLabel(title); h.setObjectName("hero")
            h.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            layout.addWidget(h, 0, Qt.AlignTop)
        if subtitle:
            sub = QLabel(subtitle); sub.setObjectName("muted")
            sub.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            layout.addWidget(sub, 0, Qt.AlignTop)
        outer.addWidget(content)
        root.content = layout
        return root

    @staticmethod
    def card():
        f = QFrame(); f.setObjectName("card"); f.setFrameShape(QFrame.StyledPanel)
        return f

    def auth_page(self):
        p = self.page(nav=False)
        wrap = QVBoxLayout(); wrap.addStretch()
        card = self.card(); card.setMaximumWidth(560)
        c = QVBoxLayout(card); c.setContentsMargins(34, 32, 34, 32); c.setSpacing(15)
        logo = QLabel("Платформа онлайн-аукционов"); logo.setWordWrap(True); logo.setStyleSheet(f"color:{GREEN};font-size:29px;font-weight:700;")
        c.addWidget(logo); c.addWidget(QLabel("Добро пожаловать на аукцион"))
        c.addWidget(QLabel("Войдите, чтобы участвовать в торгах"))
        self.login = QLineEdit(); self.login.setPlaceholderText("Электронная почта")
        self.password = QLineEdit(); self.password.setPlaceholderText("Пароль"); self.password.setEchoMode(QLineEdit.Password)
        self.login_role = QComboBox(); self.login_role.addItems(["Покупатель", "Продавец", "Администратор"])
        c.addWidget(self.login); c.addWidget(self.password); c.addWidget(self.login_role)
        enter = QPushButton("Войти в систему"); enter.clicked.connect(self.login_action); c.addWidget(enter)
        reg = QPushButton("Создать аккаунт"); reg.setObjectName("secondary"); reg.clicked.connect(lambda: self.go("register")); c.addWidget(reg)
        hint = QLabel("Демо: введите любое имя и выберите роль"); hint.setObjectName("muted"); c.addWidget(hint)
        center = QHBoxLayout(); center.addStretch(); center.addWidget(card); center.addStretch()
        wrap.addLayout(center); wrap.addStretch(); p.content.addLayout(wrap)
        return p

    def login_action(self):
        email = self.login.text().strip()
        password = self.password.text()
        if not email or not password:
            QMessageBox.warning(self, "Не все поля заполнены", "Введите электронную почту и пароль.")
            return
        if "@" not in email:
            QMessageBox.warning(self, "Некорректная почта", "В адресе электронной почты должна быть собака (@).")
            self.login.setFocus()
            return
        self.user = email.split("@")[0] or "Участник"
        self.role = self.login_role.currentText()
        self.refresh_pages()
        self.go("seller" if self.role == "Продавец" else "catalog")

    def register_page(self):
        p = self.page("Создать аккаунт", "Присоединяйтесь к сообществу покупателей и продавцов")
        card = self.card(); form = QFormLayout(card); form.setContentsMargins(26, 24, 26, 24); form.setSpacing(14)
        self.reg_name = QLineEdit(); self.reg_name.setPlaceholderText("Как к вам обращаться")
        self.reg_email = QLineEdit(); self.reg_email.setPlaceholderText("name@example.com")
        self.reg_pass = QLineEdit(); self.reg_pass.setEchoMode(QLineEdit.Password); self.reg_pass.setPlaceholderText("Не менее 6 символов")
        self.reg_role = QComboBox(); self.reg_role.addItems(["Покупатель", "Продавец"])
        form.addRow("Имя", self.reg_name); form.addRow("Электронная почта", self.reg_email); form.addRow("Пароль", self.reg_pass); form.addRow("Роль", self.reg_role)
        p.content.addWidget(card); submit = QPushButton("Зарегистрироваться"); submit.clicked.connect(self.register_action); p.content.addWidget(submit, 0, Qt.AlignLeft)
        back = QPushButton("← Вернуться ко входу"); back.setObjectName("secondary"); back.clicked.connect(lambda: self.go("auth")); p.content.addWidget(back, 0, Qt.AlignLeft)
        return p

    def register_action(self):
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_pass.text()
        if not name or not email or not password:
            QMessageBox.warning(self, "Не все поля заполнены", "Заполните имя, электронную почту и пароль.")
            return
        if "@" not in email:
            QMessageBox.warning(self, "Некорректная почта", "В адресе электронной почты должна быть собака (@).")
            self.reg_email.setFocus()
            return
        if len(password) < 6:
            QMessageBox.warning(self, "Слишком короткий пароль", "Пароль должен содержать не менее 6 символов.")
            self.reg_pass.setFocus()
            return
        self.user = name; self.role = self.reg_role.currentText(); self.refresh_pages(); self.go("seller" if self.role == "Продавец" else "catalog")

    def catalog_page(self):
        p = self.page("Найдите свой следующий лот", "Редкие находки, любимые вещи и новые возможности — всё на одних торгах")
        controls = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("⌕  Поиск по названию лота")
        self.category = QComboBox(); self.category.addItems(["Все категории", "Техника", "Дом и интерьер", "Книги", "Спорт"])
        btn = QPushButton("Найти"); btn.clicked.connect(self.render_lots)
        controls.addWidget(self.search, 3); controls.addWidget(self.category, 1); controls.addWidget(btn); p.content.addLayout(controls)
        row = QHBoxLayout(); self.lot_grid = QGridLayout(); self.lot_grid.setSpacing(16); row.addLayout(self.lot_grid); p.content.addLayout(row)
        self.render_lots()
        return p

    def render_lots(self):
        while self.lot_grid.count():
            item = self.lot_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        query = self.search.text().lower().strip()
        cat = self.category.currentText()
        filtered = [x for x in LOTS if (not query or query in x["title"].lower()) and (cat == "Все категории" or x["category"] == cat)]
        for i, lot in enumerate(filtered):
            card = self.card(); card.setMinimumHeight(245)
            c = QVBoxLayout(card); c.setContentsMargins(20, 18, 20, 18); c.setSpacing(9)
            art = QLabel(lot["emoji"]); art.setAlignment(Qt.AlignCenter); art.setStyleSheet(f"background:#edf5ef;color:{GREEN};border-radius:12px;font-size:44px;font-weight:700;padding:12px;")
            c.addWidget(art); tag = QLabel(lot["category"]); tag.setObjectName("muted"); c.addWidget(tag)
            name = QLabel(lot["title"]); name.setWordWrap(True); name.setStyleSheet("font-size:16px;font-weight:700;"); c.addWidget(name)
            price = QLabel(f"Текущая ставка  ·  {lot['price']} BYN"); price.setStyleSheet(f"color:{GREEN};font-weight:700;font-size:16px;"); c.addWidget(price)
            meta = QLabel(f"↗ {lot['bids']} ставок     ◷ {lot['ends']}"); meta.setObjectName("muted"); c.addWidget(meta)
            open_btn = QPushButton("Смотреть лот"); open_btn.clicked.connect(lambda _, x=lot: self.open_lot(x)); c.addWidget(open_btn)
            self.lot_grid.addWidget(card, i // 3, i % 3)
        if not filtered:
            empty = QLabel("Ничего не найдено. Попробуйте изменить запрос."); empty.setObjectName("muted"); self.lot_grid.addWidget(empty, 0, 0)
        self.lot_grid.setColumnStretch(0, 1); self.lot_grid.setColumnStretch(1, 1); self.lot_grid.setColumnStretch(2, 1)

    def open_lot(self, lot):
        self.selected = lot; self.refresh_pages(); self.go("lot")

    def lot_page(self):
        p = self.page("Карточка лота", "Подробности и ход торгов")
        self.lot_info = QVBoxLayout(); p.content.addLayout(self.lot_info)
        back = QPushButton("← Назад к списку лотов"); back.setObjectName("secondary"); back.clicked.connect(lambda: self.go("catalog")); p.content.addWidget(back, 0, Qt.AlignLeft)
        return p

    def render_lot(self):
        while self.lot_info.count():
            item = self.lot_info.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        lot = self.selected
        card = self.card(); row = QHBoxLayout(card); row.setContentsMargins(26, 24, 26, 24); row.setSpacing(28)
        visual = QLabel(lot["emoji"]); visual.setAlignment(Qt.AlignCenter); visual.setMinimumSize(300, 280); visual.setStyleSheet(f"background:#edf5ef;color:{GREEN};border-radius:14px;font-size:112px;font-weight:700;"); row.addWidget(visual)
        details = QVBoxLayout(); row.addLayout(details, 1)
        details.addWidget(QLabel(lot["category"])); title = QLabel(lot["title"]); title.setObjectName("title"); title.setWordWrap(True); details.addWidget(title)
        details.addWidget(QLabel("Состояние: отличное · Продавец: " + lot["seller"]))
        desc = QLabel("Уникальный лот от владельца. Перед участием ознакомьтесь с условиями торгов и минимальным шагом ставки."); desc.setWordWrap(True); desc.setObjectName("muted"); details.addWidget(desc)
        price = QLabel(f"{lot['price']} BYN"); price.setStyleSheet(f"color:{GREEN};font-size:30px;font-weight:700;"); details.addWidget(price)
        details.addWidget(QLabel(f"Шаг ставки: {lot['step']} BYN     ·     {lot['bids']} ставок     ·     Завершение: {lot['ends']}"))
        self.bid_input = QDoubleSpinBox(); self.bid_input.setPrefix("BYN  "); self.bid_input.setDecimals(2); self.bid_input.setMinimum(lot["price"] + lot["step"]); self.bid_input.setValue(lot["price"] + lot["step"]); self.bid_input.setSingleStep(lot["step"]); details.addWidget(self.bid_input)
        bid = QPushButton("Сделать ставку"); bid.clicked.connect(self.place_bid); details.addWidget(bid)
        self.lot_info.addWidget(card)
        history = self.card(); hl = QVBoxLayout(history); hl.setContentsMargins(22, 18, 22, 18); hl.addWidget(QLabel("История торгов"))
        hl.addWidget(QLabel(f"{lot['bids']} участника уже сделали ставку · текущая цена растёт с каждым предложением")); self.lot_info.addWidget(history)

    def place_bid(self):
        if self.user == "Гость": QMessageBox.information(self, "Войдите в систему", "Чтобы участвовать в торгах, сначала войдите в аккаунт."); self.go("auth"); return
        amount = self.bid_input.value(); lot = self.selected
        if amount < lot["price"] + lot["step"]:
            QMessageBox.warning(self, "Ставка отклонена", f"Минимальная следующая ставка — {lot['price'] + lot['step']} BYN."); return
        lot["price"] = amount; lot["bids"] += 1; self.refresh_pages()
        QMessageBox.information(self, "Ставка принята", f"Ваша ставка {amount:.2f} BYN принята.")

    def seller_page(self):
        owned = [lot for lot in LOTS if lot["seller"] == self.user]
        p = self.page("Кабинет продавца", "Управляйте своими аукционами и следите за ставками покупателей")
        summary = QHBoxLayout()
        for value, label in ((str(len(owned)), "Мои лоты"), (str(sum(lot["bids"] for lot in owned)), "Получено ставок"),
                             (f"{sum(lot['price'] for lot in owned):.0f} BYN", "Текущая сумма лотов")):
            card = self.card(); box = QVBoxLayout(card); box.setContentsMargins(20, 16, 20, 16)
            number = QLabel(value); number.setStyleSheet(f"font-size:25px;font-weight:700;color:{GREEN};")
            box.addWidget(number); box.addWidget(QLabel(label)); summary.addWidget(card)
        p.content.addLayout(summary)
        actions = QHBoxLayout()
        create = QPushButton("＋  Создать новый лот"); create.clicked.connect(lambda: self.go("create")); actions.addWidget(create)
        browse = QPushButton("Перейти к аукционам"); browse.setObjectName("secondary"); browse.clicked.connect(lambda: self.go("catalog")); actions.addWidget(browse)
        actions.addStretch(); p.content.addLayout(actions)
        section = QLabel("Мои лоты"); section.setObjectName("title"); p.content.addWidget(section)
        if not owned:
            empty = self.card(); box = QVBoxLayout(empty); box.setContentsMargins(24, 20, 24, 20)
            box.addWidget(QLabel("Пока у вас нет опубликованных лотов."))
            box.addWidget(QLabel("Создайте первый аукцион — после публикации он появится здесь и в общем каталоге."))
            p.content.addWidget(empty)
        else:
            table = QTableWidget(len(owned), 4)
            table.setHorizontalHeaderLabels(["Лот", "Категория", "Текущая цена", "Ставки"])
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            for i, lot in enumerate(owned):
                for j, value in enumerate((lot["title"], lot["category"], f"{lot['price']} BYN", str(lot["bids"]))):
                    table.setItem(i, j, QTableWidgetItem(value))
            table.cellDoubleClicked.connect(lambda row, _col: self.open_lot(owned[row]))
            p.content.addWidget(table)
        return p

    def create_page(self):
        p = self.page("Создать лот", "Расскажите о товаре и задайте условия аукциона")
        card = self.card(); form = QFormLayout(card); form.setContentsMargins(24, 22, 24, 22); form.setSpacing(12)
        self.new_title = QLineEdit(); self.new_title.setPlaceholderText("Например, коллекционные часы")
        self.new_cat = QComboBox(); self.new_cat.addItems(["Техника", "Дом и интерьер", "Книги", "Спорт", "Другое"])
        self.new_desc = QTextEdit(); self.new_desc.setPlaceholderText("Состояние, особенности и комплектность"); self.new_desc.setMaximumHeight(90)
        self.new_price = QDoubleSpinBox(); self.new_price.setPrefix("BYN  "); self.new_price.setMaximum(10000000); self.new_price.setValue(50)
        self.new_step = QDoubleSpinBox(); self.new_step.setPrefix("BYN  "); self.new_step.setMaximum(100000); self.new_step.setValue(5)
        start = QDateTime.currentDateTime()
        self.start_time = QDateTimeEdit(start); self.start_time.setCalendarPopup(True); self.start_time.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.end_time = QDateTimeEdit(start.addDays(1)); self.end_time.setCalendarPopup(True); self.end_time.setDisplayFormat("dd.MM.yyyy HH:mm")
        form.addRow("Название лота", self.new_title); form.addRow("Категория", self.new_cat); form.addRow("Описание", self.new_desc); form.addRow("Начальная цена", self.new_price); form.addRow("Шаг ставки", self.new_step); form.addRow("Начало аукциона", self.start_time); form.addRow("Окончание аукциона", self.end_time)
        p.content.addWidget(card); create = QPushButton("Опубликовать лот"); create.clicked.connect(self.create_lot); p.content.addWidget(create, 0, Qt.AlignLeft)
        return p

    def create_lot(self):
        if not self.new_title.text().strip() or not self.new_desc.toPlainText().strip() or self.new_step.value() <= 0:
            QMessageBox.warning(self, "Проверьте данные", "Введите название, описание и положительный шаг ставки."); return
        if self.end_time.dateTime() <= self.start_time.dateTime():
            QMessageBox.warning(self, "Неверные даты", "Окончание аукциона должно быть позже его начала."); return
        category = self.new_cat.currentText()
        lot = {"title": self.new_title.text().strip(), "category": category, "price": self.new_price.value(), "start": self.new_price.value(), "step": self.new_step.value(), "ends": self.end_time.dateTime().toString("dd.MM.yyyy HH:mm"), "emoji": category[:1], "bids": 0, "seller": self.user}
        LOTS.insert(0, lot); self.selected = lot; self.refresh_pages()
        self.go("seller" if self.role == "Продавец" else "lot")
        QMessageBox.information(self, "Лот создан", "Аукцион опубликован в каталоге и добавлен в ваши лоты.")

    def admin_page(self):
        p = self.page("Панель администратора", "Контроль пользователей и опубликованных лотов")
        stats = QHBoxLayout()
        for n, label in (("128", "Пользователей"), (str(len(LOTS)), "Активных лотов"), ("24", "Завершённых торгов")):
            card = self.card(); c = QVBoxLayout(card); c.setContentsMargins(20, 16, 20, 16); value = QLabel(n); value.setStyleSheet(f"font-size:25px;font-weight:700;color:{GREEN};"); c.addWidget(value); c.addWidget(QLabel(label)); stats.addWidget(card)
        p.content.addLayout(stats)
        table = QTableWidget(len(LOTS), 4); table.setHorizontalHeaderLabels(["Лот", "Категория", "Текущая цена", "Продавец"]); table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i, lot in enumerate(LOTS):
            for j, value in enumerate((lot["title"], lot["category"], f"{lot['price']} BYN", lot["seller"])): table.setItem(i, j, QTableWidgetItem(value))
        p.content.addWidget(table); return p

    def results_page(self):
        p = self.page("Результаты торгов", "Следите за завершёнными аукционами и итоговой стоимостью")
        card = self.card(); card.setMaximumHeight(330)
        c = QVBoxLayout(card); c.setContentsMargins(24, 20, 24, 20); c.setAlignment(Qt.AlignTop)
        c.addWidget(QLabel("🏆  Завершённые аукционы"))
        table = QTableWidget(3, 4); table.setHorizontalHeaderLabels(["Лот", "Победитель", "Итоговая цена", "Статус"]); table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setColumnWidth(1, 180)
        table.setColumnWidth(2, 200)
        table.setColumnWidth(3, 150)
        table.horizontalHeader().setMinimumSectionSize(120)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table.verticalHeader().setDefaultSectionSize(42)
        table.setFixedHeight(190)
        results = [("Старинный настольный глобус", "Елена С.", "214 BYN", "Завершён"), ("Набор виниловых пластинок", "Михаил Т.", "86 BYN", "Завершён"), ("Чайный сервиз, 1960-е", "Анна Л.", "142 BYN", "Завершён")]
        for i, r in enumerate(results):
            for j, v in enumerate(r): table.setItem(i, j, QTableWidgetItem(v))
        c.addWidget(table); p.content.addWidget(card); return p

    def refresh_pages(self):
        # Rebuild role-aware navigation while preserving current screen.
        current = next((key for key, page in self.pages.items() if page is self.stack.currentWidget()), "catalog")
        for key in ("catalog", "seller", "lot", "create", "admin", "results"):
            old = self.pages[key]; idx = self.stack.indexOf(old); new = getattr(self, {"catalog":"catalog_page", "seller":"seller_page", "lot":"lot_page", "create":"create_page", "admin":"admin_page", "results":"results_page"}[key])()
            self.stack.removeWidget(old); old.deleteLater(); self.pages[key] = new; self.stack.insertWidget(idx, new)
        self.render_lots(); self.render_lot(); self.go(current if current in self.pages else "catalog")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuctionWindow()
    window.show()
    sys.exit(app.exec_())
