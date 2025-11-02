# TODO List for Instagram-like Social Platform Transformation

## 1. Database Setup
- [x] Set up SQLite database with tables for users, posts, follows, notifications, stories
- [x] Create database models and migration scripts
- [x] Update app.py to use SQLAlchemy or similar ORM

## 2. User Profile Enhancements
- [x] Add profile photo upload functionality to registration and profile editing
- [x] Update user model to include profile_photo field
- [x] Create profile photo storage and serving

## 3. Follow/Follow Back System
- [ ] Create follow/unfollow routes and database relationships
- [ ] Add follow/follow back buttons on user profiles
- [ ] Update profile page to show followers/following counts
- [ ] Implement mutual follow detection

## 4. Post System with Video Uploads
- [ ] Create post creation form with video upload for fitness/games
- [ ] Integrate with existing activity recognition for auto-tagging
- [ ] Add post display in social feed
- [ ] Implement like/comment system on posts

## 5. Stories Feature
- [ ] Create stories table with expiration (24 hours)
- [ ] Add story creation with video/photo upload
- [ ] Display stories bar on main feed
- [ ] Implement story viewing with progress indicators

## 6. Social Feed
- [ ] Create main feed showing posts from followed users
- [ ] Add infinite scroll or pagination
- [ ] Implement post ranking/algorithm (simple chronological for now)

## 7. Enhanced Notifications
- [ ] Expand notification settings (follows, likes, comments, story views)
- [ ] Create notifications table and real-time updates
- [ ] Add notification center/page
- [ ] Implement push notifications (if possible)

## 8. UI/UX Updates
- [ ] Redesign main interface to be more Instagram-like
- [ ] Add bottom navigation bar for mobile experience
- [ ] Update profile pages with grid layout for posts
- [ ] Make responsive for mobile devices

## 9. Search and Discovery
- [ ] Add user search functionality
- [ ] Implement activity/game-based discovery
- [ ] Add trending posts/stories

## 10. Testing and Deployment
- [ ] Test all new social features
- [ ] Ensure integration with existing activity recognition
- [ ] Update GitHub with new features
- [ ] Deploy to production environment
