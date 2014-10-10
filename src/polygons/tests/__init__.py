from django.db import connection
from django.test import TestCase

import os
from glob import glob

from comp4920.settings import PROJECT_ROOT

class Base_Test(TestCase):
        
    def setUp(self):
        with connection.cursor() as cursor:
            for filePath in glob(os.path.join(PROJECT_ROOT, 'polygons', 'sql',
                                              '*')):
                with open(filePath, 'r') as sqlFile:
                    cursor.execute(sqlFile.read())