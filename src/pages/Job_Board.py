import streamlit as st
from datetime import datetime, timedelta
from utils import load_css, check_authentication

# Page configuration
st.set_page_config(page_title="Job Board", page_icon="💼", layout="wide")

# Load custom CSS
load_css()

# Check authentication
check_authentication()

# Initialize job data
if 'job_listings' not in st.session_state:
    st.session_state.job_listings = [
        {
            "id": 1,
            "title": "Campus Library Assistant",
            "company": "University Library",
            "location": "On-Campus",
            "type": "Part-time",
            "hours": "15-20 hours/week",
            "pay": "$15/hour",
            "description": "Assist students with research, organize books, and help with library operations. Perfect for students who love books and helping others.",
            "requirements": ["Current student status", "Good communication skills", "Reliable and punctual"],
            "posted": "2024-01-10",
            "deadline": "2024-01-25",
            "category": "On-Campus",
            "remote": False,
            "student_friendly": True
        },
        {
            "id": 2,
            "title": "Food Service Team Member",
            "company": "Campus Dining Services",
            "location": "Student Union",
            "type": "Part-time",
            "hours": "10-25 hours/week",
            "pay": "$14/hour + meal benefits",
            "description": "Join our dining team! Flexible schedules around class times. Great opportunity to meet other students while earning money.",
            "requirements": ["Food safety certification (we provide training)", "Teamwork skills", "Flexible schedule"],
            "posted": "2024-01-09",
            "deadline": "2024-01-30",
            "category": "On-Campus",
            "remote": False,
            "student_friendly": True
        },
        {
            "id": 3,
            "title": "Tutoring Center Math Tutor",
            "company": "Academic Success Center",
            "location": "Learning Commons",
            "type": "Part-time",
            "hours": "8-15 hours/week",
            "pay": "$18/hour",
            "description": "Help fellow students succeed in mathematics courses. Must have strong math background and excellent communication skills.",
            "requirements": ["A- or better in relevant math courses", "Previous tutoring experience preferred", "Patient and encouraging attitude"],
            "posted": "2024-01-08",
            "deadline": "2024-02-01",
            "category": "On-Campus",
            "remote": False,
            "student_friendly": True
        },
        {
            "id": 4,
            "title": "Social Media Intern",
            "company": "Local Marketing Agency",
            "location": "Downtown",
            "type": "Internship",
            "hours": "15-20 hours/week",
            "pay": "$16/hour",
            "description": "Create engaging content for social media platforms. Great experience for marketing, communications, or business students.",
            "requirements": ["Knowledge of Instagram, TikTok, LinkedIn", "Creative thinking", "Basic design skills (Canva, etc.)"],
            "posted": "2024-01-07",
            "deadline": "2024-01-28",
            "category": "Off-Campus",
            "remote": True,
            "student_friendly": True
        },
        {
            "id": 5,
            "title": "Research Assistant",
            "company": "Psychology Department",
            "location": "Psychology Building",
            "type": "Part-time",
            "hours": "10-15 hours/week",
            "pay": "$17/hour",
            "description": "Assist with ongoing research projects. Gain valuable research experience while contributing to important studies.",
            "requirements": ["Psychology or related major", "Strong attention to detail", "Interest in research"],
            "posted": "2024-01-06",
            "deadline": "2024-02-05",
            "category": "Research",
            "remote": False,
            "student_friendly": True
        },
        {
            "id": 6,
            "title": "Customer Service Representative",
            "company": "TechStart Solutions",
            "location": "Remote",
            "type": "Part-time",
            "hours": "20-25 hours/week",
            "pay": "$19/hour",
            "description": "Provide excellent customer support via chat and email. Flexible remote work perfect for students.",
            "requirements": ["Excellent written communication", "Computer proficiency", "Quiet home workspace"],
            "posted": "2024-01-05",
            "deadline": "2024-01-22",
            "category": "Remote",
            "remote": True,
            "student_friendly": True
        }
    ]

if 'job_applications' not in st.session_state:
    st.session_state.job_applications = []

