
import requests
import lxml

from bs4 import BeautifulSoup as bs
from re import sub
from datetime import datetime

class Currency_converter_class():

    URL_CBR = 'https://cbr.ru/scripts/XML_daily.asp?'

    Currency_dict = {}

    def __init__(self):
        self.main()

    def string_parser(self, input_string):
        parser_string = sub(r'\s+|\t', ' ', input_string.lower())
        string_array = parser_string.split(' ')
        if len(string_array) < 4:
            return -1
        if string_array[2] != '->':
            return -2
        try:
            input_value = int(string_array[0])
        except Exception as e:
            try:
                input_value = float(sub(r',', '.', string_array[0]))
            except Exception as e:
                return -3
        return (input_value, string_array[1], string_array[3])

    def currency_dict_fill(self, date_string):
        self.Currency_dict.setdefault('rub', '1')
        params = {'date_req':date_string}
        request = requests.get(self.URL_CBR, params)
        soup = bs(request.content, 'lxml')
        for tag in soup.findAll('valute'):
            self.Currency_dict.setdefault(tag.charcode.string.lower(), tag.value.string)
        return

    def currency_get(self, currency):
        try:
            currency_value_raw = self.Currency_dict[currency]
        except Exception as e:
            return -1
        currency_value = float(sub(r',', '.', currency_value_raw))
        return currency_value

    def main(self):
        flag = True
        while flag:
            print('\n Please, inter the a line with the name of two currencies in the format:' + \
                '\n\t number (int or float) currency_from -> currency_to')
            input_string = input(' > ')
            result_parser = self.string_parser(input_string)
            if   result_parser == -1:
                print('\n\t ERROR!!! You have entered too few arguments!')
            elif result_parser == -2:
                print('\n\t ERROR!!! Incorrect format of the entered string!')
            elif result_parser == -3:
                print('\n\t ERROR!!! You can only translate integer values!')
            else:
                date_string = datetime.today().strftime("%d/%m/%Y")
                if not self.Currency_dict:
                    self.currency_dict_fill(date_string)
                currrency_from_value = self.currency_get(result_parser[1])
                currrency_to_value = self.currency_get(result_parser[2])
                if (currrency_from_value < 0) or (currrency_to_value < 0):
                    print('\n\t ERROR!!! There is no such currency in the system!' + \
                        '\n\t\t Please make sure that you have entered the correct currency name!')
                else:
                    result_value = round(result_parser[0] * currrency_from_value / currrency_to_value, 3)
                    input_value  = round(result_parser[0], 3)
                    print(f'\n\t Answer: {input_value} {result_parser[1].upper()} = {result_value} {result_parser[2].upper()}')
            continuos_question = input('\n Do you want to repeat (Y) or exit the program (ANY OTHER)? > ')
            if not continuos_question.lower().startswith('y'): 
                flag = False
                print('')
        return 0

if __name__ == '__main__':
     Currency_converter_class()
