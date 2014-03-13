Gasoline
========

Collaborative Wiki

# Installation

## Dependencies

* MongoDB

* Python
  * pip
  * diff-match-patch
  * markdown2
  * wikipedia

* Flask
  * Flask-Script
  * Flask-Babel
  * Flask-Assets
  * Flask-Login
  * flask-mongoengine
  * Flask-Cache

## Database

Populate database with sample articles

```
python manager.py initdb
```

## Launch Gasoline 

```
python manager.py run
```
