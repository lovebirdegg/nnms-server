from django.urls import path,include
from workflow.views import workflow
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'workflow', workflow.WorkFlowViewSet, base_name="workflow")

urlpatterns = [
    path(r'api/workflow_test/', workflow.workflow_test,name='workflow_test'),
    path(r'api/new_ticket/', workflow.new_ticket,name='new_ticket'),
    path(r'api/get_tickets/', workflow.get_tickets,name='get_tickets'),
    path(r'api/get_ticket_detail/', workflow.get_ticket_detail,name='get_ticket_detail'),
    path(r'api/get_ticket_flowstep/', workflow.get_ticket_flowstep,name='get_ticket_flowstep'),
    path(r'api/get_ticket_flowlogs/', workflow.get_ticket_flowlogs,name='get_ticket_flowlogs'),
    path(r'api/get_ticket_transitions/', workflow.get_ticket_transitions,name='get_ticket_transitions'),
    path(r'api/handle_ticket/', workflow.handle_ticket,name='handle_ticket'),

]