def main():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Job Board</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("💼 Job Board")
    st.markdown("Find part-time jobs and internships perfect for international students")
    
    # Job statistics
    total_jobs = len(st.session_state.job_listings)
    on_campus_jobs = len([job for job in st.session_state.job_listings if job['category'] == 'On-Campus'])
    remote_jobs = len([job for job in st.session_state.job_listings if job['remote']])
    applied_jobs = len(st.session_state.job_applications)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Jobs</h3>
                <div class="metric-value">{total_jobs}</div>
                <div class="metric-change positive">Available positions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>On-Campus</h3>
                <div class="metric-value">{on_campus_jobs}</div>
                <div class="metric-change positive">Convenient location</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Remote Jobs</h3>
                <div class="metric-value">{remote_jobs}</div>
                <div class="metric-change positive">Work from anywhere</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>My Applications</h3>
                <div class="metric-value">{applied_jobs}</div>
                <div class="metric-change neutral">In progress</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filters
    st.subheader("🔍 Filter Jobs")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        category_filter = st.selectbox("Category", ["All", "On-Campus", "Off-Campus", "Remote", "Research"])
    
    with col2:
        type_filter = st.selectbox("Job Type", ["All", "Part-time", "Internship", "Full-time"])
    
    with col3:
        remote_filter = st.selectbox("Work Style", ["All", "Remote", "In-Person"])
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Newest", "Pay (High to Low)", "Deadline"])
    
    # Filter jobs
    filtered_jobs = st.session_state.job_listings.copy()
    
    if category_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job['category'] == category_filter]
    
    if type_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job['type'] == type_filter]
    
    if remote_filter == "Remote":
        filtered_jobs = [job for job in filtered_jobs if job['remote']]
    elif remote_filter == "In-Person":
        filtered_jobs = [job for job in filtered_jobs if not job['remote']]
    
    # Sort jobs
    if sort_by == "Newest":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x['posted'], reverse=True)
    elif sort_by == "Pay (High to Low)":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: int(x['pay'].split('$')[1].split('/')[0]), reverse=True)
    elif sort_by == "Deadline":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x['deadline'])
    
    # Job listings
    st.subheader(f"📋 Job Listings ({len(filtered_jobs)} found)")
    
    if not filtered_jobs:
        st.info("No jobs found matching your criteria. Try adjusting the filters.")
    else:
        for job in filtered_jobs:
            # Calculate days until deadline
            deadline_date = datetime.strptime(job['deadline'], '%Y-%m-%d')
            days_until_deadline = (deadline_date - datetime.now()).days
            
            # Check if already applied
            already_applied = job['id'] in [app['job_id'] for app in st.session_state.job_applications]
            
            # Job card
            st.markdown(f"""
            <div class="job-card">
                <div class="job-header">
                    <div class="job-title-section">
                        <h4 class="job-title">{job['title']}</h4>
                        <div class="job-company">{job['company']}</div>
                    </div>
                    <div class="job-badges">
                        <span class="badge {job['category'].lower().replace('-', '')}">{job['category']}</span>
                        <span class="badge type">{job['type']}</span>
                        {f'<span class="badge remote">Remote</span>' if job['remote'] else ''}
                        {f'<span class="badge student-friendly">Student Friendly</span>' if job['student_friendly'] else ''}
                    </div>
                </div>
                
                <div class="job-details">
                    <div class="job-detail-item">
                        <span class="detail-icon">📍</span>
                        <span class="detail-text">{job['location']}</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">⏰</span>
                        <span class="detail-text">{job['hours']}</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">💰</span>
                        <span class="detail-text">{job['pay']}</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">📅</span>
                        <span class="detail-text">Apply by: {job['deadline']} ({days_until_deadline} days left)</span>
                    </div>
                </div>
                
                <div class="job-description">
                    {job['description']}
                </div>
                
                <div class="job-requirements">
                    <strong>Requirements:</strong>
                    <ul>
                        {' '.join([f'<li>{req}</li>' for req in job['requirements']])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                if already_applied:
                    st.success("✅ Applied")
                else:
                    if st.button(f"📝 Apply", key=f"apply_{job['id']}"):
                        # Add to applications
                        application = {
                            "job_id": job['id'],
                            "job_title": job['title'],
                            "company": job['company'],
                            "applied_date": datetime.now().strftime("%Y-%m-%d"),
                            "status": "Applied"
                        }
                        st.session_state.job_applications.append(application)
                        st.success("Application submitted successfully!")
                        st.rerun()
            
            with col2:
                if st.button(f"💾 Save", key=f"save_{job['id']}"):
                    st.info("Save feature coming soon!")
            
            with col3:
                if st.button(f"📤 Share", key=f"share_{job['id']}"):
                    st.info("Share feature coming soon!")
            
            st.markdown("---")
    
    # My Applications section
    if st.session_state.job_applications:
        st.subheader("📋 My Applications")
        
        for app in st.session_state.job_applications:
            st.markdown(f"""
            <div class="application-item">
                <div class="application-header">
                    <div class="application-title">{app['job_title']}</div>
                    <div class="application-status">{app['status']}</div>
                </div>
                <div class="application-details">
                    <span class="application-company">{app['company']}</span>
                    <span class="application-date">Applied: {app['applied_date']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Job search tips
    st.subheader("💡 Job Search Tips for International Students")
    
    tips = [
        "🎓 Check if the job allows international students (F-1 visa holders can work on-campus)",
        "📄 Keep your resume updated and tailored for each application",
        "🕒 Apply early - many student positions have limited spots",
        "🤝 Network with professors, staff, and other students for opportunities",
        "📋 Understand work authorization requirements for your visa status",
        "⏰ Balance work hours with academic requirements (typically 20 hours/week max)",
        "💼 Consider positions that offer relevant experience for your field of study",
        "📞 Follow up on applications professionally after a reasonable time"
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="tip-item">
            <span class="tip-text">{tip}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Work authorization info
    st.subheader("📋 Work Authorization Quick Guide")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>🎓 On-Campus Employment</h4>
            <ul>
                <li>✅ No additional authorization needed</li>
                <li>⏰ Up to 20 hours/week during studies</li>
                <li>📍 Must be on university premises</li>
                <li>💼 Includes work-study positions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🏢 Off-Campus Employment</h4>
            <ul>
                <li>📄 Requires additional authorization</li>
                <li>🎯 CPT for curriculum-related work</li>
                <li>⚡ OPT after graduation</li>
                <li>🆘 Economic hardship in special cases</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
