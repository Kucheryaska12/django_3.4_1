import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student
import random




@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db(transaction=True)
def test_create_first_course(client, course_factory, transactional_db=True):
    #Arrange
    course_factory(name = 'first')

    #Act
    response = client.get('/api/v1/courses/')
    first_course = response.json()[0]
    #Assert  
    assert first_course['name'] == 'first'
    assert response.status_code == 200



@pytest.mark.django_db(transaction=True)
def test_get_course_list(client, course_factory, transactional_db=True):
    course_factory(_quantity=15)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert len(data) == 15
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_course_filter(client, course_factory, transactional_db=True):
    course_factory(_quantity=15)
    response = client.get('/api/v1/courses/') 
    data = response.json()
    id_list = []
    for course in data:
        if 'id' in course:
            id_list.append(course['id'])
    my_id = random.choice(id_list)
    new_resp = client.get(f'/api/v1/courses/{my_id}/')
    assert new_resp.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_course_name_filter(client, course_factory, transactional_db=True):
    course_factory(name='second')
    response = client.get('/api/v1/courses/?name=second')
    data = response.json()
    assert data[0]['name'] == 'second'
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_course_success_creation(client, transactional_db=True):
    data = {'name' :'Math', 'students' : []}
    response = client.post('/api/v1/courses/', data=data)
    assert response.status_code == 201


@pytest.mark.django_db(transaction=True)
def test_course_success_updating(client, course_factory, transactional_db=True):
    course_factory(name='Bio')
    bio_course = client.get('/api/v1/courses/?name=Bio')
    bio_course_id = bio_course.json()[0]['id']
    data = {'name' :'Biologiya'}
    client.patch(f'/api/v1/courses/{bio_course_id}/', data=data)
    response = client.get(f'/api/v1/courses/{bio_course_id}/')
    assert response.json()['name'] == 'Biologiya'
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_course_success_deleting(client, course_factory, transactional_db=True):
    course_factory(name='Inglish')
    ing_course = client.get('/api/v1/courses/?name=Inglish')
    ing_id = ing_course.json()[0]['id']
    response = client.delete(f'/api/v1/courses/{ing_id}/')
    assert response.status_code == 204