from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ticketScan.models import ResolutionPath, ProblemPlatform, ProblemArea, ProblemError
from ticketView.models import IncidentSolve
from feedback.models import FeedbackResolves

class createScanTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_raw_password = "password"

        self.end_user_group = Group.objects.create(name="end_users")
        self.engineers_group = Group.objects.create(name="engineers")

        self.user = User.objects.create_user(username='test-std-user',
                                             password=self.user_raw_password)
        
        self.user.groups.add(self.engineers_group)
        
        self.client.login(username=self.user.username, password=self.user_raw_password)

        self.testPlatformHardware = ProblemPlatform.objects.create(platformName = 'Hardware')
        self.testPlatformSoftware = ProblemPlatform.objects.create(platformName = 'Software')

        self.testAreaHardware = ProblemArea.objects.create(fkPlatformName = self.testPlatformHardware,
                                                   areaName = 'Hardware Area')
        self.testAreaSoftware = ProblemArea.objects.create(fkPlatformName = self.testPlatformSoftware,
                                                   areaName = 'Software Area')
        
        self.testErrorHardware = ProblemError.objects.create(fkAreaName = self.testAreaHardware,
                                                     errorDetail = 'Hardware Error')
        self.testErrorSoftware = ProblemError.objects.create(fkAreaName = self.testAreaSoftware,
                                                     errorDetail = 'Software Error')
        
        self.testResolutionHardware = ResolutionPath.objects.create(incidentType = self.testPlatformHardware,
                                                            incidentArea = self.testAreaHardware,
                                                            incidentDetail = self.testErrorHardware,
                                                            incidentSuggestion = 'Hardware suggestion',
                                                            incidentJustification = 'Hardware Justification')
        
        self.testResolutionSoftware = ResolutionPath.objects.create(incidentType = self.testPlatformSoftware,
                                                            incidentArea = self.testAreaSoftware,
                                                            incidentDetail = self.testErrorSoftware,
                                                            incidentSuggestion = 'Software suggestion',
                                                            incidentJustification = 'Software Justification')

        self.create_path = reverse('resolutionDet')

    def test_get_happy_path_create(self):
        #Ensure register page opens
        response = self.client.get(self.create_path)
        self.assertEqual(response.status_code, 200)

    def test_create_scan_success(self):
        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)
        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 1)
        self.assertEqual(len(feedback), 1)

        created_ticket = tickets[0]
        self.assertEqual(created_ticket.incidentNumber, "INC000001234567")
        self.assertEqual(created_ticket.incidentResolutionPath, self.testResolutionHardware)
        self.assertEqual(created_ticket.incidentAddDetail, "Test Detail")
        self.assertEqual(created_ticket.incidentShow, True)

        created_feedback = feedback[0]
        self.assertEqual(created_feedback.feedbackIncident, created_ticket)
        self.assertEqual(created_feedback.feedbackResult, True)
        self.assertEqual(created_feedback.feedbackDetail, "")
        self.assertEqual(created_feedback.feedbackShow, False)

        view_path = reverse('index')
        
        self.assertRedirects(response, view_path, status_code=302,
                             target_status_code=200, fetch_redirect_response=True)
        
    def test_create_scan_no_INCNumber(self):
        data = {
            'incidentNumber': "",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_no_INCType(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': "",
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_no_INCArea(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': "",
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_no_INCDetail(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': "",
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_no_INCAddDetail(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': ""
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_invalid_INCNumber(self):
        data = {
            'incidentNumber': "CIN03",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_invalid_INCType(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformSoftware,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_invalid_INCArea(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaSoftware,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_invalid_INCDetail(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testAreaSoftware.id,
            'incidentAddDetail': "Test Detail"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

    def test_create_scan_invalid_INCAddDetail(self):
        data = {
            'incidentNumber': "INC000001234567",
            'incidentType': self.testPlatformHardware.id,
            'incidentArea': self.testAreaHardware.id,
            'incidentDetail': self.testErrorHardware.id,
            'incidentAddDetail': "!@£$%^&*()"
        }
        response = self.client.post(self.create_path, data=data)

        tickets = IncidentSolve.objects.all()
        feedback = FeedbackResolves.objects.all()

        self.assertEqual(len(tickets), 0)
        self.assertEqual(len(feedback), 0)

             

