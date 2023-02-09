import os
import fitz
import textwrap


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def convert_pdf2txt(src_dir):
    files = os.listdir(src_dir)
    files = [i for i in files if '.pdf' in i]
    for file in files:
        try:
            with fitz.open(src_dir+file) as pages:
                page_count = 0
                block_count = 0
                for page in pages:
                    page_count += 1
                    blocks = page.get_text("blocks")
                    for block in blocks:
                        if block[6] == 0:
                            block_count += 1
                print(file)
                print('Pages: ', page_count)
                print('Blocks: ', block_count, '\n')
        except Exception as oops:
            print(oops, file)


if __name__ == '__main__':
    convert_pdf2txt('PDFs/')
