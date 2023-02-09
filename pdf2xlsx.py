import os
import re
import fitz
import pandas as pd

# String replacement conditions
# Replace new-line, enter, tab, whitespaces, hyphens, and double-space
rep = {'\n': ' ', '\r': ' ', '\t': ' ',
       '\s+': ' ', '-  ': '', '- ': '', '  ': ''}
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def convert_pdf2txt(src_dir, dest_dir):
    files = os.listdir(src_dir)
    files = [i for i in files if '.pdf' in i]
    for file in files:
        try:
            with fitz.open(src_dir+file) as pages:
                block_list = list()
                page_num = 0
                df = pd.DataFrame()
                for page in pages:
                    page_num += 1
                    blocks = page.get_text("blocks")
                    for block in blocks:
                        if block[6] == 0:
                            raw_text = block[4]
                            cleaned_text = pattern.sub(
                                lambda m: rep[re.escape(m.group(0))], raw_text.strip())
                            if len(cleaned_text) > 4:
                                row = {'page': page_num,
                                       'text': cleaned_text}
                                block_list.append(row)

                df = df.from_records(block_list)
                df.reset_index()
                df.columns = ['page', 'text']

                writer = pd.ExcelWriter(
                    dest_dir+file.replace('.pdf', '') + '.xlsx', engine='xlsxwriter', mode='w')
                df.to_excel(writer, sheet_name='Data Input',
                            header=False, index=False)
                writer.close()
        except Exception as oops:
            print(oops, file)


if __name__ == '__main__':
    convert_pdf2txt('01_PDF/', '02_XLSX_raw/')
