from flask import Flask, render_template, redirect, url_for, flash,request,session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,EmailField,IntegerField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os,sys
from models import *
from forms import *
import secrets
from flask_wtf import CSRFProtect
from sqlalchemy import create_engine, inspect,or_,and_
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


# Initializin Variables
load_dotenv()
app=None
def init_app():
    try:
        ISECP_app = Flask(__name__)
        ISECP_app.debug=True
        ISECP_app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///ISECP_DB.sqlite3'
        ISECP_app.app_context().push()
        db.init_app(ISECP_app)
        print(" IESCP Database Started... ")
        return ISECP_app
    except Exception as e:
        print(f"Error initializing app: {e}", file=sys.stderr)

app=init_app()
app.config['SECRET_KEY'] =secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=4)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)
app.config['SESSION_PERMANENT'] = True
csrf = CSRFProtect(app)
#-----------Database Creation One Time-----------
#from models import db #only db import nothing else
#from app import *
#db.create_all() Dont need to use
#-----------End----------------------------------
print(os.environ['SQLALCHEMY_DATABASE_URI'],file=sys.stderr)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message ="You, are not an authicated user !"

def connection_test():
    try:
        engine = create_engine('sqlite:///instance/ISECP_DB.sqlite3')
        inspector = inspect(engine)
        print("Connection to the database successful!\nTables in the database:")
        tab="user"
        print(inspector.get_table_names())
        print(f"Columns in '{tab}' table:")
        if f'{tab}' in inspector.get_table_names():
            print(inspector.get_columns(tab))
        else:
            print(f"{tab} table does not exist.")    
            db.create_all() 
            print("Now, tables created successfully!")

    except Exception as e:
        print(f"Error connecting to the database: {e}",file=sys.stderr)


@login_manager.user_loader
def load_user(user_id):
    try:
        user = User.query.filter_by(fs_uniquifier=user_id).first()
        print(f'Load User :  {user_id}, Found: {user}',file=sys.stderr)
        return user
    except Exception as e:
        print(f"Error loading user: {e}", file=sys.stderr)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Log In Bool:",form.validate_on_submit(), file=sys.stderr)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            print("User Authenticated:",current_user.is_authenticated,file=sys.stderr)
            
            print(f"Current User {user.username} and it's role: {user.role}", file=sys.stderr)
            if user.role == 'Admin':
                print("Inside Admin Role")
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'Sponsor':
                return redirect(url_for('sponsor_dashboard'))
            elif user.role == 'Influencer':
                return redirect(url_for('influencer_dashboard'))
        else:
            flash('Invalid Credentials ! Please Re-try .','danger')
            render_template('login.html',msg="Invalid Credentials !",form=form)
        
    return render_template('login.html',msg="",form=form)



@app.route('/register_influencer', methods=['GET', 'POST'])
def registerInfluencer():
    try:
        form = RegistrationForm()
        if request.method=="POST":      
            uname=form.username.data
            pwd=form.password.data
            full_name=request.form.get("name")
            email=form.email.data
            age=request.form.get("age")
            category=request.form.get("category")
            niche=request.form.get("niche")
            reach=request.form.get("reach")
            followers=request.form.get("followers")
            bio=request.form.get("bio")
            role=request.form.get("role")
            usr=User.query.filter_by(username=uname).first() #Get existig user matched
            print("-----Table Data-----",usr)
            if not usr:
                #Adding Into User Table
                new_user=User(username=uname,role=role)
                new_user.set_password(pwd)
                db.session.add(new_user)
                new_user=User.query.filter_by(username=uname).first()

                #Adding Into Influencer Table
                print(new_user.id, file=sys.stderr)
                influencer_profile=InfluencerProfile(user_id=new_user.id, name=full_name, email=email, age=age, category=category, niche=niche, reach=reach, followers=followers, bio=bio)
                db.session.add(influencer_profile)
                db.session.commit()
                return render_template("home.html")
            else:
                return render_template("influencer_signup.html",msg="Sorry, User is already existed!!",form=form)
        
        
        return render_template('influencer_signup.html',msg="",form=form)
    except Exception as e:
        print(f"Error in Influencer Registration: {e}", file=sys.stderr)  

