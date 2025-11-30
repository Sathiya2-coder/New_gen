from .entities import ThemeSettings, Team, Person, ContactMessage
from .database import db
from sqlalchemy import or_

class ThemeSettingsRepository:
    @staticmethod
    def get_by_key(key):
        return ThemeSettings.query.filter_by(setting_key=key).first()
    
    @staticmethod
    def save_or_update(key, value):
        setting = ThemeSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = value
        else:
            setting = ThemeSettings(setting_key=key, setting_value=value)
            db.session.add(setting)
        db.session.commit()
        return setting

class TeamRepository:
    @staticmethod
    def get_all():
        return Team.query.order_by(Team.name).all()
    
    @staticmethod
    def get_by_id(team_id):
        return Team.query.get(team_id)
    
    @staticmethod
    def get_by_name(name):
        return Team.query.filter_by(name=name).first()
    
    @staticmethod
    def get_with_members(team_id):
        return Team.query.get(team_id)
    
    @staticmethod
    def get_all_with_members():
        return Team.query.all()
    
    @staticmethod
    def save(team):
        db.session.add(team)
        db.session.commit()
        return team
    
    @staticmethod
    def delete(team_id):
        team = Team.query.get(team_id)
        if team:
            db.session.delete(team)
            db.session.commit()
        return team
    
    @staticmethod
    def exists_by_name(name):
        return Team.query.filter_by(name=name).first() is not None
    
    @staticmethod
    def count_total():
        return Team.query.count()

class PersonRepository:
    @staticmethod
    def get_all():
        return Person.query.filter_by(status='Active').all()
    
    @staticmethod
    def get_by_id(person_id):
        return Person.query.get(person_id)
    
    @staticmethod
    def get_by_email(email):
        return Person.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_team_id(team_id):
        return Person.query.filter_by(team_id=team_id, status='Active').order_by(Person.first_name).all()
    
    @staticmethod
    def get_active_members():
        return Person.query.filter_by(status='Active').all()
    
    @staticmethod
    def count_active_members():
        return Person.query.filter_by(status='Active').count()
    
    @staticmethod
    def save(person):
        db.session.add(person)
        db.session.commit()
        return person
    
    @staticmethod
    def soft_delete(person_id):
        person = Person.query.get(person_id)
        if person:
            person.status = 'Inactive'
            db.session.commit()
        return person
    
    @staticmethod
    def exists_by_email(email):
        return Person.query.filter_by(email=email).first() is not None
    
    @staticmethod
    def search_persons(keyword):
        return Person.query.filter(
            or_(
                Person.first_name.ilike(f'%{keyword}%'),
                Person.last_name.ilike(f'%{keyword}%'),
                Person.email.ilike(f'%{keyword}%')
            )
        ).all()

class ContactMessageRepository:
    @staticmethod
    def get_all():
        return ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    
    @staticmethod
    def get_unread():
        return ContactMessage.query.filter_by(is_read=False).order_by(ContactMessage.created_at.desc()).all()
    
    @staticmethod
    def count_unread():
        return ContactMessage.query.filter_by(is_read=False).count()
    
    @staticmethod
    def save(message):
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def mark_as_read(message_id):
        message = ContactMessage.query.get(message_id)
        if message:
            message.is_read = True
            db.session.commit()
        return message
    
    @staticmethod
    def delete(message_id):
        message = ContactMessage.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
        return message
