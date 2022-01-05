import pytest
import json
from api_app.views import UserViewSet
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model


from django.urls import reverse


# @pytest.mark.django_db
# def test_crearte_user(api_client):
#     User = get_user_model()
#     User.objects.create_user('user6@user.com', 'user6', 'user6')
#     assert User.objects.count() == 1
#     url = 
#     response = api_client.get(url)
#     assert response.status_code == 201


@pytest.mark.django_db
def test_view_documentrequest(api_client):
    endpoint = '/api_app/documentrequest/'
    
    # url = reverse('all_request')
    response = api_client.get(reverse('all_request'))
    assert response.status_code == 200

def test_example():
    assert 1 == 1