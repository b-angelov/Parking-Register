import sqlite3 as sq
import datetime


class Checking:
    messages = {
        "car number": "Номер на кола: ",
        "stay duration": "Времетраене на престой: ",
        "get option": "Изберете действие: ",
        "register car": "Регистриране на кола: ",
        "database clear": "Нулиране на базата данни: ",
        "show all": "Показване на всички записи: ",
        "confirm base clear": "Сигурни ли сте, че желаете да изтриете базата данни? Това ще изтрие необратимо всички "
                              "записи! ",
        "database cleaned": "Базата данни е нулирана. ",
        "undefined mode": "Няма зададен метод за тази команда! ",
        "stay out of range": "Престоят не може да бъде с продължителност, по-малка от една минута или повече от век!",
        "positive answer list": ['1', "y", "yes", "да"],
        "negative answer list": ['0', "n", "no", "не"],
        "quit list": ["q", "quit", "e", "exit", "и", "изход", "излез", 'вън']

    }
    time_modes = {"minutes": lambda x: int(x) / 60, "hours": lambda x: int(x), "days": lambda x: int(x) * 24,
                  "weeks": lambda x: (int(x) * 24) * 7, "months": lambda x: (int(x) * 24) * 30,
                  "years": lambda x: (int(x) * 24) * 365}
    price_list = {"hour": 2, "day": 10, "week": 70, "month": 280, "year": 3360}

    def __init__(self, time_mode="hours", dbname="parking.db"):
        self.db = dbname
        self.bases = Database(dbname)
        self.units_till_next = self.price_till_next()  # {"minutes": 30, "hours": 5, "days": 7, "weeks": 4, "months": 12, "years": 100}
        if time_mode not in self.time_modes:
            time_mode = "hours"
        self.time_mode = time_mode
        self.modes = {
            "register car": self.register_car,
            "show all": self.show_all,
            'database clear': self.base_clear,
            "test": self.tests
        }
        self.digitized_modes = list(enumerate(self.modes))
        if __name__ == "__main__":
            self.main()

    def main(self):
        mode = ""
        while mode.lower() not in self.messages["quit list"]:
            mode = input(self.messages["get option"])
            # current_mode = None
            if mode.isdigit() and int(mode) in range(len(self.digitized_modes)):
                current_mode = self.modes[self.digitized_modes[int(mode)][1]]
            elif mode in self.modes:
                current_mode = self.modes[mode]
            else:
                print(self.messages["undefined mode"])
                continue
            current_mode()

    def tests(self):
        testing = test(self)
        testing.tests()

    def register_car(self, time=None, **kwargs):
        left, paid = None,None
        if __name__ ==  "__main__":
            car_number = input(self.messages["car number"])
            stay_duration = input(self.messages['stay duration'])
        else:
            car_number = kwargs["car number"]
            stay_duration = kwargs['stay duration']
            left = kwargs["left"] if "left" in kwargs else None
            paid = kwargs["paid"] if "paid" in kwargs else None
        price = self.calculate_price(stay_duration)
        stay_duration = self.time_modes[self.time_mode](stay_duration)
        if not price:
            return
        print(price)
        if time:
            time = str(time).split(".")[0] + ".000001"
            print(time)
        self.bases.add(car_number.upper(), stay_duration, price=price, arrival_time=time, paid=paid, left=left)
        self.bases.save_changes()

    def price_till_next(self, price_list=None, update_mode=True, max_years: int = 100):
        if not price_list:
            price_list = self.price_list
        if "minutes" not in price_list.keys():
            price_list["minute"] = price_list["hour"] / 30
        price_list_keys = ["minute", "hour", "day", "week", "month", "year"]
        units_till_next = {}
        for idx, time_mode in enumerate(price_list_keys):
            time_mode_plural = time_mode + "s"
            units_till_next[time_mode_plural] = 0
            next_mode = price_list[time_mode] * max_years
            if idx + 1 < len(price_list_keys):
                next_mode = price_list[price_list_keys[idx + 1]]
            while units_till_next[time_mode_plural] * price_list[time_mode] < next_mode:
                units_till_next[time_mode_plural] += 1
        if update_mode:
            self.units_till_next = units_till_next
        return units_till_next

    def calculate_price(self, units, mode="default"):
        if units == 0:
            return units

        if mode == "default":
            mode = self.time_mode
        units = self.time_modes[mode](units)
        if units * 60 < self.units_till_next["minutes"]:
            return self.price_list["hour"] / 2
        elif self.units_till_next["hours"] >= units:
            return self.price_list["hour"] * units
        elif self.units_till_next["hours"] < units < 24:
            return self.price_list["day"]
        elif units < self.time_modes["days"](self.units_till_next["days"]):
            days = units // 24
            hours = units % 24
            return self.price_list["day"] * days + self.calculate_price(hours, "hours")
        elif units <= self.time_modes["days"](self.units_till_next["days"]):
            return self.price_list["week"]
        elif units <= self.time_modes["weeks"](self.units_till_next["weeks"]):
            weeks = units // 168
            days = units % 168
            return weeks * self.price_list["week"] + self.calculate_price(days, "hours")
        elif units <= self.time_modes["weeks"](self.units_till_next["weeks"]):
            return self.price_list["month"]
        elif units <= self.time_modes["months"](self.units_till_next["months"]):
            weeks = units // 720
            days = units % 720
            return weeks * self.price_list["month"] + self.calculate_price(days, "hours")
        elif units <= self.time_modes["months"](self.units_till_next["months"]):
            return self.price_list["year"]
        elif units <= self.time_modes["years"](self.units_till_next["years"]):
            weeks = units // 8640
            days = units % 8640
            return weeks * self.price_list["year"] + self.calculate_price(days, "hours")
        else:
            print(self.messages["stay out of range"])

    def show_all(self):
        fetched = self.bases.get_all()
        # print(*["\n".join([str(r) for r in row]) for row in fetched], sep="\n")
        self.bases.draw_on_console(fetched)

    def base_clear(self):
        confirm = input(self.messages["confirm base clear"])
        if confirm in self.messages['positive answer list']:
            self.bases.clear()
            self.bases.save_changes()
            print(self.messages['database cleaned'])

    def set_paid(self, id: int):
        """References method paid in Database class"""
        self.bases.update_paid(id)

    def set_left(self, id: int):
        """References method paid in Database class"""
        self.bases.update_left(id)

    def update_stay(self, id: int):
        arrival = self.bases.get_row(id)[3]
        departure = self.bases.get_row(id)[4]
        format = "%Y-%m-%d %H:%M:%S.%f"
        arrival = datetime.datetime.strptime(arrival, format)
        departure = datetime.datetime.strptime(departure, format)
        diff = departure - arrival
        diff = diff.total_seconds() / 3600
        price = self.calculate_price(diff, "hours")
        self.bases.update_stay(round(diff), id)
        self.bases.update_price(price, id)

    def all_for_a_time(self, date: str = None, selection_mode: str = "present_strict", select_by: str = "days",
                       select_count: int = 1, look_back = False):
        """Requires date string in format DD-MM-YYYY
        defaults to today, if no date specified.\n
            Selection mode parameter can be arrival, departure or present,
        where present returns records that are not currently left for the given date.\n
            Available selection modes are:\n
                By field - "departure" or "arrival"\n
                By presence - "present" - records between arrival and departure.\n
                And present_strict - present records with "left" equal to false. """
        # if not date:
        #     date = datetime.datetime.today()
        # else:
        #     # date = datetime.datetime.strptime(date, "%d-%m-%Y")
        #     date = self.bases.filled_datetime(date)
        # date = date + datetime.timedelta(hours=23.99)
        # print(date)
        date = self.bases.date_or_now(date)

        date = self.bases.datetime_to_dict(date)
        date.pop("second")
        return self.bases.select_by_time(select_by={select_by: select_count}, date_field=selection_mode, look_back=look_back, **date)

    def all_for_the_day(self, date: str = None, selection_mode: str = "present_strict"):
        """All records for the last week.
                See all_for_the_day for details."""
        return self.all_for_a_time(date, selection_mode, look_back=True)

    def all_for_the_week(self, week_end_date: str = None, selection_mode: str = "present_strict",
                         calendar_week: bool = False):
        """All records for the last week.
                See all_for_the_day for details."""
        date = self.bases.date_or_now(week_end_date)
        if calendar_week:
            week_day = date.weekday() + 1
            date -= datetime.timedelta(days=week_day)
        else:
            date = date - datetime.timedelta(days=7)
        return self.all_for_a_time(date, selection_mode=selection_mode, select_by="weeks")

    def all_for_the_month(self, month_end_date: str = None, selection_mode: str = "present_strict",
                          calendar_month: bool = False):
        """All records for the last week.
                See all_for_the_day for details."""
        date = self.bases.date_or_now(month_end_date)
        if calendar_month:
            exclude = date.day
        else:
            exclude = 30
        date -= datetime.timedelta(days=exclude)
        return self.all_for_a_time(date, selection_mode=selection_mode, select_by="months")

    def all_for_the_year(self, year_end_date: str = None, selection_mode: str = "present_strict",
                          calendar_year: bool = True):
        """All records for the last week.
                See all_for_the_day for details."""
        date = self.bases.date_or_now(year_end_date)
        if calendar_year:
            exclude = int(date.strftime("%j"))
        else:
            exclude = 365
        date -= datetime.timedelta(days=exclude)
        return self.all_for_a_time(date, selection_mode=selection_mode, select_by="years")

    def all_records(self,*args,**kwargs):
        return self.bases.get_all()


