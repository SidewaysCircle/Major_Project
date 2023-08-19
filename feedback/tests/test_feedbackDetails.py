from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ..models import FeedbackResolves
from ticketScan.models import ResolutionPath, ProblemPlatform, ProblemArea, ProblemError
from ticketView.models import IncidentSolve

class feedbackListTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_raw_password = "password"

        self.end_user_group = Group.objects.create(name="end_users")
        self.engineers_group = Group.objects.create(name="engineers")

        self.user = User.objects.create_superuser(username='test-std-user',
                                             password=self.user_raw_password)
        
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
        
        self.testIncident = IncidentSolve.objects.create(incidentNumber = 'INC000001234567',
                                             incidentResolutionPath = self.testResolution,
                                             incidentAddDetail = 'additional details',
                                             incidentShow = True)
        
        self.testFeedback = FeedbackResolves.objects.create( feedbackIncident = self.testIncident,
                                                        feedbackResult = True,
                                                        feedbackDetail = 'test detail',
                                                        feedbackShow = False)
        
        self.update_path = reverse('feedbackView', kwargs={"pk": self.testFeedback.pk})

    def test_get_happy_path_update(self):
        #Ensure Update Page works
        response = self.client.get(self.update_path)
        self.assertEqual(response.status_code, 200)