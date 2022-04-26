import json
import sys

import requests
from PyQt5 import QtWidgets

from Window import Ui_MainWindow


file_name = 'data.json'


class GeneralWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GeneralWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.send_button.clicked.connect(self.send_button)
        self.ui.save_button.clicked.connect(self.save_button)
        self.file_name = file_name
        self.load_savings()

    def load_savings(self):
        file_data = {
            'amount': self.ui.amount_field,
            'user_api_key': self.ui.user_api_field,
            'pay_pass': self.ui.pay_pass_field,
            'your_secret_key': self.ui.your_secret_key_field
        }
        try:
            with open(self.file_name, 'r') as read_file:
                data = json.load(read_file)
                for field in data:
                    if field in file_data:
                        file_data[field].setText(data[field])
        except FileNotFoundError:
            return  # 'file not found!'

    def send_button(self):
        amount = self.ui.amount_field.text()
        user_api_key = self.ui.user_api_field.text()
        pay_pass = self.ui.pay_pass_field.text()
        your_secret_key = self.ui.your_secret_key_field.text()
        Logic.send_money(self, amount, user_api_key, pay_pass, your_secret_key)

    def save_button(self):
        amount = self.ui.amount_field.text()
        user_api_key = self.ui.user_api_field.text()
        pay_pass = self.ui.pay_pass_field.text()
        your_secret_key = self.ui.your_secret_key_field.text()
        Logic.save_info(self, amount, user_api_key, pay_pass, your_secret_key)


class Logic(GeneralWindow):
    def __init__(self):
        super(Logic, self).__init__()

    def send_money(self, amount, user_api_key, pay_pass, your_secret_key):
        r = requests.get(
            f'https://market.csgo.com/api/v2/money-send/{amount}/'
            f'{user_api_key}?pay_pass={pay_pass}&key={your_secret_key}'
        )
        r_fields = (
            r.request.url,
            r.text
        )
        for field in r_fields:
            self.ui.textBrowser.append(field)

    def save_info(self, amount, user_api_key, pay_pass, your_secret_key):
        field_list = {
            'amount': amount,
            'user_api_key': user_api_key,
            'pay_pass': pay_pass,
            'your_secret_key': your_secret_key
        }
        with open(self.file_name, 'w') as write_file:
            json.dump(field_list, write_file, indent=4)
        self.ui.textBrowser.append(f'data in {self.file_name}'
                                   f'\nthe fields are: {field_list}')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = GeneralWindow()
    application.show()
    sys.exit(app.exec_())
