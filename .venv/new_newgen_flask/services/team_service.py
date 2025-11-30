from models.repositories import TeamRepository
from models.entities import Team

class TeamService:
    def __init__(self):
        self.repository = TeamRepository()
    
    def get_all_teams(self):
        return self.repository.get_all()
    
    def get_team_by_id(self, team_id):
        return self.repository.get_by_id(team_id)
    
    def get_team_with_members(self, team_id):
        return self.repository.get_with_members(team_id)
    
    def get_all_teams_with_members(self):
        return self.repository.get_all_with_members()
    
    def save_team(self, team_data):
        team = Team(**team_data)
        return self.repository.save(team)
    
    def delete_team(self, team_id):
        return self.repository.delete(team_id)
    
    def exists_by_name(self, name):
        return self.repository.exists_by_name(name)
    
    def get_total_teams_count(self):
        return self.repository.count_total()