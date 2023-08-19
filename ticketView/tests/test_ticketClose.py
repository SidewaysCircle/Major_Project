from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ..models import IncidentSolve
from ticketScan.models import ResolutionPath, ProblemPlatform, ProblemArea, ProblemError
from feedback.models import FeedbackResolves

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
        
        self.testIncident = IncidentSolve.objects.create(incidentNumber = 'INC000001234567',
                                             incidentResolutionPath = self.testResolution,
                                             incidentAddDetail = 'additional details',
                                             incidentShow = True)
        
        self.testFeedback = FeedbackResolves.objects.create(feedbackIncident = self.testIncident,
                                                            feedbackResult = True,
                                                            feedbackDetail = 'test detail',
                                                            feedbackShow = False)

        self.update_path = reverse('ticketClose', kwargs={"pk": self.testFeedback.pk})

    def test_get_happy_path_update(self):
        #Ensure Update Page works
        response = self.client.get(self.update_path)
        self.assertEqual(response.status_code, 200)

    def test_feedback_update_result(self):

        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, 'test detail')
        self.assertEqual(created_feedback.feedbackShow, False)
        data = {
            'feedbackIncident': self.testIncident,
            'feedbackResult': False,
            'feedbackDetail': 'test detail',
            'feedbackShow': False
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, False)
        self.assertEqual(created_feedback.feedbackDetail, 'test detail')
        self.assertEqual(created_feedback.feedbackShow, True)

        ticket = IncidentSolve.objects.all()
        self.assertEqual(len(ticket), 1)
        created_ticket = ticket[0]

        self.assertEqual(created_ticket.incidentShow, False)

    def test_feedback_update_detail(self):
        
        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, 'test detail')
        self.assertEqual(created_feedback.feedbackShow, False)
        data = {
            'feedbackIncident': self.testIncident,
            'feedbackResult': True,
            'feedbackDetail': 'changed detail',
            'feedbackShow': False
        }
        response = self.client.post(self.update_path, data=data)
        self.assertEqual(response.status_code, 302)
        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, 'changed detail')
        self.assertEqual(created_feedback.feedbackShow, True)

        ticket = IncidentSolve.objects.all()
        self.assertEqual(len(ticket), 1)
        created_ticket = ticket[0]

        self.assertEqual(created_ticket.incidentShow, False)

    def test_feedback_update_no_detail(self):

        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, 'test detail')
        self.assertEqual(created_feedback.feedbackShow, False)
        data = {
            'feedbackIncident': self.testIncident,
            'feedbackResult': False,
            'feedbackDetail': '',
            'feedbackShow': False
        }
        response = self.client.post(self.update_path, data=data)
        #No changes were made to the object as the form data was invalid
        feedback = FeedbackResolves.objects.all()
        self.assertEqual(len(feedback), 1)
        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, self.testIncident)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, 'test detail')
        self.assertEqual(created_feedback.feedbackShow, False)

        ticket = IncidentSolve.objects.all()
        self.assertEqual(len(ticket), 1)
        created_ticket = ticket[0]

        self.assertEqual(created_ticket.incidentShow, True)
