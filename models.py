from flask_security.core import UserMixin, RoleMixin
import secrets
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime


from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


# roles_users = db.Table('roles_users',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
# )

# class Role(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    #email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Use this for storing hashed passwords
    active = db.Column(db.Boolean, default=True)

    # Enum for user roles
    role = db.Column(db.Enum('Sponsor', 'Influencer', 'Admin', name='roles_enum'), nullable=False, default='Admin')
    
    # Ensure uniqueness for this field (optional, based on your requirements)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Relationships to role-specific profiles
    
    influencer_profile=db.relationship('InfluencerProfile', uselist=False,cascade="all,delete",backref='user')
    sponsor_profile=db.relationship('SponsorProfile',uselist=False,cascade="all,delete", backref='user')

    #influencer_profile_rel = db.relationship('InfluencerProfile', uselist=False, back_populates='user_rel', cascade='all, delete-orphan')
    #sponsor_profile_rel = db.relationship('SponsorProfile', uselist=False, back_populates='user_rel', cascade='all, delete-orphan')

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True  # You can just return True since UserMixin provides this functionality

    def set_password(self, password):
        """Hashes and sets the user's password."""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.fs_uniquifier is None:
            self.fs_uniquifier = self._get_unique_identifier()

    @staticmethod
    def _get_unique_identifier():
        return secrets.token_hex(16)
    @property
    def is_anonymous(self):
        return False
    def __repr__(self):
        return f'<User {self.username}>'



class InfluencerProfile(db.Model):
    __tablename__ = 'influencer_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    email = db.Column(db.String(100), nullable=False,unique=True)

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    category = db.Column(db.String(50))
    niche = db.Column(db.String(50))
    reach = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    bio = db.Column(db.Text)
 
    ad_request = db.relationship('AdRequest', backref='influencer_profile', cascade='all, delete-orphan')

    #user_rel = db.relationship('User', back_populates='influencer_profile_rel')
    #ad_request_rel = db.relationship('AdRequest', back_populates='influencer_profile_rel', cascade='all, delete-orphan')

class SponsorProfile(db.Model):
    __tablename__ = 'sponsor_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    #user_rel = db.relationship('User', back_populates='sponsor_profile_rel')
    email = db.Column(db.String(100), nullable=False,unique=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False,unique=True)
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    budget = db.Column(db.Float)
    mobile = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text)
    
    

    campaign= db.relationship('Campaign', backref='sponsor_profile', cascade='all, delete-orphan')

    #campaign_rel = db.relationship('Campaign', back_populates='sponsor_profile_rel', cascade='all, delete-orphan')



class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor_profile.id'))
    #sponsor_profile_rel = db.relationship('SponsorProfile', back_populates='campaign_rel')

    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    visibility = db.Column(db.String(10))  # 'public' or 'private'
    goals = db.Column(db.Text)
    status = db.Column(db.String(20))  # 'draft', 'active', 'completed', 'cancelled'
    total_reach = db.Column(db.Integer, default=0)
    
    ad_request= db.relationship('AdRequest', backref='campaign', cascade='all, delete-orphan')

    #ad_request_rel = db.relationship('AdRequest', back_populates='campaign_rel', cascade='all, delete-orphan')

class AdRequest(db.Model):
    __tablename__ = 'ad_request'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    #campaign_rel = db.relationship('Campaign', back_populates='ad_request_rel')
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer_profile.id'))
    #influencer_profile_rel = db.relationship('InfluencerProfile', back_populates='ad_request_rel')

    messages = db.Column(JSON, default=list)
    #requirements = db.Column(JSON, default=lambda: [])  # This will store a list of tasks
    payment_amount = db.Column(db.Float)
    status = db.Column(db.String(20))  # 'Pending', 'Accepted', 'Rejected'
    progress = db.Column(db.Float, default=0)  # Percentage of completed tasks
    engagement_rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # @property
    # def requirements_list(self):
    #     if not isinstance(self.requirements, list):
    #         return []
    #     return [{"description":req, "completed":False} if isinstance(req, str) else req for req in self.requirements]
