from models.repositories import ContactMessageRepository
from models.entities import ContactMessage

class ContactMessageService:
    def __init__(self):
        self.repository = ContactMessageRepository()
    
    def save_message(self, message_data):
        message = ContactMessage(**message_data)
        return self.repository.save(message)
    
    def get_all_messages(self):
        return self.repository.get_all()
    
    def get_unread_messages(self):
        return self.repository.get_unread()
    
    def get_unread_message_count(self):
        return self.repository.count_unread()
    
    def mark_as_read(self, message_id):
        return self.repository.mark_as_read(message_id)
    
    def delete_message(self, message_id):
        return self.repository.delete(message_id)