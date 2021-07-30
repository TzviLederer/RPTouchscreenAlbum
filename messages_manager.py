from datetime import datetime

import pandas as pd


def load_messages(path='reminders.txt'):
    with open(path) as f:
        data = f.readlines()
    data = [x.replace('\n', '').split(';') for x in data]
    return pd.DataFrame(data, columns=['Period', 'Time', 'Message'])


def filter_df(df):
    for i, line in df.iterrows():
        if line['Period'] == 'o':
            date = datetime.strptime(line['Time'], '%d/%m/%Y')
            if date.date() != datetime.today().date():
                df = df.drop(i)
        elif line['Period'] == 'w':
            if (int(line['Time']) - 2) % 7 != datetime.now().weekday():
                df = df.drop(i)
        elif line['Period'] == 'm':
            if datetime.now().day != int(line['Time']):
                df = df.drop(i)
        else:
            print(f'{line["Period"]} is Bad argument of "period" in reminders file')
            df = df.drop(i)
    return df


class Messages:
    def __init__(self):
        self.df = load_messages()
        self.df = filter_df(self.df)
        self.df['red'] = False

        self.now = datetime.now().date()

    def update(self):
        if datetime.now().date() != self.now:
            self.df = load_messages()
            self.df = filter_df(self.df)
            self.df['red'] = False

            self.now = datetime.now().date()

    def read(self, index):
        assert index in self.df.index, 'Wrong index'
        self.df.loc[index, 'red'] = True

    def get_messages(self):
        return self.df[self.df['red']]['Message'].tolist()


def main():
    messages = Messages()
    messages.read(2)
    print(messages.get_messages())


if __name__ == '__main__':
    main()
