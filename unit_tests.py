#!/usr/bin/env python3

import unittest
import random

import currency_converter

class Test_unit_tests(unittest.TestCase):

    MAX_VALUES = 10

    Special_symbols = currency_converter.Special_symbol_dict
    All_currency = [v for k, v in Special_symbols.items()]

    def setUp(self):
        self.Converter = currency_converter.Currency_converter_class()

    def generator_currency_value(self):
        return [round((random.random() * random.randint(1, 100)), 5) for _ in range(0, self.MAX_VALUES)]

    def test_parser(self):
        number_spaces = random.randint(1, 100)
        string_spaces = ' ' * number_spaces
        currency_value = self.generator_currency_value()
        currency_value_string = ' '.join([str(value) for value in currency_value])

        values_lenght = len(self.All_currency) - 1
        currency_from = self.All_currency[random.randint(0, values_lenght)]
        currency_to   = self.All_currency[random.randint(0, values_lenght)]

        test_string = f'{string_spaces}11.12.21{string_spaces}{currency_value_string}{string_spaces}' + \
            f'{currency_from}{string_spaces}\t->\t{string_spaces}{currency_to}{string_spaces}'
        result_test = ('11/12/2021', currency_value, currency_from, currency_to)

        result = self.Converter.string_parser(test_string)

        self.assertEqual(result, result_test, ' ERROR in string_parser! ')

    def test_input_array_number(self):
        currency_value = self.generator_currency_value()

        currency_from_value = round(random.random() * 100, 5)
        currency_to_value   = round(random.random() * 100, 5)
        output_test_result = [round((currency_value[i] * currency_from_value / currency_to_value), 3) 
                              for i in range(0, 10)]

        input_test_result  = [round(elem, 3) for elem in currency_value]
        result_test = (input_test_result, output_test_result)

        result = self.Converter.input_array_number(currency_value, currency_from_value, currency_to_value)

        self.assertEqual(result, result_test, ' ERROR in input_array_number! ')

    def test_currency_dict_fill(self):
        date_string = '10/12/2021'
        dict_length_start = len(self.Converter.Currency_dict.items())

        self.Converter.currency_dict_fill(date_string)
        dict_length_end   = len(self.Converter.Currency_dict.items())

        currency_usd = self.Converter.Currency_dict['usd']
        currency_eur = self.Converter.Currency_dict['eur']
        currency_rub = self.Converter.Currency_dict['rub']

        self.assertEqual(dict_length_start, 0, ' ERROR in dict_length_start! ')
        self.assertEqual(dict_length_end, len(self.All_currency) - 1, ' ERROR in dict_length_end! ')

        self.assertEqual(currency_rub, '1', ' ERROR in Currency_dict! ')
        self.assertEqual(currency_usd, '73,5998', ' ERROR in Currency_dict! ')
        self.assertEqual(currency_eur, '83,3444', ' ERROR in Currency_dict! ')

        self.assertFalse('hhh' in self.Converter.Currency_dict, ' ERROR in Currency_dict! ')

    def test_currency_get(self):
        date_string = '10/12/2021'
        self.Converter.currency_dict_fill(date_string)

        usd_value = self.Converter.currency_get('usd')
        eur_value = self.Converter.currency_get('eur')
        rub_value = self.Converter.currency_get('rub')

        usd_value_symbol = self.Converter.currency_get('$')
        eur_value_symbol = self.Converter.currency_get('€')
        rub_value_symbol = self.Converter.currency_get('₽')

        self.assertEqual(rub_value, 1, ' ERROR in rub_value! ')
        self.assertEqual(usd_value, 73.5998, ' ERROR in usd_value! ')
        self.assertEqual(eur_value, 83.3444, ' ERROR in eur_value! ')

        self.assertEqual(rub_value_symbol, rub_value, ' ERROR in rub_value_symbol! ')
        self.assertEqual(usd_value_symbol, usd_value, ' ERROR in usd_value_symbol! ')
        self.assertEqual(eur_value_symbol, eur_value, ' ERROR in eur_value_symbol! ')

    def test_currency_dict_update(self):
        client = self.Converter.CLIENT
        date_string_first = '17/12/2021'
        client.set(date_string_first, b'{1:2, 3:4}', expire = 5)

        dict_len_start = len(self.Converter.Currency_dict)
        self.Converter.currency_dict_update(client, date_string_first)

        client_get_2 = client.get(date_string_first)
        curr_dict_2 = self.Converter.Currency_dict

        date_string_second = '18/12/2021'
        self.Converter.currency_dict_update(client, date_string_second)

        client_get_full = client.get(date_string_second)
        dict_len_full = len(self.Converter.Currency_dict)

        self.assertEqual(client_get_2, b'{1:2, 3:4}', ' ERROR in client_get_2! ')
        self.assertIn(dict_len_start, [0, 35], ' ERROR in dict_len_start! ')
        self.assertEqual(curr_dict_2, {1:2, 3:4}, ' ERROR in curr_dict_2! ')

        self.assertIsNotNone(client_get_full, ' ERROR in client_get_full_end! ')
        self.assertEqual(dict_len_full,  35, ' ERROR in dict_len_full! ')

    def test_replace_None(self):
        test_array_first = [1, (2, 3), '456', [23.0, 45.0], {10:'$'}]

        test_array  = [test_array_first[int(i / 2)] if i % 2 == 0 else None  for i in range(0, 10)]
        true_result = [test_array_first[int(i / 2)] if i % 2 == 0 else b'{}' for i in range(0, 10)]

        result = [self.Converter.replace_None(x) for x in test_array]

        self.assertEqual(result, true_result, ' ERROR in replace_None! ')

if __name__ == '__main__':
    unittest.main()