@app.route('/register_sponsor', methods=['GET', 'POST'])
def registerSponsor():
    try:
        form = RegistrationForm()
        if request.method=="POST":        
            uname=form.username.data
            pwd=form.password.data
            full_name=request.form.get("name")
            email=form.email.data
            
            industry=request.form.get("industry")
            budget=request.form.get("budget")
            company=request.form.get("company")
            mobile=request.form.get("mobile")
            des=request.form.get("description")
            role=request.form.get("role") #hidden field
            usr=User.query.filter_by(username=uname).first() #Get existig user matched
            if not usr:
                #Adding Into User Table
                new_user=User(username=uname,role=role)
                new_user.set_password(pwd)
                db.session.add(new_user)
                new_user=User.query.filter_by(username=uname).first()
                #Adding Into Sponsor Table*9[]
                print(new_user.id,file=sys.stderr)
                print(new_user.fs_uniquifier,file=sys.stderr)
                new_sponsor_profile=SponsorProfile(user_id=new_user.id,name=full_name,email=email,company_name=company,industry=industry,budget=budget,mobile=mobile,description=des)
                db.session.add(new_sponsor_profile)
                db.session.commit()
                return render_template("home.html")
            else:
                return render_template("sponsor_signup.html",msg="Sorry, User with same id is already existed!!",form=form)
        return render_template('sponsor_signup.html', msg="",form=form)   
    except Exception as e:
        print(f"Error in Sponsor Registration: {e}", file=sys.stderr)        

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    print("Current User In Admin Dashboard: ",current_user)
    print(dir(current_user))
    print("Auth:",current_user.is_authenticated,file=sys.stderr)
    if current_user.is_authenticated:
        return render_template('admin_dashboard.html')
    print("Current Use:{current_user.role}",file=sys.stderr)
    if current_user.role != 'Admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/sponsor_dashboard')
@login_required
def sponsor_dashboard():
    form=RegistrationForm()
    if current_user.role == 'Sponsor':
        if request.method == 'POST':
            pass
        sponsor_data=fetch_user(current_user.id)
        return render_template('sponsor_dashboard.html',sponsor=sponsor_data.sponsor_profile,form=form)
    else:
        redirect(url_for('login'))
    return render_template('sponsor_dashboard.html',sponsor="",form=form)

@app.route('/influencer_dashboard')
@login_required
def influencer_dashboard():
    form=RegistrationForm()
    if current_user.role == 'Influencer':
        if request.method == 'POST':
            pass
        influencer_data=fetch_user(current_user.id)
        return render_template('influencer_dashboard.html',influencer=influencer_data.influencer_profile,form=form)
    else:
        redirect(url_for('login'))
    return render_template('influencer_dashboard.html',influencer="",form=form)


@app.route('/sponsoredit/<int:user_id>',methods=['GET','POST'])
@login_required
def update_sponsor(user_id):
    try:
        print("....Update Sponsor Data....",file=sys.stderr)
        #user = User.query.get_or_404(user_id)
        form = RegistrationForm()
        if request.method=="POST":
            new_name=request.form.get("name")
            new_email=request.form.get("email")
            new_company=request.form.get("company")
            

            new_industry=request.form.get("industry")
            new_budget=request.form.get("budget")
            new_mobile=request.form.get("mobile")
            new_bio=request.form.get("bio")
            print(new_bio, file=sys.stderr)


            sponsor=SponsorProfile.query.filter_by(user_id=user_id).first()
            print(new_name,new_email,new_budget,new_company,new_mobile,new_bio,new_industry, file=sys.stderr)
            sponsor.name=new_name
            sponsor.email=new_email
            sponsor.company_name=new_company
            sponsor.industry=new_industry
            sponsor.budget=new_budget
            sponsor.mobile=new_mobile
            sponsor.description=new_bio
            print(sponsor, file=sys.stderr)

            db.session.commit()
            print(dir(sponsor), file=sys.stderr)
            return render_template("sponsor_dashboard.html",sponsor=sponsor,form=form)
    
        
        return render_template('sponsor_dashboard.html',sponsor="",form=form)
    except Exception as e:
        print(f"Error in Sponsor Update: {e}", file=sys.stderr)

@app.route('/influenceredit/<int:user_id>',methods=['GET','POST'])
@login_required
def update_influencer(user_id):
    try:
        print("....Update Influencer Data....",file=sys.stderr)
        #user = User.query.get_or_404(user_id)
        form = RegistrationForm()
        if request.method=="POST":
            new_name=request.form.get("name")
            new_email=request.form.get("email")
            new_age=request.form.get("age")
            

            new_category=request.form.get("category")
            new_niche=request.form.get("niche")
            new_reach=request.form.get("reach")
            new_followers=request.form.get("followers")
            new_bio=request.form.get("bio")
            print(new_bio, file=sys.stderr)


            influencer=InfluencerProfile.query.filter_by(user_id=user_id).first()
            #print(new_name,new_email,new_budget,new_company,new_mobile,new_bio,new_industry, file=sys.stderr)
            influencer.name=new_name
            influencer.email=new_email
            influencer.age=new_age
            influencer.category=new_category
            influencer.niche=new_niche
            influencer.reach=new_reach
            influencer.followers=new_followers
            influencer.bio=new_bio
            print(influencer, file=sys.stderr)

            db.session.commit()
            print(dir(influencer), file=sys.stderr)
            return render_template("influencer_dashboard.html",influencer=influencer,form=form)
    
        
        return render_template('influencer_dashboard.html',influencer="",form=form)
    except Exception as e:
        print(f"Error in Sponsor Update: {e}", file=sys.stderr)