class Database:
    messages = {
        "date range error": "Датата е извън допустимите граници!",
        "invalid date format": "Неправилен формат за датата!",
        "value not found": "Стойността не е намерена!",
        "field names": {"ID":"ID", "car ID":"номер-кола", "country":"държава", "arrival":"дата на пристигане", "departure":"дата на заминаване", "stay":"времетраене на престой",
                   "price":"сума", "paid":"платено", "left":"напуснал"},
        "time names": {"year":"Година", "month":"Месец", "day":"Ден", "hour":"Час", "minute":"Минута","second":"Секунда"},
        "time names plural": {"years":"Години", "months":"Месеца", "days":"Дни", "hours":"Часа", "minutes":"Минути","seconds":"Секунди"}
    }

    def __init__(self, dbname=":memory:"):
        self.db = sq.connect(dbname)
        self.cursor = self.db.cursor()
        self.table = "parking"
        self.cursor.execute(
            f'''CREATE TABLE if not exists {self.table} (id integer primary key autoincrement,car_id text, country text, arrival text, departure text, stay integer(8), price real, paid bool, left bool)''')

    def add(self, car_id, stay, price=0, country="BG", paid=False, left=False, arrival_time: str = None):
        if not arrival_time:
            arrival = datetime.datetime.now()
        else:
            arrival = datetime.datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S.%f")
        try:
            departure = arrival + datetime.timedelta(hours=float(stay))
        except ValueError:
            print(self.messages["date range error"])
            return
        print(arrival, departure)
        query_dict = {

            "car_id": car_id,
            "country": country,
            "arrival": arrival,
            "departure": departure,
            "stay": stay,
            "paid": paid,
            "left": left,
            "price": price

        }
        self.cursor.execute(
            f"""INSERT INTO {self.table} VALUES (null,:car_id,:country,:arrival,:departure,:stay,:price,:paid,:left)""",
            query_dict)

    def get_all(self):
        db = self.cursor.execute(f"""select * from {self.table}""")
        return db.fetchall()

    def fetch_try(self, query_object):
        try:
            res = query_object.fetchone()
            if res is None:
                raise ValueError(self.messages["value not found"])
            return res
        except ValueError:
            return self.messages["value not found"]

    def get_row(self, field: int, field_name: str = "id"):
        db = self.cursor.execute(f"""select * from {self.table} where {field_name}={field}""")
        return self.fetch_try(db)

    def del_row(self, field, field_name: str = "id"):
        db = self.cursor.execute(f"""delete from {self.table} where {field_name}={field}""")
        self.save_changes()

    def clear(self, reset_primary_key=True):
        self.cursor.execute(f"delete from {self.table}")
        if reset_primary_key:
            self.cursor.execute(f"delete from sqlite_sequence where name='{self.table}'")

    def save_changes(self):
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()

    def update(self, values: dict, key_value=0, key_field="id"):
        if key_field not in values.keys():
            values[key_field] = key_value
        tables = [f"{key}=:{key}" for key in values if key != key_field]
        self.cursor.execute(f"update {self.table} set {','.join(tables)} where {key_field}=:id", values)
        self.save_changes()

    def switch_bool(self, column: str, key_value, single_mode=True, key_field="id"):
        result = self.cursor.execute(f"select {column} from {self.table} where {key_field}=?", [key_value])
        result = self.fetch_try(result)[0]
        if result:
            result = False
        else:
            result = True
        if not single_mode:
            return result
        self.update({column: result, key_field: key_value})

    def update_paid(self, id: int, key_field="id"):
        self.switch_bool("paid", id, key_field=key_field)

    def update_left(self, id: int, key_field="id"):
        self.switch_bool("left", id, key_field=key_field)

    def convert_date(self, date: str, time: str = "000000"):
        """Convert string to date"""
        given_date = date + time + ".000001"
        try:
            given_date = datetime.datetime.strptime(given_date, "%d%m%Y%H%M%S.%f")
        except ValueError:
            print(self.messages["invalid date format"])
            return
        return given_date

    def update_date(self, date: str, time: str, field: str, id: int, single_mode=True, key_field="id"):
        if time:
            date = self.convert_date(date, time)
        else:
            date = self.convert_date(date)
        if not single_mode:
            return date
        self.update({field: date}, id, key_field=key_field)

    def update_arrival(self, id: int, date: str, time=None, key_field="id"):
        self.update_date(date, time, "arrival", id, key_field=key_field)

    def update_departure(self, id: int, date: str, time=None, key_field="id"):
        self.update_date(date, time, "departure", id, key_field=key_field)

    def update_stay(self, value: int, id: int, key_field="id"):
        self.update({"stay": value}, id, key_field=key_field)

    def update_price(self, value: float, id: int, key_field="id"):
        self.update({"price": value}, id, key_field=key_field)

    def update_car(self, value: float, id: int, key_field="id"):
        self.update({"car_id": value}, id, key_field=key_field)

    def update_country(self, value: float, id: int, key_field="id"):
        self.update({"country": value}, id, key_field=key_field)

    def update_multiple(self, id: int, car_id: str = None, country: str = None, arrival: list = None,
                        departure: list = None,
                        stay: int = None, price: float = None, paid: bool = None, left: bool = None, key_field="id"):
        update_dict = {"id": id}
        if car_id:
            update_dict["car_id"] = car_id
        if country:
            update_dict["country"] = country
        if arrival:
            if len(arrival) == 1:
                arrival.append(None)
            arrival = self.update_date(arrival[0], arrival[1], "arrival", id, False)
            update_dict["arrival"] = arrival
        if departure:
            if len(departure) == 1:
                departure.append(None)
            departure = self.update_date(departure[0], departure[1], "departure", id, False)
            update_dict["departure"] = departure
        if stay:
            update_dict["stay"] = stay
        if price:
            update_dict["price"] = price
        if paid is not None:
            paid = self.switch_bool("paid", id, False)
            update_dict["paid"] = paid
        if left is not None:
            left = self.switch_bool("paid", id, False)
            update_dict["left"] = left
        self.update(update_dict, id, key_field=key_field)

    def select_by_time(self, select_by: dict = None, day: str = "01", month: str = "01", year: str = "2022",
                       hour: str = "00", minute: str = "00", date_field="departure", look_back: bool = False):
        """Select by mode accepts as key: "minutes", "hours", "days", "weeks", "months" and "years"
        value should be the count of the unit, given as a value."""
        if select_by:
            select_mode = list(select_by.keys())[0]
        if not select_by:
            select_by = {"days": 1}
            select_mode = "days"
        if "months" in select_by:
            select_by = {"days": 30}
        elif "years" in select_by:
            select_by = {"days": 365}
        if look_back:
            select_by = {k: -v for (k, v) in select_by.items()}
        time_dict = {"day": day, "month": month, "year": year, "hour": hour, "minute": minute}
        f = lambda v: str(v) if len(str(v)) > 1 else "0" + str(v)
        time_dict = {k: f(v) for k, v in time_dict.items()}
        timestamp = f'{time_dict["year"]}-{time_dict["month"]}-{time_dict["day"]} {time_dict["hour"]}:{time_dict["minute"]}'
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        next_stamp = timestamp + datetime.timedelta(**select_by)
        # timestamp = self.trim_timestamp(timestamp, select_mode[:-1])
        # next_stamp = self.trim_timestamp(next_stamp, select_mode[:-1])
        timestamp_trimmed = self.trim_timestamp(timestamp, select_mode[:-1])
        if look_back:
            timestamp, next_stamp = next_stamp, timestamp
        print(timestamp, next_stamp, timestamp_trimmed)
        query = f"select * from {self.table} where {date_field} between '{timestamp}' and '{next_stamp}'"
        if "present" in date_field:
            query = f"select * from {self.table} where departure > '{timestamp}' and arrival < '{next_stamp}'"
            if date_field != "present":
                query += " and left = 0"
        query = self.cursor.execute(query)
        return query.fetchall()

    def datetime_to_dict(self, datetime_obj):
        dt_dict = {}
        datetime_obj = str(datetime_obj).split()
        dt_dict = zip(["year", "month", "day", "hour", "minute", "second"],
                      datetime_obj[0].split("-") + [obj.split(".")[0] for obj in datetime_obj[1].split(":")])
        return dict(dt_dict)

    def dict_to_timestamp(self, time_dict: dict):
        timestamp = time_dict["year"]
        if "month" in time_dict:
            timestamp += "-" + time_dict["month"]
            if "day" in time_dict:
                timestamp += "-" + time_dict["day"]
                if "hour" in time_dict:
                    timestamp += " " + time_dict["hour"]
                    if "minute" in time_dict:
                        timestamp += ":" + time_dict["minute"]
                        if "second" in time_dict:
                            timestamp += ":" + time_dict["second"]
        return timestamp

    def trim_timestamp(self, timestamp: str, trim_to: str = "second"):
        timestamp = self.datetime_to_dict(timestamp)
        _times = list(timestamp.values())
        _names = list(timestamp.keys())
        if trim_to == "second":
            _times = _times
        elif trim_to == "minute":
            _times = _times[:-1]
        elif trim_to == "hour":
            _times = _times[:-2]
        elif trim_to == "day":
            _times = _times[:-3]
        elif trim_to == "month":
            _times = _times[:-4]
        elif trim_to == "year":
            _times = _times[:-5]
        return self.dict_to_timestamp(dict(zip(_names, _times)))

    def filled_datetime(self, _datetime: str = "2044"):
        _datetime = str(_datetime)
        datetime_list = ["2022", "01", "01", "00", "00", "00"]
        _datetime = _datetime.split("-")
        if len(_datetime) == 3:
            _datetime = _datetime[:2] + _datetime[2].replace(" ", ":").split(":")
        _datetime = [str(v) for v in _datetime]
        for index in range(len(_datetime)):
            datetime_list[index] = _datetime[index]
        timestamp = "-".join(datetime_list[:3]) + " " + ":".join(datetime_list[3:])
        timestamp = timestamp.split(".")[0] + ".000001"
        return datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    def date_or_now(self, date=None):
        if not date:
            return datetime.datetime.now()
        else:
            return self.filled_datetime(date)

    def get_time(self, hours, mode="hours"):
        kwarg = {mode:hours}
        hours = datetime.timedelta(**kwarg)
        d = datetime.datetime(1, 1, 1) + hours
        # return "%d-%d-%d %d:%d:%d.000001" % (d.year, d.month, d.day - 1, d.hour, d.minute, d.second)
        time_list = ["Years"]
        time = [d.year-1, d.month-1, d.day - 1, d.hour, d.minute, d.second]
        time_names_plural = self.time_names_list("plural")
        time_names_singular = self.time_names_list("singular")
        time = [f"{int(time[ind])} {time_names_singular[ind]}" if int(val) == 1 else f"{int(time[ind])} {time_names_plural[ind]}" for (ind,val) in enumerate(time) if val >= 1]
        return time

    def time_names_list(self, mode="singular"):
        if mode == "singular":
            return [self.messages["time names"]["year"], self.messages["time names"]["month"], self.messages["time names"]["day"], self.messages["time names"]["hour"], self.messages["time names"]["minute"], self.messages["time names"]["second"]]
        return [self.messages["time names plural"]["years"], self.messages["time names plural"]["months"], self.messages["time names plural"]["days"], self.messages["time names plural"]["hours"],self.messages["time names plural"]["minutes"], self.messages["time names plural"]["seconds"]]

    def field_names_list(self):
        m = self.messages["field names"]
        return [m["ID"], m["car ID"], m["country"], m["arrival"], m["departure"], m["stay"], m["price"], m["paid"], m["left"]]

    def draw_on_console(self, fetched):
        titles = [tuple(self.field_names_list())]
        console = ConsoleDraw()
        console.print_table(titles + fetched + titles)

    def modify_fields(self,row_list: list, car_id = None, country=None, arrival=None, departure=None, stay=None, price=None, paid=None, left=None ):
        """Functions are required as parameter values!"""
        funcs = [None, car_id, country, arrival, departure, stay, price, paid, left]
        funcs = [value if value else lambda x: x for value in funcs]
        data = [tuple([funcs[ind](val) for ind,val in enumerate(value)]) for value in row_list]
        return data


