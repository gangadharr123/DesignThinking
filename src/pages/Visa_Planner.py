import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils import load_css, check_authentication, format_currency, get_country_info, get_housing_options

# Page configuration
st.set_page_config(page_title="Visa Planner", page_icon="📋", layout="wide")

# Load custom CSS
load_css()

# Check authentication
check_authentication()

# Initialize visa data
if 'visa_documents' not in st.session_state:
    st.session_state.visa_documents = [
        {"name": "Passport", "status": "completed", "deadline": "2024-02-01", "priority": "high"},
        {"name": "Bank Statement", "status": "completed", "deadline": "2024-02-15", "priority": "high"},
        {"name": "Letter of Acceptance", "status": "in_progress", "deadline": "2024-03-01", "priority": "high"},
        {"name": "Health Insurance", "status": "pending", "deadline": "2024-03-15", "priority": "medium"},
        {"name": "Accommodation Proof", "status": "pending", "deadline": "2024-04-01", "priority": "medium"},
        {"name": "Financial Sponsorship Letter", "status": "pending", "deadline": "2024-04-15", "priority": "low"},
    ]

if 'visa_timeline' not in st.session_state:
    st.session_state.visa_timeline = [
        {"step": "Research Visa Requirements", "status": "completed", "date": "2024-01-01"},
        {"step": "Gather Required Documents", "status": "in_progress", "date": "2024-02-01"},
        {"step": "Submit Visa Application", "status": "pending", "date": "2024-03-01"},
        {"step": "Attend Visa Interview", "status": "pending", "date": "2024-03-15"},
        {"step": "Receive Visa Decision", "status": "pending", "date": "2024-04-01"},
        {"step": "Book Flight Tickets", "status": "pending", "date": "2024-04-15"},
    ]

