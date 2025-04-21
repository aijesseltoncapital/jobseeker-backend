from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from backend.models.job import Job, SavedJob, JobApplication
from backend.models.user import User

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs/recommended', methods=['GET'])
@jwt_required()
def get_recommended_jobs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Get filter parameters
    filters = request.args.to_dict()
    
    # Logic for job recommendation based on user skills and preferences
    # This would typically use a recommendation algorithm
    recommended_jobs = Job.query.limit(10).all()
    
    return {
        "status": "success",
        "jobs": [job.to_dict() for job in recommended_jobs]
    }

@jobs_bp.route('/jobs', methods=['GET'])
def get_all_jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('type', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    query = Job.query
    
    if search:
        query = query.filter(Job.title.ilike(f'%{search}%') | Job.description.ilike(f'%{search}%'))
    
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    
    if job_type:
        query = query.filter(Job.job_type == job_type)
    
    # Pagination
    total = query.count()
    jobs = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "status": "success",
        "total": total,
        "page": page,
        "limit": limit,
        "jobs": [job.to_dict() for job in jobs]
    }

@jobs_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def quick_apply_job(job_id):
    user_id = get_jwt_identity()
    
    # Check if job exists
    job = Job.query.get(job_id)
    if not job:
        return {"status": "error", "message": "Job not found"}, 404
    
    # Check if already applied
    existing_application = JobApplication.query.filter_by(user_id=user_id, job_id=job_id).first()
    if existing_application:
        return {"status": "error", "message": "Already applied for this job"}, 400
    
    # Create application
    application = JobApplication(user_id=user_id, job_id=job_id)
    db.session.add(application)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Successfully applied to job"
    }

@jobs_bp.route('/job/<int:id>', methods=['GET'])
def view_job_detail(id):
    job = Job.query.get(id)
    if not job:
        return {"status": "error", "message": "Job not found"}, 404
    
    return {
        "status": "success",
        "job": job.to_dict(detailed=True)
    }

@jobs_bp.route('/job/<int:id>/save', methods=['POST'])
@jwt_required()
def save_job(id):
    user_id = get_jwt_identity()
    
    # Check if job exists
    job = Job.query.get(id)
    if not job:
        return {"status": "error", "message": "Job not found"}, 404
    
    # Check if already saved
    existing_save = SavedJob.query.filter_by(user_id=user_id, job_id=id).first()
    if existing_save:
        return {"status": "error", "message": "Job already saved"}, 400
    
    # Save job
    saved_job = SavedJob(user_id=user_id, job_id=id)
    db.session.add(saved_job)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Job saved successfully"
    }

@jobs_bp.route('/job/saved', methods=['GET'])
@jwt_required()
def saved_job_list():
    user_id = get_jwt_identity()
    
    # Get saved jobs
    saved_jobs = SavedJob.query.filter_by(user_id=user_id).all()
    job_ids = [saved.job_id for saved in saved_jobs]
    jobs = Job.query.filter(Job.id.in_(job_ids)).all()
    
    return {
        "status": "success",
        "jobs": [job.to_dict() for job in jobs]
    }

@jobs_bp.route('/jobs/map', methods=['GET'])
def map_view_job_list():
    # Get jobs with location data
    jobs = Job.query.filter(Job.latitude != None, Job.longitude != None).all()
    
    return {
        "status": "success",
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "lat": job.latitude,
                "lng": job.longitude,
                "salary": job.salary
            } for job in jobs
        ]
    }
