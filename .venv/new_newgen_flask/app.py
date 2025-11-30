from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models.database import db, login_manager
from services.person_service import PersonService
from services.team_service import TeamService
from services.theme_service import ThemeService
from services.contact_service import ContactMessageService
from utils.auth import init_admin_user, verify_password
from models.entities import Person, Team, ContactMessage
from models.database import User
from datetime import datetime
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    # Initialize services
    person_service = PersonService()
    team_service = TeamService()
    theme_service = ThemeService()
    contact_service = ContactMessageService()
    
    with app.app_context():
        db.create_all()
        try:
            theme_service.initialize_default_theme()
        except Exception as e:
            # rollback any failed transaction so subsequent DB calls work
            try:
                db.session.rollback()
            except Exception:
                pass
            print(f"Warning: Theme initialization skipped: {e}")
        init_admin_user()
    
    def load_theme_settings():
        current_theme = theme_service.get_current_theme()
        theme_class = "theme-light" if current_theme == "light" else "theme-dark"
        
        return {
            'theme_mode': current_theme,
            'theme_class': theme_class,
            'app_name': 'NEC NewGen',
            'college_name': 'National Engineering College',
            'colors': Config.THEME_CONFIG.get(current_theme, Config.THEME_CONFIG['dark'])
        }
    
    # Routes
    @app.route('/')
    def introduction():
        return render_template('introduction.html')
    
    @app.route('/home')
    def home():
        context = load_theme_settings()
        context['total_members'] = person_service.count_active_persons()
        context['teams'] = team_service.get_all_teams_with_members()
        return render_template('home.html', **context)
    
    @app.route('/about')
    def about():
        context = load_theme_settings()
        return render_template('about.html', **context)
    
    @app.route('/services')
    def services():
        context = load_theme_settings()
        return render_template('services.html', **context)
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        context = load_theme_settings()
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message_text = request.form.get('message')
            
            if name and email and message_text:
                message_data = {
                    'name': name,
                    'email': email,
                    'message': message_text
                }
                try:
                    contact_service.save_message(message_data)
                    flash('Thank you for your message! We\'ll get back to you soon.', 'success')
                    return redirect(url_for('contact'))
                except Exception as e:
                    flash('Error sending message. Please try again.', 'error')
            else:
                flash('Please fill in all fields.', 'error')
        
        return render_template('contact.html', **context)
    
    @app.route('/persons')
    def list_persons():
        context = load_theme_settings()
        context['persons'] = person_service.get_all_persons()
        context['teams'] = team_service.get_all_teams_with_members()
        context['total_members'] = person_service.count_active_persons()
        context['total_teams'] = team_service.get_total_teams_count()
        return render_template('team_members.html', **context)
    
    @app.route('/team-members')
    def team_members_combined():
        """Combined view for teams and members"""
        context = load_theme_settings()
        context['persons'] = person_service.get_all_persons()
        context['teams'] = team_service.get_all_teams_with_members()
        context['total_members'] = person_service.count_active_persons()
        context['total_teams'] = team_service.get_total_teams_count()
        return render_template('team_members.html', **context)
    
    @app.route('/persons/add', methods=['GET', 'POST'])
    @login_required
    def add_person():
        context = load_theme_settings()
        
        if request.method == 'POST':
            # Get form data
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            role = request.form.get('role')
            department = request.form.get('department')
            join_date_str = request.form.get('joinDate')
            status = request.form.get('status', 'Active')
            team_id = request.form.get('team_id')
            
            # Validate required fields
            if not all([first_name, last_name, email, role, department]):
                flash('Please fill in all required fields.', 'error')
                context['teams'] = team_service.get_all_teams()
                return render_template('persons/add.html', **context)
            
            # Convert join_date if provided
            join_date = None
            if join_date_str:
                try:
                    join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
                except ValueError:
                    join_date = datetime.utcnow().date()
            
            # Check if email already exists
            if person_service.exists_by_email(email):
                flash('A member with this email already exists!', 'error')
                context['teams'] = team_service.get_all_teams()
                return render_template('persons/add.html', **context)
            
            person_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'role': role,
                'department': department,
                'join_date': join_date,
                'status': status,
                'team_id': team_id if team_id else None
            }
            
            try:
                person_service.save_person(person_data)
                flash(f"Member {person_data['first_name']} {person_data['last_name']} added successfully!", 'success')
                return redirect(url_for('list_persons'))
            except Exception as e:
                flash(f'Error adding member: {str(e)}', 'error')
        
        context['teams'] = team_service.get_all_teams()
        return render_template('persons/add.html', **context)
    
    @app.route('/persons/edit/<int:person_id>', methods=['GET', 'POST'])
    @login_required
    def edit_person(person_id):
        context = load_theme_settings()
        person = person_service.get_person_by_id(person_id)
        
        if not person:
            flash('Member not found!', 'error')
            return redirect(url_for('list_persons'))
        
        if request.method == 'POST':
            # Get form data
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            role = request.form.get('role')
            department = request.form.get('department')
            join_date_str = request.form.get('joinDate')
            status = request.form.get('status')
            team_id = request.form.get('team_id')
            
            # Validate required fields
            if not all([first_name, last_name, email, role, department]):
                flash('Please fill in all required fields.', 'error')
                context['person'] = person
                context['teams'] = team_service.get_all_teams()
                return render_template('persons/edit.html', **context)
            
            # Convert join_date if provided
            join_date = person.join_date
            if join_date_str:
                try:
                    join_date = datetime.strptime(join_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            person_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'role': role,
                'department': department,
                'join_date': join_date,
                'status': status,
                'team_id': team_id if team_id else None
            }
            
            try:
                person_service.update_person(person_id, person_data)
                flash(f"Member {person_data['first_name']} {person_data['last_name']} updated successfully!", 'success')
                return redirect(url_for('list_persons'))
            except Exception as e:
                flash(f'Error updating member: {str(e)}', 'error')
        
        context['person'] = person
        context['teams'] = team_service.get_all_teams()
        return render_template('persons/edit.html', **context)
    
    @app.route('/persons/delete/<int:person_id>')
    @login_required
    def delete_person(person_id):
        person = person_service.get_person_by_id(person_id)
        if person:
            try:
                person_service.delete_person(person_id)
                flash(f"Member {person.first_name} {person.last_name} deleted successfully!", 'success')
            except Exception as e:
                flash(f'Error deleting member: {str(e)}', 'error')
        else:
            flash('Member not found!', 'error')
        return redirect(url_for('list_persons'))
    
    @app.route('/persons/team/<int:team_id>')
    def view_team_members(team_id):
        context = load_theme_settings()
        team = team_service.get_team_with_members(team_id)
        
        if not team:
            flash('Team not found!', 'error')
            return redirect(url_for('list_persons'))
        
        context['team'] = team
        context['members'] = [member for member in team.members if member.status == 'Active']
        return render_template('persons/team_members.html', **context)
    
    @app.route('/teams')
    def list_teams():
        # Redirect to combined team members page
        return redirect(url_for('team_members_combined'))
    
    @app.route('/teams/<int:team_id>')
    def view_team(team_id):
        context = load_theme_settings()
        team = team_service.get_team_with_members(team_id)
        
        if not team:
            flash('Team not found!', 'error')
            return redirect(url_for('list_teams'))
        
        context['team'] = team
        return render_template('teams/view.html', **context)
    
    @app.route('/teams/add', methods=['GET', 'POST'])
    @login_required
    def add_team():
        context = load_theme_settings()
        
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            icon = request.form.get('icon')
            team_lead = request.form.get('teamLead')
            
            if not name:
                flash('Team name is required!', 'error')
                return render_template('teams/add.html', **context)
            
            if team_service.exists_by_name(name):
                flash('A team with this name already exists!', 'error')
                return render_template('teams/add.html', **context)
            
            team_data = {
                'name': name,
                'description': description,
                'icon': icon,
                'team_lead': team_lead
            }
            
            try:
                team_service.save_team(team_data)
                flash(f"Team '{team_data['name']}' created successfully!", 'success')
                return redirect(url_for('list_teams'))
            except Exception as e:
                flash(f'Error creating team: {str(e)}', 'error')
        
        return render_template('teams/add.html', **context)
    
    @app.route('/team')
    def team_page():
        context = load_theme_settings()
        context['teams'] = team_service.get_all_teams_with_members()
        return render_template('team.html', **context)
    
    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        context = load_theme_settings()
        
        if request.method == 'POST':
            theme = request.form.get('theme')
            if theme in ['dark', 'light']:
                theme_service.save_theme(theme)
                flash('Theme updated successfully!', 'success')
                # Reload context with new theme
                context = load_theme_settings()
            else:
                flash('Invalid theme selection!', 'error')
        
        return render_template('settings.html', **context)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        context = load_theme_settings()
        
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = verify_password(username, password)
            if user:
                login_user(user)
                flash('Logged in successfully!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                flash('Invalid username or password.', 'error')
        
        return render_template('login.html', **context)
    
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('home'))
    
    # API Routes for AJAX
    @app.route('/api/persons/count')
    def api_persons_count():
        return jsonify({'count': person_service.count_active_persons()})
    
    @app.route('/api/teams/count')
    def api_teams_count():
        return jsonify({'count': team_service.get_total_teams_count()})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        context = load_theme_settings()
        return render_template('404.html', **context), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        context = load_theme_settings()
        return render_template('500.html', **context), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        context = load_theme_settings()
        return render_template('403.html', **context), 403
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=8081)