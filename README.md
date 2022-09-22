# Image Resizing Service

This is a service in Flask, can be used for image editing - you can resize images with JPG extension.
The queue manager takes the job from Flask and processes it. Broker - RabbitMQ.

## celery_sample

simple flask app with celery

`docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management`

**default management creds:**

username: guest

password: guest

`celery -A celery_worker worker --loglevel=INFO --purge --pool=solo`