class ConsoleDraw:

    def __init__(self):
        self.a = 1

    def get_digits(self, stri):
        out = "0"
        for number in range(len(stri)):
            if stri[:number + 1].isdigit():
                out = stri[:number + 1]
                continue
            break
        return int(out)

    def split_by_digit(self, stri: str):
        lis = []
        index = 0
        first = 1
        valid = 0
        while len(stri) != index:
            if first:
                first = 0
                if stri[index - 1] != "~":
                    continue
                else:
                    valid = 1
            if stri[index].isdigit() and valid:
                multiplyer = self.get_digits(stri[index:])
                lis.append((stri[:index - 1], multiplyer))
                stri = stri[index + len(str(multiplyer)):]
                index = 0
                continue
            index += 1
            first = 1
            valid = 0
        return lis

    def dict_to_string(self, dictionary: list):
        return "".join([key[0] * key[1] for key in dictionary]).replace('\\N', "\n").replace('\\n', "\n")

    def print_out(self, string):
        return self.dict_to_string(self.split_by_digit(string))

    def rows_length(self, table_rows: list):
        rows_max_list = [[len(str(field)) for field in row] for row in table_rows]
        max_list = []
        for row in rows_max_list:
            for index, field in enumerate(row):
                if index not in range(len(max_list)):
                    max_list.append(field)
                else:
                    if max_list[index] < field:
                        max_list[index] = field
        return max_list

    def print_table(self, table_rows: list):
        max_list = self.rows_length(table_rows)
        row_length = sum(max_list)
        table_rows = [
            list(map(lambda field, idx: str(field) + " " * (idx - len(str(field))) + " ~1|~1 ", field, max_list)) for
            field in table_rows]
        table_row_strings = [self.print_out(
            f"~1_~{round(row_length * 1.22)}\n~1|~1 " + "".join(rows) + f" ~1\n~1‾~{round(row_length * 1.22)}") for rows
            in table_rows]
        print("\n".join(table_row_strings))


