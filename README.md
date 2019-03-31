# Automated Attendance Monitoring System
Automated Attendance Monitoring System for Innopolis University in context of [S19] Software Project course.
### Contributors:
* [Lenar Gumerov](mailto:l.gumerov@innopolis.ru "Send mail")
* [Egor Polivtsev](mailto:e.polivtsev@innopolis.ru "Send mail")
* [Victoria Zubrinkina](mailto:v.zubrinkina@innopolis.ru "Send mail")
* [Georgii Khorushevskii](mailto:g.horuzhevskiy@innopolis.ru "Send mail")
* [Mikhail Bobrov](mailto:m.bobrov@innopolis.ru "Send mail")
------
## Getting Started
### Starting server
#### Execute commands:

*Unix Bash (Linux, Mac, etc.)*:
```
$ export FLASK_APP=run.py
$ flask db upgrade
$ flask run -h 0.0.0.0
```
*Windows CMD*:
```
> set FLASK_APP=run.py
> flask db upgrade
> flask run -h 0.0.0.0
```
*Windows PowerShell*:
```
> $env:FLASK_APP = "run.py"
> flask db upgrade
> flask run -h 0.0.0.0
```
### Testing service
After starting the server link to site is host's IPv4 in network and port ```5000```

__Example:__
```
10.240.17.219:5000
```
If you are trying to access to the site on the same machine as the server is running, do not use ```localhost``` or ```127.0.0.1```, because it will break URLs in QR-codes. Use your network address or ip instead.
