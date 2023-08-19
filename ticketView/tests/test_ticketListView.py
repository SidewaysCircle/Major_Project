from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ..models import IncidentSolve
from ticketScan.models import ResolutionPath, ProblemPlatform, ProblemArea, ProblemError

class listTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_raw_password = "password"

        self.end_user_group = Group.objects.create(name="end_users")
        self.engineers_group = Group.objects.create(name="engineers")

        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)
        
        self.user.groups.add(self.engineers_group)
        
        self.client.login(username=self.user.username, password=self.user_raw_password)

        self.testPlatform = ProblemPlatform.objects.create(platformName = 'test platform')

        self.testArea = ProblemArea.objects.create(fkPlatformName = self.testPlatform,
                                                   areaName = 'test area')
        
        self.testError = ProblemError.objects.create(fkAreaName = self.testArea,
                                                     errorDetail = 'test error')
        
        self.testResolution = ResolutionPath.objects.create(incidentType = self.testPlatform,
                                                            incidentArea = self.testArea,
                                                            incidentDetail = self.testError,
                                                            incidentSuggestion = 'test suggest',
                                                            incidentJustification = 'test justify')

        self.list_path = reverse('ticketList')

    def test_get_list_view(self):
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)

    def test_empty_ticket_list(self):
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['incidentList'], [])

    def test_populated_ticket_list(self):
        incident = IncidentSolve.objects.create(incidentNumber = 'INC000001234567',
                                             incidentResolutionPath = self.testResolution,
                                             incidentAddDetail = 'additional details',
                                             incidentShow = True)
        response = self.client.get(self.list_path)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['incidentList'], [incident])