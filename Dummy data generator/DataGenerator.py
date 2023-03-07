import warnings
from numpy import random
import pandas as pd
from os import getcwd
from datetime import date
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype

warnings.filterwarnings("ignore")


def get_mue_sigma(column_name):
    """
    get and validate mean and sigma value for each column in the generated data
    :param column_name: name of the current column
    :return: mean and sigma value for each column
    """
    while True:
        try:
            avg = float(input('\nEnter mean value for "{}" column'.format(column_name)))
            std = float(input('Enter sigma value for "{}" column'.format(column_name)))
            break
        except (ValueError, Exception):
            print("\nValues must be numbers, try again")
    return avg, std


class DummyDataGenerator(object):

    def __init__(self, data_size, columns_num, contains_date_column, contains_cat_columns):
        """
        initialize shape of data and set data frame attributes like file name

        :param data_size: length of data to be generated
        :param columns_num: number of columns
        :param contains_date_column: check date column existence (y|n)
        :param contains_cat_columns: check categorical column(s) existence (y|n)
        """
        try:
            value = int(columns_num)  # data_size
            value1 = int(data_size)  # columns_num
            if value > 0 and value1 > 0:
                self.data_size = value1
                self.columns_num = value

                if contains_date_column == 'y':
                    self.columns_num -= 1

                self.date_check = contains_date_column
                self.categorical_check = contains_cat_columns
                self.generated_data = pd.DataFrame()
                self.data_file_name = f'{getcwd()}//{date.today()} {data_size} rows generated data.txt'
                print('\nData frame with shape ({},{}) generated'.format(value1, value))
                self.get_data()
            else:
                print('\nColumns number and data size must be integers greater than 0')
        except (ValueError, Exception):
            print('\nColumns number and data size must be numbers')

    def get_numerical_columns_names(self, cat_columns_num):
        """
        take data frame columns names as inputs
        :return: list of data frames columns names
        """
        columns_names = list()

        for i in range(self.columns_num - cat_columns_num):
            columns_names.append(input('\nEnter name for numerical column (column number {})'.
                                       format((self.columns_num - cat_columns_num) + i)))

        return columns_names

    def plot_data_frame(self):
        """
        to take a look on the distribution of each column
        plot numerical columns after the generation of data
        :return: None
        """
        for col in self.generated_data.columns:
            if is_numeric_dtype(self.generated_data[col]):
                print('"{}" is numerical column'.format(col))
                figure, axis = plt.subplots(1, 2)

                axis[0].hist(self.generated_data[col])
                axis[0].set_title(col)

                axis[1].boxplot(self.generated_data[col])
                axis[1].set_title(col)
                plt.show()
            else:
                print('"{}" is non-numerical column'.format(col))
                plt.pie(self.generated_data[col].value_counts().values,
                        labels=self.generated_data[col].value_counts().keys())
                plt.title(col)
                plt.legend()
                plt.show()

    def save_data(self):
        """
        save generated data as csv file in txt file
        :return: None
        """
        self.generated_data.to_csv(self.data_file_name, index=False)

    def generate_date_range(self):
        """
        generate date column in the data frame
        :return: None
        """
        while True:
            try:
                start_date = input('\nEnter star date DD-MM-YYYY')
                end_date = input('Enter end date DD-MM-YYYY')
                self.generated_data['Date'] = pd.to_datetime(
                    pd.Series(pd.date_range(start_date, end_date, self.data_size)))
                self.generated_data['Date'] = self.generated_data['Date'].dt.date
                break
            except (ValueError, Exception):
                print('\nInvalid date (enter date in the following format DD-MM-YYYY).try again')

    def generate_categorical_column(self, columns_num):
        """
        generate categorical column by take number of available values and randomize them with replacement
        :return: None
        """
        for j in range(columns_num):
            while True:
                try:
                    column_name = input('\nEnter name for categorical column (column number {})'.format(j + 1))
                    column_values_num = int(input('Enter number of values chose from them'))
                    column_values = list()

                    if column_values_num > 0:
                        for i in range(column_values_num):
                            column_values.append(input('Enter value number {}'.format(i + 1)))
                        self.generated_data[column_name] = random.choice(column_values,
                                                                         size=self.data_size, replace=True)
                        break
                    else:
                        print('\nColumn values number must be greater than 0')
                except (ValueError, Exception):
                    print('\nInvalid parameters. try again')

    def get_data(self):
        """
        call methods and functions to generate and save data generated
        :return: None
        """

        cat_columns_num = 0
        if self.date_check == 'y':
            self.generate_date_range()

        if self.categorical_check == 'y':
            while True:
                try:
                    cat_columns_num = int(input('\nHow many categorical columns'))
                    if 0 < cat_columns_num <= self.columns_num:
                        self.generate_categorical_column(cat_columns_num)
                        break
                    else:
                        print(f'\nNumber of categorical columns must be number greater than 0 and '
                              f'less than or equal to {self.columns_num}')
                except (ValueError, Exception):
                    print('\nInvalid input. try again')

        columns_names = self.get_numerical_columns_names(cat_columns_num)
        for num in range(self.columns_num - cat_columns_num):
            mue, sigma = get_mue_sigma(columns_names[num])
            column = random.normal(mue, sigma, size=self.data_size)
            self.generated_data[columns_names[num]] = column
        self.save_data()
        self.plot_data_frame()
