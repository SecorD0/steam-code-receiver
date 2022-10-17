import email
import imaplib
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup as BS

from utils.resource_path import resource_path
from windows.interface.main import Ui_main_window


class Main_window(QtWidgets.QWidget, Ui_main_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # --- Window setting
        self.setFixedSize(300, 149)
        self.setWindowIcon(QtGui.QIcon(resource_path('images/icons/app.ico')))

        # --- Button signals
        self.pushButton_getCode.clicked.connect(self.get_code)

    def get_imap(self, mail: str) -> str:
        domain = mail.split('@')[-1]
        if domain in ['rambler.ru', 'lenta.ru', 'autorambler.ru', 'myrambler.ru', 'ro.ru', 'rambler.ua']:
            return 'imap.rambler.ru'
        elif domain in ['outlook.com', 'hotmail.com']:
            return 'outlook.office365.com'
        elif domain == 'yandex.ru':
            return 'imap.yandex.ru'
        elif 'gmail' in domain:
            return 'imap.gmail.com'

    def get_code(self):
        address = ''.join(self.lineEdit_email.text().split())
        password = ''.join(self.lineEdit_password.text().split())
        text = None
        date = None
        try:
            self.label_time_value.setText('')
            with imaplib.IMAP4_SSL(self.get_imap(address)) as mail:
                mail.login(address, password)
                mail.select("inbox")
                result, data = mail.uid('search', None, 'FROM "noreply@steampowered.com"')
                result, data = mail.uid('fetch', data[0].split()[-1], '(RFC822)')
                message = email.message_from_bytes(data[0][1])
                date = datetime.strptime(message['Date'], '%a, %d %b %Y %H:%M:%S %z').astimezone().strftime(
                    '%d.%m.%Y %H:%M:%S')
                html = message.get_payload()[1].get_payload(decode=True)
                message = BS(html, 'html.parser')
                code = message.find('td', class_='title-48 c-blue1 fw-b a-center')
                if not code:
                    url = message.find('a', class_='link c-grey4')
                    if not url:
                        QtWidgets.QMessageBox.information(self, 'Error!', 'No letter was found, try again!',
                                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                    else:
                        text = url['href']

                else:
                    text = code.get_text(strip=True)

            if text:
                self.label_time_value.setText(date)
                self.lineEdit_code.setText(text)

        except ConnectionRefusedError:
            QtWidgets.QMessageBox.warning(self, 'Error!', "This email service isn't supported!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        except Exception as e:
            if str(e) == "b'LOGIN failed.'":
                QtWidgets.QMessageBox.warning(self, 'Error!', f'Wrong credentials!', QtWidgets.QMessageBox.Ok,
                                              QtWidgets.QMessageBox.Ok)

            else:
                QtWidgets.QMessageBox.warning(self, 'Error!', f'Something went wrong:\n'
                                                              f'{type(e)}\n'
                                                              f'{str(e)}', QtWidgets.QMessageBox.Ok,
                                              QtWidgets.QMessageBox.Ok)
