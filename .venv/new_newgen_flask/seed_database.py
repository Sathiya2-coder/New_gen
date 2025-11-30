#!/usr/bin/env python
"""
Seed script to populate the database with teams and members data
Run this after creating the app: python seed_database.py
"""

from app import create_app
from models.database import db
from models.entities import Team, Person, ThemeSettings
from datetime import datetime

def seed_database():
    """Populate database with initial teams and members"""
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep data)
        # db.session.query(Person).delete()
        # db.session.query(Team).delete()
        # db.session.query(ThemeSettings).delete()
        
        print("🌱 Starting database seeding...")
        
        # Initialize theme settings
        theme = ThemeSettings.query.filter_by(setting_key='theme.mode').first()
        if not theme:
            theme = ThemeSettings(setting_key='theme.mode', setting_value='dark')
            db.session.add(theme)
            print("✓ Theme settings initialized")
        
        # Teams data
        teams_data = [
            {
                'name': 'Leadership',
                'description': 'CEO, COO, CCO & Core Leadership',
                'icon': 'fa-crown',
                'team_lead': 'REFFINO D'
            },
            {
                'name': 'Technical',
                'description': 'Developers & Technical Experts',
                'icon': 'fa-laptop-code',
                'team_lead': 'SUPRAJA V S'
            },
            {
                'name': 'Communication',
                'description': 'Communication & Documentation Team',
                'icon': 'fa-pen-fancy',
                'team_lead': 'ANTO JANISH B'
            },
            {
                'name': 'Operations',
                'description': 'Operations & Management Team',
                'icon': 'fa-building',
                'team_lead': 'ARUN KUMAR V'
            },
            {
                'name': 'Media',
                'description': 'Media & Promotion Team',
                'icon': 'fa-megaphone',
                'team_lead': 'DEVA DARSHINI R'
            },
            {
                'name': 'Innovation',
                'description': 'Innovation & Volunteers Team',
                'icon': 'fa-lightbulb',
                'team_lead': 'VISHAKAN P'
            }
        ]
        
        # Create teams
        teams = {}
        for team_data in teams_data:
            team = Team.query.filter_by(name=team_data['name']).first()
            if not team:
                team = Team(**team_data)
                db.session.add(team)
                db.session.flush()
            teams[team_data['name']] = team
            print(f"✓ Team '{team_data['name']}' created/updated")
        
        db.session.commit()
        
        # Members data
        members_data = [
            # Leadership Team
            {'first_name': 'REFFINO', 'last_name': 'D', 'email': '2310018@nec.edu.in', 'phone': '8667383450', 'role': 'Chief Executive Officer', 'department': 'Mechanical Engineering', 'team': 'Leadership'},
            {'first_name': 'MIR FAHEEM', 'last_name': 'MEHRAJ', 'email': '2310062@nec.edu.in', 'phone': '6006126500', 'role': 'Chief Operating Officer', 'department': 'Mechanical Engineering', 'team': 'Leadership'},
            {'first_name': 'PON GOPI', 'last_name': 'KRISHNAN P', 'email': '2315044@nec.edu.in', 'phone': '6383897263', 'role': 'Chief Coordination Officer', 'department': 'Information Technology', 'team': 'Leadership'},
            
            # Technical Team
            {'first_name': 'SUPRAJA', 'last_name': 'V S', 'email': '2313031@nec.edu.in', 'phone': '8838458381', 'role': 'Technical Lead', 'department': 'EEE', 'team': 'Technical'},
            {'first_name': 'PRAGATHIJA', 'last_name': 'S', 'email': '24205023@nec.edu.in', 'phone': '9344449628', 'role': 'Developer', 'department': 'IT', 'team': 'Technical'},
            {'first_name': 'J.', 'last_name': 'KARTHIKA', 'email': '24103058@nec.edu.in', 'phone': '9342525539', 'role': 'Developer', 'department': 'Civil', 'team': 'Technical'},
            {'first_name': 'M. MANO', 'last_name': 'SATHIYA MOORTHI', 'email': '24243050@nec.edu.in', 'phone': '9025749011', 'role': 'Developer', 'department': 'AI&DS', 'team': 'Technical'},
            
            # Communication Team
            {'first_name': 'ANTO', 'last_name': 'JANISH B', 'email': '24205007@nec.edu.in', 'phone': '8807627209', 'role': 'Documentation Lead', 'department': 'IT', 'team': 'Communication'},
            {'first_name': 'MOKSHITHA SHREE', 'last_name': 'L', 'email': '24104034@nec.edu.in', 'phone': '9566689801', 'role': 'Content Writer', 'department': 'CSE', 'team': 'Communication'},
            {'first_name': 'S.', 'last_name': 'SOORYA BARATHY', 'email': '2316021@nec.edu.in', 'phone': '6374877058', 'role': 'Documentation Specialist', 'department': 'Civil', 'team': 'Communication'},
            {'first_name': 'MURUGAN', 'last_name': 'P', 'email': '24106097@nec.edu.in', 'phone': '8072881160', 'role': 'Communication Coordinator', 'department': 'ECE', 'team': 'Communication'},
            {'first_name': 'NAGA', 'last_name': 'VARSHINI N', 'email': '24243057@nec.edu.in', 'phone': '8072064223', 'role': 'Content Writer', 'department': 'AI&DS', 'team': 'Communication'},
            
            # Operations Team
            {'first_name': 'ARUN', 'last_name': 'KUMAR V', 'email': '2310003@nec.edu.in', 'phone': '6379364967', 'role': 'Operations Manager', 'department': 'Mechanical', 'team': 'Operations'},
            {'first_name': 'SHIYAM BALA', 'last_name': 'SUNDAR M', 'email': '2310032@nec.edu.in', 'phone': '6384384221', 'role': 'Operations Coordinator', 'department': 'Mechanical', 'team': 'Operations'},
            {'first_name': 'SWEETY FROST', 'last_name': 'A', 'email': '24243056@nec.edu.in', 'phone': '8778316492', 'role': 'Operations Assistant', 'department': 'AI&DS', 'team': 'Operations'},
            {'first_name': 'MOHAMED KAIS IBRAHIM', 'last_name': 'S S', 'email': '24205025@nec.edu.in', 'phone': '8015206467', 'role': 'Logistics Coordinator', 'department': 'IT', 'team': 'Operations'},
            {'first_name': 'BARATH', 'last_name': 'KUMAR V', 'email': '24243054@nec.edu.in', 'phone': '7200854406', 'role': 'Facilities Manager', 'department': 'AI&DS', 'team': 'Operations'},
            
            # Media Team
            {'first_name': 'DEVA DARSHINI', 'last_name': 'R', 'email': '2313029@nec.edu.in', 'phone': '9342378027', 'role': 'Media Lead', 'department': 'EEE', 'team': 'Media'},
            {'first_name': 'NANDHINI', 'last_name': 'S', 'email': '2313025@nec.edu.in', 'phone': '9360204254', 'role': 'Content Creator', 'department': 'EEE', 'team': 'Media'},
            {'first_name': 'PRIYADHARSHINI', 'last_name': 'M', 'email': '24205055@nec.edu.in', 'phone': '9360077673', 'role': 'Social Media Manager', 'department': 'IT', 'team': 'Media'},
            {'first_name': 'SANTHOSH', 'last_name': 'KUMAR S', 'email': '24114060@nec.edu.in', 'phone': '8825550649', 'role': 'Video Editor', 'department': 'Mechanical', 'team': 'Media'},
            
            # Innovation Team
            {'first_name': 'VISHAKAN', 'last_name': 'P', 'email': '2313042@nec.edu.in', 'phone': '9443527897', 'role': 'Innovation Lead', 'department': 'EEE', 'team': 'Innovation'},
            {'first_name': 'ARUNKUMAR', 'last_name': 'S', 'email': '2313032@nec.edu.in', 'phone': '9489889537', 'role': 'Research Coordinator', 'department': 'EEE', 'team': 'Innovation'},
            {'first_name': 'VIJAYARANI', 'last_name': 'B', 'email': '2313034@nec.edu.in', 'phone': '9600664223', 'role': 'Innovation Specialist', 'department': 'EEE', 'team': 'Innovation'},
            {'first_name': 'AHAMED NALL FARHAN', 'last_name': 'A', 'email': '24106041@nec.edu.in', 'phone': '8056782410', 'role': 'Volunteer Coordinator', 'department': 'ECE', 'team': 'Innovation'}
        ]
        
        # Create members
        for member_data in members_data:
            team_name = member_data.pop('team')
            team = teams[team_name]
            
            person = Person.query.filter_by(email=member_data['email']).first()
            if not person:
                person = Person(
                    **member_data,
                    team_id=team.id,
                    join_date=datetime(2023, 6, 15) if '2310' in member_data['email'] or '2313' in member_data['email'] or '2315' in member_data['email'] else datetime(2024, 6, 15),
                    status='Active'
                )
                db.session.add(person)
            else:
                person.team_id = team.id
            
        db.session.commit()
        print(f"✓ {len(members_data)} members created/updated")
        
        print("\n✅ Database seeding completed successfully!")
        print(f"   - {len(teams_data)} teams")
        print(f"   - {len(members_data)} members")

if __name__ == '__main__':
    seed_database()
