import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student

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


@pytest.mark.django_db
def test_create_first_course(client, course_factory):
    #Arrange
    course_factory(name = 'first')

    #Act
    response = client.get('/api/v1/courses/')
    data = response.json()
    #Assert  
    assert data[0]['name'] == 'first'



@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    course_factory(_quantity=15)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert len(data) == 15


@pytest.mark.django_db
def test_course_filter(client, course_factory):
    course_factory(_quantity=15)
    response = client.get('/api/v1/courses/?id=22') # id 22, т.к. предыдущие тесты создали 1+15 экземпляров Course.
    data = response.json()
    assert data[0]['id'] == 22


@pytest.mark.django_db
def test_course_name_filter(client, course_factory):
    course_factory(name='second')
    response = client.get('/api/v1/courses/?name=second')
    data = response.json()
    assert data[0]['name'] == 'second'


@pytest.mark.django_db
def test_course_success_creation(client):
    data = {'name' :'Math', 'students' : []}
    response = client.post('/api/v1/courses/', data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_course_success_updating(client, course_factory):
    course = course_factory(name='Bio')
    data = {'name' :'Biologiya'}
    client.post('/api/v1/courses/?name=Bio', data=data)
    response = client.get('/api/v1/courses/?name=Biologiya')
    new_name = response.json()
    assert new_name[0]['name'] == 'Biologiya'


@pytest.mark.django_db
def test_course_success_deleting(client, course_factory):
    course_factory(name='Inglish')
    ing_course = client.get('/api/v1/courses/?name=Inglish')
    ing_id = ing_course.json()[0]['id']
    response = client.delete(f'/api/v1/courses/{ing_id}')
    assert response.status_code == 204