from app import db

# Import models to make them available for migrations
from backend.models.user import User
from backend.models.job import Job, SavedJob, JobApplication
from backend.models.message import Message, Conversation
from backend.models.notification import Notification
from backend.models.credential import Credential
from backend.models.payment import Payment
from backend.models.reward import Reward
from backend.models.schedule import Schedule
