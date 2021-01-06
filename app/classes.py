from random import choice
import string
from werkzeug.utils import secure_filename
import os


class Uploads():
    ''' Save Uploads to the server '''

    def __init__(self, uploaded_file, folder):
        ''' Pass through request.files & folder to save to '''
        self.uploaded_file = uploaded_file
        self.folder = folder
        
    @staticmethod
    def generate_file_id(Length=56):
        ''' rename file before saving to server'''
        generate = string.ascii_letters + string.ascii_uppercase + string.digits
        return ''.join(choice(generate) for i in range(Length))

    def save_upload(self):
        if secure_filename(self.uploaded_file.filename) == '':
            ''' Fail safe -> Incase user tries to upload a file, and the file doesn't get submitted correctly '''
            return False

        filename = secure_filename(self.uploaded_file.filename)
        
        final_file_name = self.generate_file_id() + '.' + filename.split(".")[-1]
        self.uploaded_file.save(os.path.join(self.folder, final_file_name))

        return final_file_name

    def remove_upload(self, upload):
        ''' remove upload from server once user changes/deletes product '''
        os.remove(os.path.join(self.folder, upload))