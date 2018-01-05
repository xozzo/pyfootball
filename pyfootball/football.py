import requests
import os

from . import globals
from .globals import endpoints
from .models.competition import Competition
from .models.team import Team
from .models.fixture import Fixture
from .models.leaguetable import LeagueTable
from .models.player import Player


class Football(object):
    def __init__(self, api_key=None):
        """Takes either an api_key as a keyword argument or tries to access
        an environmental variable ``PYFOOTBALL_API_KEY``, then uses the key to
        send a test request to make sure that it's valid. The api_key
        kwarg takes precedence over the envvar.

        Sends one request to api.football-data.org.

        :keyword api_key: The user's football-data.org API key.
        :type api_key: string
        """
        if api_key:
            key = api_key
        elif os.getenv('PYFOOTBALL_API_KEY', None):
            key = os.getenv('PYFOOTBALL_API_KEY')
        else:
            raise ValueError("Couldn't find an API key in the keyword " +
                             "argument api_key nor the environmental " +
                             "variable PYFOOTBALL_API_KEY.")

        endpoint = endpoints['all_competitions']
        globals.headers = {'X-Auth-Token': key}
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()
        globals.api_key = key

    def get_prev_response(self):
        """Returns information about the most recent response.

        :returns: A dict containing information about the most recent response.
        """
        return globals.prev_response

    def get_competition(self, comp_id):
        """Returns a Competition object associated with the competition ID.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: The :class:`Competition` object.
        """
        endpoint = endpoints['competition'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        return Competition(r.json())

    def get_all_competitions(self):
        """Returns a list of Competition objects representing the current
        season's competitions.

        Sends one request to api.football-data.org.

        :returns: A list of :class:`Competition` objects.
        """
        endpoint = endpoints['all_competitions']
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        comp_list = []
        for comp in data:
            comp_list.append(Competition(comp))
        return comp_list

    def get_league_table(self, comp_id):
        """Given a competition ID, returns a LeagueTable object for the
        league table associated with the competition.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: A :class:`LeagueTable` object.
        """
        endpoint = endpoints['league_table'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        return LeagueTable(r.json())

    def get_comp_fixtures(self, comp_id):
        """Given an ID, returns a list of Fixture objects associated with the
        given competition.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: A list of :class:`Fixture` objects.
        """
        endpoint = endpoints['comp_fixtures'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['fixtures']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_competition_teams(self, comp_id):
        """Given an ID, returns a list of Team objects associated with the
        given competition.

        Sends one request to api.football-data.org.

        :param comp_id: The competition ID.
        :type comp_id: integer

        :returns: A list of :class:`Team` objects.
        """
        endpoint = endpoints['comp_teams'].format(comp_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        team_list = []
        for tm in data['teams']:
            team_list.append(Team(tm))
        return team_list

    def get_fixture(self, fixture_id):
        """Returns a Fixture object associated with the given ID. The response
        includes a head-to-head between teams; this will be implemented
        in the near future.

        Sends one request to api.football-data.org.

        :param fixture_id: The fixture ID.
        :type fixture_id: integer

        :returns: A :class:`Fixture` object.
        """
        endpoint = endpoints['fixture'].format(fixture_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        return Fixture(r.json()['fixture'])

    def get_all_fixtures(self):
        """Returns a list of all Fixture objects in the specified time frame.
        Defaults to the next 7 days or "n7". TODO: Include timeFrameStart
        and timeFrameEnd, and filter for specifying time frame.

        Sends one request to api.football-data.org.

        :returns: A list of :class:`Fixture` objects.
        """
        endpoint = endpoints['all_fixtures']
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['fixtures']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def get_team(self, team_id=None, team_name=None):
        """Given an ID, returns a Team object for the team associated with
        the ID. If no ID is supplied, checks if name is supplied. Database
        is queried using the team name and the first result in the response
        is returned. If both ID and name are supplied, ID will be evaluated
        and name will be ignored.

        Sends one request to api.football-data.org if fetching team by ID; two
        requests if fetching team by name.

        :param team_id: The team ID. Default ``None``.
        :type team_id: integer
        :param team_name: The team name. Default ``None``.
        :type team_name: string

        :returns: A :class:`Team` object on success, or ``None`` if no
        matches are found for the given team_name or ID.
        """
        if team_id and isinstance(team_id, int):
            endpoint = endpoints['team'].format(team_id)
            r = requests.get(endpoint, headers=globals.headers)
            globals.update_prev_response(r, endpoint)
            r.raise_for_status()
            return Team(r.json())

        elif team_name and isinstance(team_name, str):
            if len(team_name) < 3:
                raise ValueError("team_name must be at least 3 characters.")
            name = team_name.replace(" ", "%20")
            endpoint = endpoints['team'].format('?name='+name)
            r = requests.get(endpoint, headers=globals.headers)
            r.raise_for_status()
            data = r.json()
            if len(data['teams']) == 0:
                return None
            endpoint = endpoints['team'].format(data['teams'][0]['id'])
            r = requests.get(endpoint, headers=globals.headers)
            globals.update_prev_response(r, endpoint)
            r.raise_for_status()
            return Team(r.json())

        raise ValueError("No valid arguments were supplied to get_team. "
                         "Please supply either a team_id:int or team_name\
                         :str.")

    def get_team_players(self, team_id):
        """Given a team ID, returns a list of Player objects associated
        with the team.

        Sends one request to api.football-data.org.

        :param team_id: The team ID.
        :type team_id: integer

        :returns: A list of :class:`Player` objects based on players in the \
        specified team.
        """
        endpoint = endpoints['team_players'].format(team_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        player_list = []
        for player in data['players']:
            player_list.append(Player(player))
        return player_list

    def get_team_fixtures(self, team_id):
        """Given a team ID, returns a list of Fixture objects associated
        with the team.

        Sends one request to api.football-data.org.

        :param team_id: The team ID.
        :type team_id: integer

        :returns: A list of :class:`Fixture` objects for the specified team.
        """
        endpoint = endpoints['team_fixtures'].format(team_id)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        fixture_list = []
        for fixture in data['fixtures']:
            fixture_list.append(Fixture(fixture))
        return fixture_list

    def search_teams(self, team_name):
        """Given a team name, queries the database for matches and returns
        a dictionary containing key-value pairs of their team IDs and
        team names.

        Sends one request to api.football-data.org.

        :param team_name: The partial or full team name.
        :type team_name: string

        :returns: A dict with team ID as keys and team name as values.\
         ``None`` if no matches are found for the given team_name.
        """
        name = team_name.replace(" ", "%20")
        endpoint = endpoints['team'].format('?name='+name)
        r = requests.get(endpoint, headers=globals.headers)
        globals.update_prev_response(r, endpoint)
        r.raise_for_status()

        data = r.json()
        if data['count'] is 0:
            return None
        else:
            matches = {}
            for team in data['teams']:
                matches[team['id']] = team['name']
            return matches