class test:

    def __init__(self, object):
        self.object = object

    def tests(self):
        if __name__ == "__main__":
            checking = self.object
            checking.calculate_price(167.99)
            checking.bases.update_multiple(3, car_id="ABC 11 DEF", paid=True, left=True, arrival=["26102022", "190000"],
                                           departure=["28102022", "203300"], country="BG")
            checking.bases.draw_on_console(checking.all_for_the_year("2022-09-27", selection_mode="present"))
            # print(checking.bases.select_by_time({"days": 2.5}, month=9, day=17, look_back=True, date_field="arrival"))
            # pattern = "~1_~100\n~1|~1 дата на пристигане ~1|~1 дата на заминаване ~1|~1 времетраене на престой ~1|~1 изплатена сума ~1|~1 номер на МПС ~1|~1 example ~1|~1 example|~1 example ~1|~1\n~1-~100"
            # print(drawer.print_out(pattern))
            # drawer.print_table([("ID","номер-кола","държава","дата на пристигане","дата на заминаване","времетраене на престой","сума","платено","напуснал"),(194, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.264132', '2023-06-13 14:31:13.264132', 6480, 2520.0, 0, 0), (195, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.413174', '2023-07-13 14:31:13.413174', 7200, 2800.0, 0, 0), (196, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.493739', '2023-08-12 14:31:13.493739', 7920, 3080.0, 0, 0), (197, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.648977', '2023-09-11 14:31:13.648977', 8640, 3360.0, 0, 0), (198, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.721137', '2023-09-11 15:31:13.721137', 8641, 3362.0, 0, 0), (199, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.837012', '2023-09-11 16:31:13.837012', 8642, 3364.0, 0, 0), (200, 'A 1111 BB', 'BG', '2022-09-16 14:31:13.916365', '2023-09-11 17:31:13.916365', 8643, 3366.0, 0, 0), (201, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.014656', '2023-09-11 18:31:14.014656', 8644, 3368.0, 0, 0), (202, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.076485', '2023-09-11 19:31:14.076485', 8645, 3370.0, 0, 0), (203, 'A 1111 BB', 'БГ', '2022-09-16 14:31:14.151270', '2023-09-18 19:31:14.151270', 8813, 3440.0, 0, 0), (204, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.212676', '2023-10-11 14:31:14.212676', 9360, 3640.0, 0, 0), (205, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.265137', '2024-09-05 14:31:14.265137', 17280, 6720.0, 0, 0), (206, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.328839', '2025-08-31 14:31:14.328839', 25920, 10080.0, 0, 0), (207, 'A 1111 BB', 'BG', '2022-09-16 14:31:14.390290', '2121-04-10 14:31:14.390290', 864000, 336000.0, 0, 0)])

            # checking.register_car("2022-09-19 12:21:22.000000")
            print(self.object.bases.filled_datetime("2022-02-03 11:11"), type(self.object.bases.filled_datetime()))
            self.register_on_date()
        else:
            pass

    def register_on_date(self):
        date = input("Изберете дата:")
        time = input("Изберете време:")
        _datetime = date.replace(" ", "") + " " + time.replace(" ", "")
        try:
            _datetime = datetime.datetime.strptime(_datetime, "%d%m%Y %H%M%S")
        except:
            print("Грешна дата!")
            return
        self.object.register_car(_datetime)

    def add_random_data(self, count: int=1, date_range: tuple=("2000-01-01", "2100-01-01")):
        import random
        import time
        time_format = '%Y-%m-%d %H:%M:%S'
        start,end = list(date_range)
        start,end = start + f" {random.randrange(0, 23)}:{random.randrange(0, 59)}:00",end + f" {random.randrange(0, 23)}:{random.randrange(0, 59)}:00"
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))
        ptime = lambda x=None: stime + random.random() * (etime - stime)
        rand_countr = ["BG","GB","FR","IT","RO","CZ","UKR","RU","SV","SLO","SL"]
        rand_country = lambda x=None: rand_countr[random.randrange(0,len(rand_countr))]
        rand_cyr = lambda x=None: chr(random.randrange(ord("А"),ord("Я")))
        rand_invalid_carid = lambda x=None: f"{rand_cyr()} {random.randrange(1000, 9999)} {rand_cyr()}{rand_cyr()}"
        rand_arrival =  lambda x=None: time.strftime(time_format, time.localtime(ptime())) + ".000001"

        for _ in range(count):
            rand_stay = random.randint(1,8760)
            rand_price = random.randint(1,100)
            self.object.bases.add(rand_invalid_carid(), rand_stay, self.object.calculate_price(rand_price), rand_country(), random.randrange(0,2), random.randrange(0,2),rand_arrival())

        self.object.bases.save_changes()



if __name__ == "__main__":
    Checking("hours")
