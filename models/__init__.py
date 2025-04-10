from app import db

# Import models to make them available for migrations
from models.user import User
from models.job import Job, SavedJob, JobApplication
from models.message import Message, Conversation
from models.notification import Notification
from models.credential import Credential
from models.payment import Payment
from models.reward import Reward
from models.schedule import Schedule
