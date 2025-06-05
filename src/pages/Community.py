import streamlit as st
from datetime import datetime, timedelta
from utils import load_css, check_authentication, render_sidebar

# Page configuration
st.set_page_config(page_title="Community", page_icon="💬", layout="wide")

# Load custom CSS
load_css()

# Check authentication
check_authentication()

if st.session_state.get("logged_in", False):
    render_sidebar()

# Initialize community data
if 'community_posts' not in st.session_state:
    st.session_state.community_posts = [
        {
            "id": 1,
            "title": "Best budget grocery stores near campus?",
            "content": "Hi everyone! I'm new to the area and looking for affordable grocery options. Any recommendations for budget-friendly stores near the university campus?",
            "author": "Maria_S",
            "category": "Living Tips",
            "timestamp": "2024-01-10 14:30:00",
            "likes": 12,
            "replies": 8,
            "tags": ["groceries", "budget", "campus"]
        },
        {
            "id": 2,
            "title": "Visa interview experience - F1 student visa",
            "content": "Just had my F1 visa interview yesterday! Thought I'd share my experience to help others. The interview was about 5 minutes long, and they asked about my program, funding, and post-graduation plans.",
            "author": "Alex_K",
            "category": "Visa & Legal",
            "timestamp": "2024-01-09 16:45:00",
            "likes": 25,
            "replies": 15,
            "tags": ["visa", "F1", "interview", "experience"]
        },
        {
            "id": 3,
            "title": "Study group for Computer Science courses",
            "content": "Looking to form a study group for CS students! I'm taking Data Structures and Algorithms this semester. Anyone interested in weekly study sessions?",
            "author": "CodeStudent",
            "category": "Study Groups",
            "timestamp": "2024-01-08 20:15:00",
            "likes": 18,
            "replies": 12,
            "tags": ["study-group", "computer-science", "algorithms"]
        },
        {
            "id": 4,
            "title": "Affordable winter clothing recommendations",
            "content": "Coming from a tropical country and need advice on winter clothing! What are some good brands for warm, affordable winter jackets and boots?",
            "author": "TropicalStudent",
            "category": "Living Tips",
            "timestamp": "2024-01-07 11:20:00",
            "likes": 30,
            "replies": 22,
            "tags": ["winter", "clothing", "budget", "weather"]
        },
        {
            "id": 5,
            "title": "International student meetup this weekend!",
            "content": "Hey everyone! We're organizing a meetup for international students this Saturday at Central Park. Great opportunity to make new friends and share experiences. Who's in?",
            "author": "EventOrganizer",
            "category": "Events",
            "timestamp": "2024-01-06 09:30:00",
            "likes": 45,
            "replies": 28,
            "tags": ["meetup", "friends", "events", "weekend"]
        }
    ]

if 'community_categories' not in st.session_state:
    st.session_state.community_categories = [
        "All", "Living Tips", "Visa & Legal", "Study Groups", "Events", "Housing", "Jobs", "Food & Dining"
    ]

