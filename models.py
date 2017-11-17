import http.client

import requests
import json

state_new_user = "state_new_user"
state_smth = "implement me!"
state_smth_2 = "implement me!"
state_smth_3 = "implement me!"
state_smth_4 = "implement me!"


class User:
    def __init__(self, uid: int, login: str = "no_login", state: str = "state_new_user"):
        self.uid = uid
        self.login = login
        self.state = state
        self.verified = False

    def __str__(self):
        return self.dump()

    def dump(self) -> str:
        return json.dumps({
            "uid": self.uid,
            "login": self.login,
            "state": self.state,
            "verified": self.verified,
        })


class Database:
    def __init__(self, addr_port: str = "http://80.211.129.44:8100"):
        """
        Обёртка для БД
        :param addr_port: адрес и порт удалённого сервера с БД
        """
        self.addr_port = addr_port

    def get_user(self, uid=None, login=None) -> User:
        """
        Достаём юзера из удалённой БД
        :param uid:
        :param login:
        :return:
        """
        if not uid and not login:
            raise BaseException("use uid OR login")

        url = "/get_user"
        if uid:
            params = {"uid": uid}
        else:
            params = {"login": login}

        r = requests.get(self.addr_port + url, params=params)
        if r.status_code not in (200, 404):
            raise BaseException('/get_user error, response text: -- ' + r.text)

        if r.status_code == 404:
            return None

        data = json.loads(r.text)
        u = User(
            data['uid'],
            data['login'],
            data['state']
        )
        return u

    def save_user(self, u: User):
        r = requests.post(self.addr_port + '/save_user', data={"user": u.dump()})
        if r.status_code != 200:
            raise BaseException('/save_user error, response text: --' + r.text)
        return


class Logic:
    def __init__(self, db: Database):
        self.db = db
        pass

    def handle(self, uid: int, message: str) -> str:
        """
        Общая логика бота

        :param uid: id юзера
        :param message: его сообщение
        :return: сообщение/кнопка, отсылаемое юзеру
        """

        # достаём юзера
        u = self.db.get_user(uid)
        if not u:
            # если это новый юзер
            self.db.save_user(User(uid, state=state_new_user))
            # сохраняем юзера в бд и возвращаем приветствие
            return "welcome to herd!"

        # юзер уже в бд

        # юзер не подтвердил свою личность (фотка паспорта / другое)
        if not u.verified:
            pass

        # юзер ...
        # ...
        return "not handled!"