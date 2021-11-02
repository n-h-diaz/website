import json
import unittest
from unittest import mock

from main import app
from services import datacommons as dc


class TestApiGetStatsValue(unittest.TestCase):

    @mock.patch('services.datacommons.send_request')
    def test_api_get_stats_value(self, send_request):

        def side_effect(req_url,
                        req_json={},
                        compress=False,
                        post=True,
                        has_payload=True):
            if req_url == dc.API_ROOT + "/stat/value" and req_json == {
                    'place': 'geoId/06',
                    'stat_var': 'Count_Person_Male',
                    'date': None,
                    'measurement_method': None,
                    'observation_period': None,
                    'unit': None,
                    'scaling_factor': None
            } and not post and not has_payload:
                return {'value': 19640794}

        send_request.side_effect = side_effect
        response = app.test_client().get(
            '/api/stats/value?place=geoId/06&stat_var=Count_Person_Male')
        assert response.status_code == 200
        assert json.loads(response.data) == {"value": 19640794}


class TestApiGetStatSetWithinPlace(unittest.TestCase):

    def test_required_predicates(self):
        """Failure if required fields are not present."""
        no_parent_place = app.test_client().get(
            '/api/stats/within-place?child_type=City&stat_vars=Count_Person')
        assert no_parent_place.status_code == 400

        no_child_type = app.test_client().get(
            '/api/stats/within-place?parent_place=country/USA&stat_vars=Count_Person'
        )
        assert no_child_type.status_code == 400

        no_stat_var = app.test_client().get(
            '/api/stats/within-place?parent_place=country/USA&child_type=City')
        assert no_stat_var.status_code == 400

    @mock.patch('services.datacommons.send_request')
    def test_api_get_stats_set_within_place(self, send_request):

        result = {
            "data": {
                "Count_Person_Male": {
                    "val": {
                        "geoId/10001": 84271,
                        "geoId/10003": 268870,
                        "geoId/10005": 106429
                    },
                    "measurementMethod": "CensusACS5yrSurvey",
                    "importName": "CensusACS5YearSurvey",
                    "provenanceUrl": "https://www.census.gov/"
                },
                "Count_Person": {
                    "val": {
                        "geoId/10001": 178540,
                        "geoId/10003": 557550,
                        "geoId/10005": 229389
                    },
                    "measurementMethod":
                        "CensusPEPSurvey",
                    "importName":
                        "CensusPEP",
                    "provenanceUrl":
                        "https://www.census.gov/programs-surveys/popest.html"
                }
            }
        }

        def side_effect(req_url,
                        req_json={},
                        compress=False,
                        post=True,
                        has_payload=True):
            if req_url == dc.API_ROOT + "/stat/set/within-place" and req_json == {
                    'parent_place': 'geoId/10',
                    'child_type': 'County',
                    'date': '2018',
                    'stat_vars': ['Count_Person', 'Count_Person_Male']
            } and post and not has_payload:
                return result

        send_request.side_effect = side_effect
        response = app.test_client().get(
            '/api/stats/within-place?parent_place=geoId/10&child_type=County'
            '&date=2018&stat_vars=Count_Person&stat_vars=Count_Person_Male')
        assert response.status_code == 200
        assert json.loads(response.data) == result['data']

    @mock.patch('services.datacommons.send_request')
    def test_api_get_stat_set_within_place_no_date(self, send_request):

        result = {
            "data": {
                "Count_Person_Male": {
                    "val": {
                        "geoId/10001": 84271,
                        "geoId/10003": 268870,
                        "geoId/10005": 106429
                    },
                    "measurementMethod": "CensusACS5yrSurvey",
                    "importName": "CensusACS5YearSurvey",
                    "provenanceUrl": "https://www.census.gov/"
                },
                "Count_Person": {
                    "val": {
                        "geoId/10001": 178540,
                        "geoId/10003": 557550,
                        "geoId/10005": 229389
                    },
                    "measurementMethod":
                        "CensusPEPSurvey",
                    "importName":
                        "CensusPEP",
                    "provenanceUrl":
                        "https://www.census.gov/programs-surveys/popest.html"
                }
            }
        }

        def side_effect(req_url,
                        req_json={},
                        compress=False,
                        post=True,
                        has_payload=True):
            print(req_url)
            print(req_json)
            if req_url == dc.API_ROOT + "/stat/set/within-place" and req_json == {
                    'parent_place': 'geoId/10',
                    'child_type': 'County',
                    'date': None,
                    'stat_vars': ['Count_Person', 'Count_Person_Male']
            } and post and not has_payload:
                return result

        send_request.side_effect = side_effect
        response = app.test_client().get(
            '/api/stats/within-place?parent_place=geoId/10&child_type=County'
            '&stat_vars=Count_Person&stat_vars=Count_Person_Male')
        assert response.status_code == 200
        assert json.loads(response.data) == result['data']

    @mock.patch('services.datacommons.send_request')
    def test_api_get_stats_property(self, send_request):

        def side_effect(req_url,
                        req_json={},
                        compress=False,
                        post=True,
                        has_payload=True):
            print(req_json)
            if req_json == {
                    'dcids': [
                        'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    ]
            }:
                return {
                    'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26': [{
                        'objectId':
                            'StatisticalVariable',
                        'objectName':
                            'StatisticalVariable',
                        'objectTypes': ['Class'],
                        'predicate':
                            'typeOf',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'minValue',
                        'objectName':
                            'minValue',
                        'objectTypes': ['Property'],
                        'predicate':
                            'statType',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'dc/d7tbsb1',
                        'objectName':
                            'https://datacommons.org',
                        'objectTypes': ['Provenance'],
                        'predicate':
                            'provenance',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'Place',
                        'objectName':
                            'Place',
                        'objectTypes': ['Class'],
                        'predicate':
                            'populationType',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectValue':
                            'Min Temperature of 2006-01, RCP 2.6 (Difference '
                            'Relative To Base Date & Daily)',
                        'predicate':
                            'name',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'dc/g/Place_BaseDate-200601_EmissionsScenario-RCP2.6',
                        'objectName':
                            'Place With Base Date = 2006-01, Emissions Scenario = '
                            'RCP 2.6',
                        'objectTypes': ['StatVarGroup'],
                        'predicate':
                            'memberOf',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'DifferenceRelativeToBaseDate&Daily',
                        'objectTypes': ['Thing'],
                        'predicate':
                            'measurementQualifier',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'temperature',
                        'objectName':
                            'temperature',
                        'objectTypes': ['Property'],
                        'predicate':
                            'measuredProperty',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'RCP2.6',
                        'objectName':
                            'RCP2.6',
                        'objectTypes': [
                            'RepresentativeConcentrationPathwayEnum'
                        ],
                        'predicate':
                            'emissionsScenario',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectValue':
                            'Daily minimum near-surface air temperature under '
                            'RCP2.6 emissions scenario',
                        'predicate':
                            'description',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectId':
                            'emissionsScenario',
                        'objectName':
                            'emissionsScenario',
                        'objectTypes': ['Property'],
                        'predicate':
                            'constraintProperties',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }, {
                        'objectValue':
                            '2006-01',
                        'predicate':
                            'baseDate',
                        'provenanceId':
                            'dc/d7tbsb1',
                        'subjectId':
                            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
                    }]
                }

        send_request.side_effect = side_effect
        response = app.test_client().get(
            '/api/stats/stats-var-property?dcid=DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26'
        )
        assert response.status_code == 200
        assert json.loads(response.data) == {
            'DifferenceRelativeToBaseDate2006-01_Daily_Min_Temperature_RCP26': {
                'mprop':
                    'temperature',
                'pt':
                    'Place',
                'md':
                    '',
                'st':
                    'minValue',
                'mq':
                    'DifferenceRelativeToBaseDate&Daily',
                'pvs': {
                    'emissionsScenario': 'RCP2.6'
                },
                'title':
                    'Min Temperature of 2006-01, RCP 2.6 (Difference Relative To Base Date & Daily)',
                'ranked':
                    False
            }
        }