def main():
    st.markdown("""
    <div class="breadcrumb">
        <span>🎓 StudyAbroad Platform</span> > <span>Community</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("💬 Community Forum")
    st.markdown("Connect with fellow international students and share your experiences")
    
    # Community stats
    total_posts = len(st.session_state.community_posts)
    total_likes = sum(post['likes'] for post in st.session_state.community_posts)
    total_replies = sum(post['replies'] for post in st.session_state.community_posts)
    active_users = len(set(post['author'] for post in st.session_state.community_posts))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Posts</h3>
                <div class="metric-value">{total_posts}</div>
                <div class="metric-change positive">Active discussions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Likes</h3>
                <div class="metric-value">{total_likes}</div>
                <div class="metric-change positive">Community engagement</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Total Replies</h3>
                <div class="metric-value">{total_replies}</div>
                <div class="metric-change positive">Helpful responses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-content">
                <h3>Active Users</h3>
                <div class="metric-value">{active_users}</div>
                <div class="metric-change positive">Community members</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create post and filters section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("➕ Create New Post", type="primary", use_container_width=True):
            st.session_state.show_create_post = True
    
    with col2:
        selected_category = st.selectbox("Filter by Category", st.session_state.community_categories)
    
    # Create post modal
    if st.session_state.get('show_create_post', False):
        with st.expander("Create New Post", expanded=True):
            with st.form("create_post_form"):
                post_title = st.text_input("Post Title", placeholder="Enter a descriptive title...")
                post_category = st.selectbox("Category", st.session_state.community_categories[1:])  # Exclude "All"
                post_content = st.text_area("Content", placeholder="Share your thoughts, questions, or experiences...", height=150)
                post_tags = st.text_input("Tags", placeholder="Enter tags separated by commas (e.g., housing, budget, tips)")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Post", use_container_width=True):
                        if post_title and post_content:
                            new_post = {
                                "id": max([post['id'] for post in st.session_state.community_posts]) + 1,
                                "title": post_title,
                                "content": post_content,
                                "author": st.session_state.username,
                                "category": post_category,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "likes": 0,
                                "replies": 0,
                                "tags": [tag.strip() for tag in post_tags.split(',') if tag.strip()]
                            }
                            st.session_state.community_posts.insert(0, new_post)
                            st.session_state.show_create_post = False
                            st.success("Post created successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in both title and content!")
                
                with col2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_create_post = False
                        st.rerun()
    
    # Filter posts
    filtered_posts = st.session_state.community_posts
    if selected_category != "All":
        filtered_posts = [post for post in st.session_state.community_posts if post['category'] == selected_category]
    
    # Sort posts by timestamp (newest first)
    filtered_posts = sorted(filtered_posts, key=lambda x: x['timestamp'], reverse=True)
    
    # Display posts
    st.subheader(f"📋 Recent Posts {f'- {selected_category}' if selected_category != 'All' else ''}")
    
    if not filtered_posts:
        st.info("No posts found in this category. Be the first to start a discussion!")
    else:
        for post in filtered_posts:
            post_time = datetime.strptime(post['timestamp'], "%Y-%m-%d %H:%M:%S")
            time_diff = datetime.now() - post_time
            if time_diff.days > 0:
                time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
            else:
                minutes = time_diff.seconds // 60
                time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"

            with st.expander(post['title']):
                st.write(f"Category: {post['category']} | Author: {post['author']} | {time_ago}")
                st.write(post['content'])
                st.write(f"Tags: {', '.join(post['tags'])}")
                st.write(f"👍 {post['likes']} | 💬 {post['replies']}")
    
    # Popular topics sidebar
    st.subheader("🔥 Trending Topics")
    
    # Count tag frequencies
    all_tags = []
    for post in st.session_state.community_posts:
        all_tags.extend(post['tags'])
    
    from collections import Counter
    tag_counts = Counter(all_tags)
    popular_tags = tag_counts.most_common(10)
    
    if popular_tags:
        cols = st.columns(2)
        for i, (tag, count) in enumerate(popular_tags):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="trending-tag">
                    <span class="trending-tag-name">#{tag}</span>
                    <span class="trending-tag-count">{count} posts</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Community guidelines
    st.subheader("📋 Community Guidelines")
    
    guidelines = [
        "🤝 Be respectful and kind to all community members",
        "💬 Keep discussions relevant and helpful",
        "🚫 No spam, self-promotion, or inappropriate content",
        "🔍 Search before posting to avoid duplicates",
        "💡 Share accurate information and personal experiences",
        "🏷️ Use relevant tags to help others find your posts"
    ]
    
    for guideline in guidelines:
        st.markdown(f"""
        <div class="guideline-item">
            <span class="guideline-text">{guideline}</span>
        </div>
        """, unsafe_allow_html=True)

# Execute the page logic
if __name__ == "__main__":
    main()
