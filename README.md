#Special Media

Setup
----------
**Local Setup**

* Clone the repo
```
   git clone git@github.com:Rishabh222/SpecialMedia.git
```

* CD into directory
```
    cd SpecialMedia
```

* Create virtual env
```
    virtualenv ve
```

* Activate virtual Env
```
    source ve/bin/activate
```

* Install dependencies
```
    pip install -r requirements.pip
```

* Copy the local settings
```
 cp specialmedia/settings/local_settings.py.back specialmedia/settings/local_settings.py
```


* Configure the local settings
```
  Configure it
```

* Run the tasks
```
    python manage.py get_Instructions
```