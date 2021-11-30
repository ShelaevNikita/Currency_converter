
[![CI](https://github.com/ShelaevNikita/Currency_converter/actions/workflows/service_ci.yml/badge.svg?branch=main)](https://github.com/ShelaevNikita/Currency_converter/actions/workflows/service_ci.yml)
# The Currency Converter Service

This is a service for converting one currency into another.   
It refers for data to the website of [The Central bank of Russia](https://cbr.ru/).   
To convert, the user must enter a string in the following format: `[Date] Numbers CurrencyFrom -> CurrencyTo`   
Where: 
 - **Date** - The date on which the service needs to look at the exchange rate. Optional. If the user has not entered a date, the current date of the operating system will be used. Format: **dd.mm.yy**, **>= 01.01.2000** and **<= TODAY**;   
 - **Numbers** - One or more currency values to convert, separated by spaces (integer or float);   
 - **CurrencyFrom** - The name of the currency **to be converted**;
 - **CurrencyTo** - The name of the currency **to convert to**.

For **CurrencyFrom** and **CcurrencyTo**, the use of a 3-letter ABBreviation is implied, but it is also possible to use special characters (for example,  **$**).

### Running the service using the command line and ***Python***

- Example of currency conversion **without** entering a date (the system date is used):

```
>>>python currency_converter.py
Please, inter the a line with the name of two currencies in the format:
         "[Date] Numbers CurrencyFrom -> CurrencyTo"
>>> 100 USD -> RUB
    [30.11.21]: 100 USD = 7498.18 RUB
```

- Example of currency conversion **with** date input:

```
>>>python currency_converter.py
Please, inter the a line with the name of two currencies in the format:
         "[Date] Numbers CurrencyFrom -> CurrencyTo"
>>> 01.01.10 100 USD -> RUB
    [01.01.10]: 100 USD = 3018.51 RUB
```

- Example of entering multiple values and using special characters:

```
>>>python currency_converter.py
Please, inter the a line with the name of two currencies in the format:
         "[Date] Numbers CurrencyFrom -> CurrencyTo"
>>> 25.10.21 1 5 10.25 0.1 50.5 $ -> €
    [25.10.21]: 1 $ = 0.859 €
    [25.10.21]: 5 $ = 4.295 €
    [25.10.21]: 10.25 $ = 8.804 €
    [25.10.21]: 0.1 $ = 0.086 €
    [25.10.21]: 50.5 $ = 43.377 €
```

### Running the service in a Docker-container

To get a working service, you need to run the following command:
```sudo docker build [-t <image_name>] .```   
After that, you need to run the assembled image:
```sudo docker run -p 11211:11211 [-it <image_name>]```   
Where ***image_name*** is the name of the assembled image (optional).   
...Further work with the service is similar to the description above **🠕**.