# @app.route('/user/delete/<int:user_id>', methods=['POST'])
# @login_required
# def delete_user(user_id):
#     if request.method=="POST":
#         title=request.form.get("title")
#         list_obj=Lists.query.filter_by(user_id=user_id,title=title).first()
#         db.session.delete(list_obj)
#         db.session.commit()
#         user_info=fetch_user_info(user_id)
#         return render_template("user_dashboard.html",id=user_info.id,name=user_info.user_name,lists=user_info.lists)
@app.route('/search_influencer', methods=['GET','POST'])
@login_required
def search_influencer():
    try:
        form=RegistrationForm()
        print("\nSearch Influencer ", file=sys.stderr)
        if request.method=="POST":
            data=dict(list(request.form.items()))
            print(f"Search Fileds: {data}", file=sys.stderr)

            camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()
            #influencer=InfluencerProfile.query.filter_by(reach=data['reach']).all()
            influencer = InfluencerProfile.query.filter(or_(InfluencerProfile.reach == data['reach'],InfluencerProfile.category == data['category'],InfluencerProfile.niche == data['niche'],InfluencerProfile.followers == data['followers'])).all()
            print("Search Influencers:\n:",dir(influencer),influencer, file=sys.stderr)
            return render_template("search_influencer.html",influencers=influencer,camp_all=camp_all,form=form)
        
        return render_template("search_influencer.html",influencers="",camp_all="",form=form)      
    except Exception as e:
        print(f"Error in Search Influencer: {e}", file=sys.stderr) 

@app.route('/adrequest', methods=['GET','POST'])
@login_required
def adrequest():
    try:
        form=AdditionalForm()

        if request.method=="POST":
            data=dict(list(request.form.items()))
            print(f"Ad Fields: {data}", file=sys.stderr)
            adRequest=AdRequest.query.filter_by(influencer_id=data['influencerId'],campaign_id=data['dropdownSelect'].split("#")[1]).all()
            print(adRequest)
            if not adRequest:
                if data['payment_amount']=='':
                    data['payment_amount']=0
                adRequest=AdRequest(influencer_id=data['influencerId'], campaign_id=data['dropdownSelect'].split("#")[1],messages=data['requirements'],payment_amount=data['payment_amount'],progress='0',engagement_rate='0', status="Pending",created_at=datetime.today())
                db.session.add(adRequest)
                db.session.commit()
            print("After Adding Ad Request:\t", adRequest, file=sys.stderr)
            #return render_template("ad_request.html", form=form, adRequests=[adRequest])      
        print("------4-----")
        camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()
        print("Ad Request all Campaigns:\t",camp_all)
        adRequest_=[AdRequest.query.filter_by(campaign_id=camp.id).all() for camp in camp_all] 
        adRequest=[adReq for adReq in adRequest_ if adReq is not None]
        adRequest=sum(adRequest, [])
        print("******:\t", adRequest)
        print("Matched Ads from Adrequest table are ",adRequest,dir(adRequest[0]),dir(adRequest[0].influencer_profile))
        
       

        return render_template("ad_request.html",form=form,adRequests=adRequest)      
    except Exception as e:
        print(f"Error in ad Request Influencer: {e}", file=sys.stderr)     

@app.route('/delete_adrequest', methods=['POST'])
@login_required
def delete_adrequest():
    try:
        form=RegistrationForm()
        print("\nDelete Ad-request Send ! ", file=sys.stderr)
        print(request.method, file=sys.stderr)
    
        data=dict(list(request.form.items()))
        print(f"Delete Ad Fields: {data}", file=sys.stderr)
        #Delete
        adRequest=AdRequest.query.filter_by(influencer_id=data['influencer_Id'],campaign_id=data['campaignid']).first()
        db.session.delete(adRequest)
        db.session.commit()
        camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()
        print("Delete Ad Request all Campaigns:\t",camp_all)
        adRequest=[]
        adRequest=[AdRequest.query.filter_by(campaign_id=camp.id).first() for camp in camp_all]

        return render_template("ad_request.html",form=form,adRequests=adRequest) 
    
            
        
    except Exception as e:
        print(f"Error in Delete ad Request : {e}", file=sys.stderr)     

