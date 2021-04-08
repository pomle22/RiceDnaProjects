import base64, random, string, os # encode
from django.conf import settings
from .models import *

# function set format date for insert to table
# date format input --> 01/05/2019
# date format output --> 2019-05-01
def date_format(date):
    if date == '':
        return None
    else:
        date = date.split('/')
        date = date[2]+'-'+date[1]+'-'+date[0]
        return date

def encode(number):
    encode = base64.b16encode(base64.b85encode(bytes(str(number), "utf-8"))).decode("utf-8", "ignore")
    return encode

def decode(number):
    decode = base64.b85decode(base64.b16decode(number)).decode("utf-8", "ignore")
    return decode

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def rename_to_upload_photo(name_input_file, specimen_id, title, path_dir):
    filename_to_DB = []
    for count, x in enumerate(name_input_file):
        def process(file, filename):
            filename__sub = []
            filename = str(filename).split('.')
            file_type = '.'+filename[-1]
            # specimen_id_encode
            specimen_id_encode = encode(specimen_id)+'_'
            # string random
            string_encode = string.ascii_letters
            string_encode = encode(''.join([random.choice(string.ascii_letters) for i in range(4)]))
            num_random = encode(random.randint(0,9999999))
            # file_name
            filename = title+'_'+specimen_id_encode+string_encode+num_random+file_type

            path = settings.MEDIA_ROOT+'/'+path_dir+'/'+filename
            if os.path.exists(path) == True:
                # string random
                string_encode = string.ascii_letters
                string_encode = encode(''.join([random.choice(string.ascii_letters) for i in range(4)]))
                num_random = encode(random.randint(0,9999999))
                num_random2 = encode(random.randint(0,9999999))
                filename = title+'_'+specimen_id_encode+string_encode+num_random+num_random2+file_type

            filename__sub.append(filename)

            with open(settings.MEDIA_ROOT+'/'+path_dir+'/' + str(filename), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return filename__sub    
        data = process(x,x)
        filename_to_DB.extend(data)
    if filename_to_DB == []:
        filename_to_DB = ''
    return filename_to_DB

def deleteImage(part, image_name):
    # if you need to dalete all Image
    # deleteImage(part, Array[image name]):
    os.remove(part+image_name)
    return(True)

def add_logs(log_type,log_detail,user_action,user_id):
    logs.objects.create(log_type=log_type,log_detail=log_detail,user_action=user_action,user_id=user_id)


