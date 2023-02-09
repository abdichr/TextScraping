import os
import json
import pandas as pd


def convert_pdf2txt(src_dir, dest_dir):
    files = os.listdir(src_dir)
    files = [i for i in files if '.txt' in i]
    df = pd.DataFrame()
    for file in files:
        with open(src_dir+file) as data:
            list_string = data.read().split('\n\n')
            block_list = list()
            num = 0
            for string in list_string:
                if len(string) > 0:
                    num += 1
                    row_json = json.loads(string)
                    row = {'page': row_json['page'],
                           'text': row_json['text']}
                    block_list.append(row)
        df = df.from_records(block_list)
        df.reset_index()
        df.columns = ['page', 'text']
        writer = pd.ExcelWriter(
            dest_dir+file.replace('.txt', '.xlsx'), engine='xlsxwriter')
        df.to_excel(writer,
                    sheet_name='Data Input',
                    header=False,
                    index=False)
        writer.close()


if __name__ == '__main__':
    convert_pdf2txt('03_TXT_cleaned/', '04_XLSX/')
