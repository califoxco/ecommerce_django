
For django3 users:
	You may encounter an import error stating that 'available_attrs' failed to import. This is because the django_lazysignup package was utilized and maintined in Django2 which has some of its APIs removed in Django 3.
To fix this issue, simply go to "...\lib\site-packages\lazysignup\decorators.py", and remove the import, and delete its occurances. 
