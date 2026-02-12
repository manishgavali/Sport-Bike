from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.accident_reports import AccidentReport
from app.models.bike import Bike
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
@login_required
def index():
    reports = AccidentReport.query.filter_by(user_id=current_user.id).order_by(
        AccidentReport.incident_date.desc()
    ).all()
    return render_template('reports/view_reports.html', reports=reports)

@reports_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == 'POST':
        report = AccidentReport(
            user_id=current_user.id,
            bike_id=request.form.get('bike_id', type=int),
            incident_date=datetime.strptime(request.form.get('incident_date'), '%Y-%m-%dT%H:%M'),
            location=request.form.get('location'),
            severity=request.form.get('severity'),
            incident_type=request.form.get('incident_type'),
            description=request.form.get('description'),
            weather_condition=request.form.get('weather_condition'),
            road_condition=request.form.get('road_condition'),
            damage_description=request.form.get('damage_description'),
            estimated_cost=request.form.get('estimated_cost', type=float)
        )
        
        db.session.add(report)
        db.session.commit()
        
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('reports.index'))
    
    bikes = Bike.query.filter_by(is_active=True).all()
    return render_template('reports/submit_report.html', bikes=bikes)

@reports_bp.route('/public')
def public_reports():
    # Show anonymized public reports for community awareness
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Get filters from query params
    severity = request.args.get('severity')
    incident_type = request.args.get('incident_type')
    bike_id = request.args.get('bike_id', type=int)
    
    query = AccidentReport.query
    
    # Apply filters
    if severity:
        query = query.filter_by(severity=severity)
    if incident_type:
        query = query.filter_by(incident_type=incident_type)
    if bike_id:
        query = query.filter_by(bike_id=bike_id)
    
    # Paginate results
    reports = query.order_by(
        AccidentReport.incident_date.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Get all bikes for filter dropdown
    bikes = Bike.query.filter_by(is_active=True).order_by(Bike.brand, Bike.model).all()
    
    # Get statistics for info cards
    from sqlalchemy import func
    total_reports = AccidentReport.query.count()
    severity_stats = dict(
        db.session.query(
            AccidentReport.severity, func.count(AccidentReport.id)
        ).group_by(AccidentReport.severity).all()
    )
    incident_type_stats = dict(
        db.session.query(
            AccidentReport.incident_type, func.count(AccidentReport.id)
        ).group_by(AccidentReport.incident_type).all()
    )
    
    return render_template('reports/public_reports.html',
                         reports=reports,
                         bikes=bikes,
                         total_reports=total_reports,
                         severity_stats=severity_stats,
                         incident_type_stats=incident_type_stats,
                         current_severity=severity,
                         current_incident_type=incident_type,
                         current_bike_id=bike_id)
