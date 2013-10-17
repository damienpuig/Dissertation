Dissertation
============

MSc Computer Science Dissertation for Brookes University

![Schema of the final deliverable](/framework.png "Schema of the final deliverable")


Title of the dissertation
-------------------------

*A Context-aware infrastructure using Publish/Subscribe for Load-Balancing in Distributed Systems.*

The architecture described above is based on 3 parts:
* A physical network retrieving information using arduinos (Arduinos networks, developed in modified C++, Redis pub/sub).
* A System layer, distributed and collecting data using either Redis Lists + Publish/Subscribe, or RabbitMQ queue comsumption.
The system layer also implement a web server to deliver data to Sinks, using  HTTP or WebSocket. This web-server is based on Bottle web framework in MVC.
The system layer is entirely developed in Python. ( MongoDB, Bottle, Monkey, Redis, Rabbit-pika, pytest..)
* The Web server renders HTML pages linked with KnockoutJS.
