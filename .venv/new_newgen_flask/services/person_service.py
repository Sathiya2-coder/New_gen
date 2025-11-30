from models.repositories import PersonRepository
from models.entities import Person
from datetime import date

class PersonService:
    def __init__(self):
        self.repository = PersonRepository()
    
    def get_all_persons(self):
        return self.repository.get_all()
    
    def get_person_by_id(self, person_id):
        return self.repository.get_by_id(person_id)
    
    def save_person(self, person_data):
        person = Person(**person_data)
        return self.repository.save(person)
    
    def update_person(self, person_id, person_data):
        person = self.repository.get_by_id(person_id)
        if person:
            for key, value in person_data.items():
                setattr(person, key, value)
            return self.repository.save(person)
        return None
    
    def delete_person(self, person_id):
        return self.repository.soft_delete(person_id)
    
    def exists_by_email(self, email):
        return self.repository.exists_by_email(email)
    
    def count_active_persons(self):
        return self.repository.count_active_members()
    
    def get_persons_by_team_id(self, team_id):
        return self.repository.get_by_team_id(team_id)
    
    def search_persons(self, keyword):
        return self.repository.search_persons(keyword)