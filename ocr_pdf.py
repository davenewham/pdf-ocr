import os, random, string
from bottle import response, route, run, static_file, request, abort
import ocrmypdf

@route('/scripts/pdf2ocr',)
def main_page():
    return static_file("index.html", root=os.path.curdir)

@route('/scripts/pdf2ocr/<filename>')
def hello(filename="index.html"):
    return static_file(filename, root=os.path.curdir)

@route('/scripts/pdf2ocr/upload', method='POST')
def upload_pdf():
    upload     = request.files.get('upload')

    while True:
        dirname = os.path.join("tmp", "pdf2ocr", ''.join(random.choices(string.ascii_letters + string.digits, k=20)))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            break

    name, ext = os.path.splitext(upload.filename)
    if not ext == '.pdf':
        return 'File extension not allowed. Please upload a PDF!'

    upload.save(dirname)

    # Convert this file.
    file_path = os.path.join(dirname, upload.filename)
    file_out_name = upload.filename[:-3] + "OCR.pdf"
    file_out = os.path.join(dirname, file_out_name)

    ocrmypdf.ocr(file_path, file_out, deskew=True, use_threads=True, force_ocr=True)
    # except ocrmypdf.exceptions.PriorOcrFoundError:
    #     return 'Document already contains OCR!'
    return static_file(file_out_name, root=dirname)

if __name__ == '__main__':
    run(host='localhost', port=8085)