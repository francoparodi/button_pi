# Button_pi

Simple sample of events from two buttons with Raspberry pi.
Each connected client, will be notify about events (websocketIO)

### Coonection schema

![Connection Schema](docs/button_pi_bb.png)

### Installing

From project root create virtual environment, activate and install requirements:

```sh
~/button_pi$ python3 -m venv venv
~/button_pi$ source venv/bin/activate
~/button_pi$ pip install -r requirements.txt
```

## Running

__as app__

```sh
export FLASK_APP=flaskr
flask run
```

__as wsgi server__

```sh
gunicorn --worker-class eventlet -w 1 -b localhost:8080 wsgi
```

## Deployment

As seen above (gunicorn...)

## Authors 

Franco Parodi

## License

This project is licensed under the MIT License
