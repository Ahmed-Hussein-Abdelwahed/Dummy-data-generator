import DataGenerator


def data_generator_interface():
    while True:
        print('-' * 20 + 'Dummy data generator' + '-' * 20)
        print('1) Generate numerical data contains date column')
        print('2) Generate numerical data does not contain date column')
        print('3) Generate data contains numerical, categorical, and date column(s)')
        print('4) Generate data contains numerical, categorical, and without date column(s)')
        print('5) Exit')
        choice = input()

        if choice == '1':
            size = input('Enter data size')
            columns_num = input('How many columns')
            dummy_date_generator = DataGenerator.DummyDataGenerator(size, columns_num, 'y', 'n')
        elif choice == '2':
            size = input('Enter data size')
            columns_num = input('How many columns')
            dummy_date_generator = DataGenerator.DummyDataGenerator(size, columns_num, 'n', 'n')
        elif choice == '3':
            size = input('Enter data size')
            columns_num = input('How many columns')
            dummy_date_generator = DataGenerator.DummyDataGenerator(size, columns_num, 'y', 'y')
        elif choice == '4':
            size = input('Enter data size')
            columns_num = input('How many columns')
            dummy_date_generator = DataGenerator.DummyDataGenerator(size, columns_num, 'n', 'y')
        elif choice == '5':
            break
        else:
            print('\nInvalid choice. try again')
        print('=' * 60)


data_generator_interface()
