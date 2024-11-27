
# Vegetables shop

This website is a site where you can buy and sell vegetables and fruits. The difference between this site and other sites where such things are sold is that we have divided the products into categories based on their quality, appearance, and size.


## Run locally

To run this project locally


**1) creating virtual environment**
```bash
  python -m venv venv
```

**2) activating virtual environment**

*in windows*
```bash
    venv\Scripts\activate
```

*in Linux*
```bash
    source venv/bin/activate
```

**3) install requirements**

```bash
    pip install -r requirements.txt
```

**4) Migrate models to database**

```bash
    python manage.py migrate
```

**5) Run the server**
```bash
    python manage.py runserver
```

in this case server run on `localhost:8000`