@app.route('/create_campaign', methods=['GET','POST'])
@login_required
def create_campaign():
    try:
        form=CampaignForm()
        print("Campaign Creation..", file=sys.stderr)
        if request.method=="POST":
            name=form.name.data
            description=form.description.data
            budget=form.budget.data
            start_date=form.start_date.data
            end_date=form.end_date.data
            visibility=form.visibility.data
            goals=request.form.get("goals")
            status=form.status.data
            total_reach=request.form.get("total_reach")
            print(name, budget, description, file=sys.stderr)
            new_campaign=Campaign(sponsor_id=current_user.id,name=name,description=description,start_date=start_date,end_date=end_date,budget=budget,visibility=visibility,goals=goals,status=status,total_reach=total_reach)
            db.session.add(new_campaign)
            db.session.commit()
            return render_template("create_campaign.html", form=form)
        else:
            return render_template("create_campaign.html", form=form)      
    except Exception as e:
        print(f"Error in Campaign Creation: {e}", file=sys.stderr)  

@app.route('/my_campaigns', methods=['GET','POST'])
@login_required
def my_campaigns():    
    try:
        form=CampaignForm()
        camp=Campaign.query.filter_by(sponsor_id=current_user.id).all()
        print("Capaigns\t:",dir(camp),camp, file=sys.stderr)

        return render_template("my_campaigns_dashboard.html", campaigns=camp,form=form)
    except Exception as e:
        print(f"Error in My Campaigns: {e}", file=sys.stderr)          

@app.route('/campaignedit', methods=['GET','POST'])
@login_required
def update_campaign():
    try:
        print("....Update Campaign Data....",file=sys.stderr)
        #user = User.query.get_or_404(user_id)
        form = CampaignForm()
        camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()
        if request.method=="POST":
            cm_id=request.form.get("campaignid")
            new_name=request.form.get("name")
            new_description=request.form.get("description")
            new_budget=request.form.get("budget")
            new_start_date=datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
            new_end_date=datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
            # new_visibility=request.form.get("visibility")
            new_visibility=form.visibility.data
            new_goals=request.form.get("goals")
            new_status=form.status.data
            new_total_reach=request.form.get("total_reach")
            print("new_budget:",new_budget)
            if new_budget=="":
                new_budget=0
            print("Campaign Id:\t",cm_id, file=sys.stderr)
            camp=Campaign.query.filter_by(id=cm_id).first()
            camp.name=new_name
            camp.description=new_description
            camp.budget=new_budget
            camp.start_date=new_start_date
            camp.end_date=new_end_date
            camp.visibility=new_visibility
            camp.goals=new_goals
            camp.status=new_status
            camp.total_reach=new_total_reach
      
            db.session.commit()
            camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()

            print("Database updated Successfully.", file=sys.stderr)
            return render_template("my_campaigns_dashboard.html",campaigns=camp_all,form=form)
    
        print("Capaign Update Get Methos:",dir(camp),camp, file=sys.stderr)
        return render_template('my_campaigns_dashboard.html',campaigns=camp_all,form=form)
    except Exception as e:
        print(f"Error in Campaign Update: {e}", file=sys.stderr)

@app.route('/deletecampaign', methods=['GET','POST'])
@login_required
def delete_campaign():
    try:
        print("....Delete Campaign Data....",file=sys.stderr)
        form = CampaignForm()
        camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()
        if request.method=="POST":
            cm_id=request.form.get("campaignid")
            camp=Campaign.query.filter_by(id=cm_id).first()
            db.session.delete(camp)
            db.session.commit()
            camp_all=Campaign.query.filter_by(sponsor_id=current_user.id).all()

            print("Delete Campaigns Successfully.", file=sys.stderr)
            return render_template("my_campaigns_dashboard.html",campaigns=camp_all,form=form)
    
        print("Capaign Delete Get Methods:",dir(camp),camp, file=sys.stderr)
        return render_template('my_campaigns_dashboard.html',campaigns=camp_all,form=form)
    except Exception as e:
        print(f"Error in Delete Campaign: {e}", file=sys.stderr)        


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def fetch_user(userid):
    user=User.query.filter_by(id=userid).first()
    return user

def add_admin():
    usr=User.query.filter_by(username=os.environ['ADMIN_USER_NAME']).first()
    if not usr:
        new_user=User(username=os.environ['ADMIN_USER_NAME'],role=os.environ['ADMIN_ROLE'])
        new_user.set_password(os.environ["ADMIN_PASSWORD"])
        db.session.add(new_user)
        db.session.commit()
    
if __name__ == "__main__":
    connection_test()
    add_admin()
    app.run(debug=True)
