
from dataclasses import dataclass, field
from typing import List

@dataclass
class Match:
    home_team: str
    home_micro_name: str
    match_result_home: str
    away_team: str
    away_micro_name: str
    match_result_away: str
    match_time: str
    match_status: str
    matchday_range: str

@dataclass
class Matchday:
    matchday_number: str
    matchday_range: str
    matches: List[Match] =field(default_factory=list)

    def add_match(self, home_team, home_micro_name, match_result_home, away_team, away_micro_name, match_result_away,
                  match_time, match_status):


        match = Match(
            home_team=home_team,
            home_micro_name=home_micro_name,
            match_result_home=match_result_home,
            away_team=away_team,
            away_micro_name=away_micro_name,
            match_result_away=match_result_away,
            match_time=match_time,
            match_status=match_status,
            matchday_range=self.matchday_range,
        )
        self.matches.append(match)

    def __str__(self):
        # "matchday_range" ist in der Matchday-Klasse, aber du hast 'date_range' in der __str__-Methode benutzt
        return f"Matchday {self.matchday_number}: {self.matchday_range}\n" + "\n".join([
            f"{m.home_team} vs {m.away_team}: {m.match_result_home}-{m.match_result_away}, Time: {m.match_time}, Status: {m.match_status}"
            for m in self.matches])


#TODO write class for season, collect matchdays

@dataclass
class Season:
    matchdays: List[Matchday] = field(default_factory=list)

    def add_matchday(self, matchday: Matchday):
        self.matchdays.append(matchday)

    def __str__(self):
        return  "\n".join([str(matchday) for matchday in self.matchdays])

season = Season()