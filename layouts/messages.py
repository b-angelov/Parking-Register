class Messages:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.messages = {
                "cancel": "Отказ",
                "save": "Запиши",
                "confirm save": "Желаете ли запишете посочените номера в регистъра?",
                "car number": "Номер МПС:",
                "stay": "Престой:",
                "paid": "Платено:",
                "left": "Напуснал:",
                "register a car": "Регистриране на автомобил",
                "view registered": "Преглед на регистрираните",
                "register title": "Регистрирай",
                "show registered title": "Покажи регистрираните",
                "about the app title": "За приложението",
                "about the app": f"Паркинг регистратор\n Конзолно приложение плюс графичен интерфейс \n с помощта на KivyMD 2.0.0 \n Борислав Ангелов 2025 © \n Версия: {self.APP_VERSION} \n https://github.com/b-angelov/Parking-Register",
                "sort by": "Сортиране по",
                "today": "Днешна дата",
                "now": "Час",
                "hour": "час",
                "submit":"изпрати",
                "sort":"Сортиране",
                "reset date": "Сверяване на часовника",
                "time dict" : {"day": "Ден", "week": "Седмица", "month": "Месец", "year": "Година", "all":"Всички данни"},
                "sort dict" : {"arrival":"Пристигане", "departure":"Заминаване", "present":"Присъствали през периода", "present_strict":"Присъстващи в момента" },
                "work date hint": "Изберете текуща дата",
                "work date error": "Датата не е променена",
                "work time hint": "Изберете текущ час",
                "work time error": "Часът не е променен",
                "rows per page": "Редове на страница:",
                "time unit": "Единица време",
                "rows count": "Брой редове",

            }