def main():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Visa Planner</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("📋 Visa Application Planner")
    st.markdown("Comprehensive visa planning based on your course start date and destination")
    
    # Course start date input
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        course_start_date = st.date_input(
            "📅 Course Start Date",
            value=st.session_state.course_start_date or (datetime.now() + timedelta(days=180)),
            min_value=datetime.now(),
            help="When does your course begin? This affects visa timeline planning."
        )
        
        if course_start_date != st.session_state.course_start_date:
            st.session_state.course_start_date = course_start_date
            st.rerun()
    
    with col2:
        country_info = get_country_info()
        processing_time = country_info.get(st.session_state.selected_country, {}).get('visa_processing_time', '3-4 months')
        st.metric("Visa Processing Time", processing_time)
    
    with col3:
        # Calculate application deadline
        if st.session_state.course_start_date:
            # Recommend starting visa process 6 months before course start
            recommended_start = st.session_state.course_start_date - timedelta(days=180)
            days_until_course = (st.session_state.course_start_date - datetime.now().date()).days
            
            if days_until_course < 180:
                urgency_color = "negative"
                urgency_msg = "URGENT: Apply immediately!"
            elif days_until_course < 240:
                urgency_color = "neutral" 
                urgency_msg = "Start application process soon"
            else:
                urgency_color = "positive"
                urgency_msg = "Good timeline for preparation"
            
            st.markdown(f"""
            <div class="timeline-alert {urgency_color}">
                <h4>⏰ Timeline Status</h4>
                <p><strong>{days_until_course} days</strong> until course starts</p>
                <p>{urgency_msg}</p>
                <p>Recommended start: {recommended_start.strftime('%B %d, %Y')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress overview
    completed_docs = len([doc for doc in st.session_state.visa_documents if doc['status'] == 'completed'])
    total_docs = len(st.session_state.visa_documents)
    progress_percentage = (completed_docs / total_docs) * 100
    
    completed_steps = len([step for step in st.session_state.visa_timeline if step['status'] == 'completed'])
    total_steps = len(st.session_state.visa_timeline)
    timeline_percentage = (completed_steps / total_steps) * 100
    
    # Overview cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Documents Progress</h3>
                <div class="metric-value">{completed_docs}/{total_docs}</div>
                <div class="metric-change {'positive' if progress_percentage > 50 else 'neutral'}">
                    {progress_percentage:.1f}% complete
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Timeline Progress</h3>
                <div class="metric-value">{completed_steps}/{total_steps}</div>
                <div class="metric-change {'positive' if timeline_percentage > 30 else 'neutral'}">
                    {timeline_percentage:.1f}% complete
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Next deadline
        pending_docs = [doc for doc in st.session_state.visa_documents if doc['status'] != 'completed']
        if pending_docs:
            next_deadline = min(pending_docs, key=lambda x: datetime.strptime(x['deadline'], '%Y-%m-%d'))
            days_until = (datetime.strptime(next_deadline['deadline'], '%Y-%m-%d') - datetime.now()).days
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-content">
                    <h3>Next Deadline</h3>
                    <div class="metric-value">{days_until} days</div>
                    <div class="metric-change {'negative' if days_until < 7 else 'neutral'}">
                        {next_deadline['name']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-content">
                    <h3>Next Deadline</h3>
                    <div class="metric-value">None</div>
                    <div class="metric-change positive">All documents completed!</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Two columns layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Document Checklist")
        
        # Group documents by priority
        high_priority = [doc for doc in st.session_state.visa_documents if doc['priority'] == 'high']
        medium_priority = [doc for doc in st.session_state.visa_documents if doc['priority'] == 'medium']
        low_priority = [doc for doc in st.session_state.visa_documents if doc['priority'] == 'low']
        
        for priority, docs in [("High Priority", high_priority), ("Medium Priority", medium_priority), ("Low Priority", low_priority)]:
            if docs:
                st.markdown(f"**{priority}**")
                
                for i, doc in enumerate(docs):
                    status_icon = {"completed": "✅", "in_progress": "🟡", "pending": "⭕"}[doc['status']]
                    status_color = {"completed": "positive", "in_progress": "neutral", "pending": "negative"}[doc['status']]
                    
                    deadline_date = datetime.strptime(doc['deadline'], '%Y-%m-%d')
                    days_until = (deadline_date - datetime.now()).days
                    
                    # Create checkbox for status update
                    checkbox_key = f"doc_checkbox_{doc['name']}"
                    current_completed = doc['status'] == 'completed'
                    
                    col_check, col_content = st.columns([0.1, 0.9])
                    
                    with col_check:
                        is_checked = st.checkbox("Complete", value=current_completed, key=checkbox_key, label_visibility="hidden")
                        if is_checked != current_completed:
                            # Update document status
                            for j, document in enumerate(st.session_state.visa_documents):
                                if document['name'] == doc['name']:
                                    st.session_state.visa_documents[j]['status'] = 'completed' if is_checked else 'pending'
                            st.rerun()
                    
                    with col_content:
                        st.markdown(f"""
                        <div class="document-item {status_color}">
                            <div class="document-header">
                                <span class="document-name">{status_icon} {doc['name']}</span>
                                <span class="document-deadline">Due: {doc['deadline']}</span>
                            </div>
                            <div class="document-status">
                                Status: {doc['status'].replace('_', ' ').title()} 
                                | {days_until} days remaining
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("📅 Application Timeline")
        
        for i, step in enumerate(st.session_state.visa_timeline):
            status_icon = {"completed": "✅", "in_progress": "🔄", "pending": "⏳"}[step['status']]
            status_color = {"completed": "positive", "in_progress": "neutral", "pending": "negative"}[step['status']]
            
            step_date = datetime.strptime(step['date'], '%Y-%m-%d')
            
            # Create checkbox for status update
            checkbox_key = f"step_checkbox_{i}"
            current_completed = step['status'] == 'completed'
            
            col_check, col_content = st.columns([0.1, 0.9])
            
            with col_check:
                is_checked = st.checkbox("Complete", value=current_completed, key=checkbox_key, label_visibility="hidden")
                if is_checked != current_completed:
                    # Update step status
                    st.session_state.visa_timeline[i]['status'] = 'completed' if is_checked else 'pending'
                    st.rerun()
            
            with col_content:
                st.markdown(f"""
                <div class="timeline-item {status_color}">
                    <div class="timeline-content">
                        <div class="timeline-step">{status_icon} {step['step']}</div>
                        <div class="timeline-date">Target Date: {step['date']}</div>
                        <div class="timeline-status">Status: {step['status'].replace('_', ' ').title()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick actions section
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📎 Add Document", use_container_width=True):
            st.session_state.show_add_document = True
    
    with col2:
        if st.button("📅 Add Timeline Step", use_container_width=True):
            st.session_state.show_add_step = True
    
    with col3:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
    
    # Add document modal
    if st.session_state.get('show_add_document', False):
        with st.expander("Add New Document", expanded=True):
            with st.form("add_document_form"):
                doc_name = st.text_input("Document Name")
                doc_deadline = st.date_input("Deadline", datetime.now() + timedelta(days=30))
                doc_priority = st.selectbox("Priority", ["high", "medium", "low"])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Add Document"):
                        new_doc = {
                            "name": doc_name,
                            "status": "pending",
                            "deadline": doc_deadline.strftime("%Y-%m-%d"),
                            "priority": doc_priority
                        }
                        st.session_state.visa_documents.append(new_doc)
                        st.session_state.show_add_document = False
                        st.success("Document added successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.show_add_document = False
                        st.rerun()
    
    # Add timeline step modal
    if st.session_state.get('show_add_step', False):
        with st.expander("Add Timeline Step", expanded=True):
            with st.form("add_step_form"):
                step_name = st.text_input("Step Name")
                step_date = st.date_input("Target Date", datetime.now() + timedelta(days=30))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Add Step"):
                        new_step = {
                            "step": step_name,
                            "status": "pending",
                            "date": step_date.strftime("%Y-%m-%d")
                        }
                        st.session_state.visa_timeline.append(new_step)
                        st.session_state.show_add_step = False
                        st.success("Timeline step added successfully!")
                        st.rerun()
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.show_add_step = False
                        st.rerun()
    
    # Housing Information Section
    st.subheader("🏠 Housing Options in " + st.session_state.selected_city)
    
    housing_options = get_housing_options(st.session_state.selected_city, st.session_state.selected_country)
    
    cols = st.columns(len(housing_options))
    for i, (option_name, details) in enumerate(housing_options.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="housing-option-card">
                <h4>{option_name.replace('_', ' ').title()}</h4>
                <div class="housing-price">{details['price_range']}</div>
                <p>{details['description']}</p>
                
                <div class="housing-pros-cons">
                    <div class="housing-pros">
                        <strong>Pros:</strong>
                        <ul>
                            {' '.join([f'<li>{pro}</li>' for pro in details['pros']])}
                        </ul>
                    </div>
                    <div class="housing-cons">
                        <strong>Cons:</strong>
                        <ul>
                            {' '.join([f'<li>{con}</li>' for con in details['cons']])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips section
    st.subheader("💡 Visa Application Tips")
    
    tips = [
        "Start your visa application process at least 3-4 months before your intended travel date",
        "Always submit original documents or certified copies as required", 
        "Keep multiple copies of all important documents",
        "Check visa processing times regularly as they can vary",
        "Prepare for your visa interview by researching common questions",
        "Maintain sufficient funds in your bank account throughout the process"
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="tip-item">
            <span class="tip-icon">💡</span>
            <span class="tip-text">{tip}</span>
        </div>
        """, unsafe_allow_html=True)

# Execute the page logic
if __name__ == "__main__":
    main()
