import traceback


class Fixture(object):
    def __init__(self, data):
        """ Takes a dict converted from the JSON response by the API and wraps
            the fixture data within an object.

            Keyword arguments:
            data -- A python dict converted from JSON containing the fixture
                    data.
        """
        try:
            self._home_team_ep = data['_links']['homeTeam']['href']
            self._away_team_ep = data['_links']['awayTeam']['href']
            self._competition_ep = data['_links']['competition']['href']
            self.date = data['date']
            self.status = data['status']
            self.matchday = data['matchday']
            self.home_team = data['homeTeamName']
            self.home_team_id = self._home_team_ep.split("/")[-1]
            self.away_team = data['awayTeamName']
            self.away_team_id = self._away_team_ep.split("/")[-1]
            self.competition_id = self._competition_ep.split("/")[-1]

            if data['result']['goalsHomeTeam'] is not None:
                self.result = {
                    'home_team_goals': data['result']['goalsHomeTeam'],
                    'away_team_goals': data['result']['goalsAwayTeam'],
                }
                if 'halfTime' in data['result']:
                    ht = data['result']['halfTime']
                    self.result['half_time'] = {
                        'home_team_goals': ht['goalsHomeTeam'],
                        'away_team_goals': ht['goalsAwayTeam']
                    }
            else:
                self.result = None

            if data['odds']:
                self.odds = {
                    'home_win': data['odds']['homeWin'],
                    'draw': data['odds']['draw'],
                    'away_win': data['odds']['awayWin']
                }
            else:
                self.odds = None

        except KeyError:
            traceback.print_exc()
