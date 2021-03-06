Getting Started
=================
In this tutorial, you'll be introduced to pyfootball's API as well as its data mapping. 

If you're not familiar with football-data.org, it'd be better for you to get acquainted with it by reading the `football-data.org documentation <http://api.football-data.org/documentation>`_ before proceeding with pyfootball.

If you don't have pyfootball set up, see :doc:`the home page <../index>`. Otherwise, let's get started!

First, you're going to want to create a ``Football`` instance:
::

    >>> import pyfootball
    >>> f = pyfootball.Football(api_key='your_api_key')

You can also choose to instantiate ``Football`` without any arguments and make
it use an API key obtained from an environmental variable named
``PYFOOTBALL_API_KEY``. Here is an example in \*nix:
::

    $ export PYFOOTBALL_API_KEY='your_api_key'

and then in your program:
::

    >>> import pyfootball
    >>> f = pyfootball.Football()

If you provide an invalid API key, an HTTPError exception will be raised. 

.. note:: Instantiating a ``Football`` object will use one request out of the 50 allowed per minute by football-data.org's API. You can see the full list of which functions send requests and which ones don't at :doc:`api`.

The ``Football`` class serves as an entry point for the library. Now, we want to get the data of a team — for example, Manchester United — but since we don't know its ID in football-data.org's database, we're going to have to look it up:
::

    >>> matches = f.search_teams("manchester")
    >>> matches
    {65: 'Manchester City FC', 66: 'Manchester United FC'}

``Football.search_teams(name)`` queries the database for matches to ``name`` and returns key-value pairs of team IDs and team names respectively.

Now that we have Manchester United's ID, we can get more information about it:
::

    >>> man_utd = f.get_team(66)

``Football.get_team(id)`` returns a ``Team`` object. It contains all the information you'd get in a JSON response from football-data.org, along with some cool functions. We can call ``Team.get_fixtures()`` to get its fixtures or ``Team.get_players()`` to get its players.

.. hint:: The ``Football`` class provides a useful method ``Football.get_prev_response()`` to give you information about the most recently-used response. Any time you use a method in the library that sends a HTTP request, this value is updated. You can use it to keep track of useful stuff like response status code or how many requests you have left.

::

    >>> players = man_utd.get_players()

``Team.get_players()`` returns a list of ``Player`` objects. Like ``Team`` objects, ``Player`` objects are objects from JSON responses mapped to Python classes:
::

    >>> players[0].name
    Paul Pogba
    >>> players[0].market_value
    70,000,000 €

A comprehensive list of object models and their attributes are available at :doc:`data_model`. A full list of functions available are available at :doc:`api`.
