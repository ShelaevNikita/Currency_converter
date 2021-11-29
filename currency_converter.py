
import requests
import lxml

from bs4 import BeautifulSoup as bs
from re import sub
from datetime import datetime

Special_symbol_dict = {'₽':'rub', 'A$':'aud', '₼':'azn', '£':'gbp', '֏':'amd', 'Br':'byn', 'лв':'bgn', 'R$':'brl', \
    'Ft':'huf', 'HK$':'hkd', 'dkr':'dkk', '$':'usd', '€':'eur', '₹':'inr', '₸':'kzt', 'C$':'cad', 'с':'kgs', \
    'C¥':'cny','L':'mdl', 'nkr':'nok', 'zł':'pln', 'lei':'ron', 'SDR':'xdr', 'S$':'sgd', 'SM':'tjs', '₺':'try', \
    'T':'tmt', "So'm":'uzs', '₴':'uah', 'Kč':'czk', 'skr':'sek', 'Fr':'chf', 'R':'zar', '₩':'krw', '원':'krw', 'J¥':'jpy'}

class Currency_converter_class():

    URL_CBR = 'https://cbr.ru/scripts/XML_daily.asp?'

    Currency_dict = {}

    def __init__(self):
        self.main()

    def string_parser(self, input_string):
        parser_string = sub(r'\s+|\t', ' ', input_string.lower())
        string_array = parser_string.split(' ')
        len_string_array = len(string_array)
        if len_string_array < 4:
            return -1
        if string_array[-2] != '->':
            return -2
        input_values = [0] * (len_string_array - 3)
        for i in range(0, len_string_array - 3):
            try:
                input_values[i] = int(string_array[i])
            except Exception as e:
                try:
                    input_values[i] = float(sub(r',', '.', string_array[i]))
                except Exception as e:
                    return -3
        return (input_values, string_array[-3], string_array[-1])

    def currency_dict_fill(self, date_string):
        self.Currency_dict.setdefault('rub', '1')
        params = {'date_req':date_string}
        request = requests.get(self.URL_CBR, params)
        soup = bs(request.content, 'lxml')
        for tag in soup.findAll('valute'):
            self.Currency_dict.setdefault(tag.charcode.string.lower(), tag.value.string)
        return

    def currency_get(self, currency):
        if currency in self.Currency_dict.keys():
            currency_value_raw = self.Currency_dict[currency_raw]
        elif currency in Special_symbol_dict.keys():
            currency_value_raw = self.Currency_dict[Special_symbol_dict[currency]]
        else:
            return -1
        currency_value = float(sub(r',', '.', currency_value_raw))
        return currency_value

    def input_array_number(self, input_values, currency_from_value, currency_to_value):
        len_input_values = len(input_values)
        output_values = [0] * len_input_values
        input_values_round = [0] * len_input_values
        for i in range(0, len_input_values):
            output_values[i] = round((input_values[i] * currency_from_value / currency_to_value), 3)
            input_values_round[i] = round(input_values[i], 3)
        return (input_values_round, output_values)

    def main(self):
        flag = True
        while flag:
            print('\n Please, inter the a line with the name of two currencies in the format:' + \
                '\n\t "numbers (int or float) currency_from -> currency_to"')
            input_string = input(' > ')
            print('')
            result_parser = self.string_parser(input_string)
            if   result_parser == -1:
                print('\t ERROR!!! You have entered too few arguments!')
            elif result_parser == -2:
                print('\t ERROR!!! Incorrect format of the entered string!')
            elif result_parser == -3:
                print('\t ERROR!!! You can only translate integer or float values!')
            else:
                date_string = datetime.today().strftime("%d/%m/%Y")
                if not self.Currency_dict:
                    self.currency_dict_fill(date_string)
                currency_from_value = self.currency_get(result_parser[1])
                currency_to_value = self.currency_get(result_parser[2])
                if (currency_from_value < 0) or (currency_to_value < 0):
                    print('\t ERROR!!! There is no such currency in the system!' + \
                        '\t\t Please make sure that you have entered the correct currency name!')
                else:
                    result_values = self.input_array_number(result_parser[0], currency_from_value, currency_to_value)
                    currency_from_name = result_parser[1].upper()
                    currency_to_name   = result_parser[2].upper()
                    for i in range(0, len(result_values[0])):
                        print(f'\t {result_values[0][i]} {currency_from_name} = {result_values[1][i]} {currency_to_name}')
            continuos_question = input('\n Do you want to repeat (Y) or exit the program (ANY OTHER)? > ')
            if not continuos_question.lower().startswith('y'): 
                flag = False
                print('')
        return 0

if __name__ == '__main__':
     Currency_converter_class()
