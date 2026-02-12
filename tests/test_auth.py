"""
Authentication and Authorization Tests
Tests for user registration, login, logout, and protected routes
"""

import pytest
from flask import session, url_for
from app.models import User
from app import db


class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_registration_page_loads(self, client):
        """Test that registration page is accessible"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data or b'Sign Up' in response.data
    
    def test_successful_registration(self, client, app):
        """Test successful user registration"""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify user was created in database
        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.username == 'newuser'
            assert user.check_password('SecurePass123!')
    
    def test_registration_with_existing_email(self, client):
        """Test registration fails with existing email"""
        response = client.post('/auth/register', data={
            'username': 'anotheruser',
            'email': 'test@example.com',  # Already exists
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'Another',
            'last_name': 'User'
        }, follow_redirects=True)
        
        assert b'Email already registered' in response.data or \
               b'already exists' in response.data
    
    def test_registration_password_mismatch(self, client):
        """Test registration fails when passwords don't match"""
        response = client.post('/auth/register', data={
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        
        assert b'Passwords must match' in response.data or \
               b'do not match' in response.data
    
    def test_registration_weak_password(self, client):
        """Test registration fails with weak password"""
        response = client.post('/auth/register', data={
            'username': 'testuser3',
            'email': 'test3@example.com',
            'password': '123',  # Too weak
            'password2': '123',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        
        # Should fail validation
        assert response.status_code == 200
        assert b'Register' in response.data or b'Sign Up' in response.data


class TestUserLogin:
    """Test user login functionality"""
    
    def test_login_page_loads(self, client):
        """Test that login page is accessible"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'Sign In' in response.data
    
    def test_successful_login(self, client):
        """Test successful login with correct credentials"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check if redirected to dashboard or home
        assert b'Dashboard' in response.data or b'Welcome' in response.data
    
    def test_login_with_username(self, client):
        """Test login using username instead of email"""
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_incorrect_password(self, client):
        """Test login fails with incorrect password"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Invalid' in response.data or b'incorrect' in response.data
    
    def test_login_nonexistent_user(self, client):
        """Test login fails for non-existent user"""
        response = client.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        
        assert b'Invalid' in response.data or b'not found' in response.data
    
    def test_remember_me_functionality(self, client):
        """Test remember me checkbox functionality"""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123',
            'remember_me': True
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Check for remember_me cookie
        assert 'remember_token' in [cookie.name for cookie in client.cookie_jar]


class TestUserLogout:
    """Test user logout functionality"""
    
    def test_logout_when_logged_in(self, client):
        """Test logout when user is logged in"""
        # First login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        # Then logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data.lower() or b'login' in response.data.lower()
    
    def test_logout_when_not_logged_in(self, client):
        """Test logout redirects when not logged in"""
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200


class TestProtectedRoutes:
    """Test access control to protected routes"""
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard requires authentication"""
        response = client.get('/dashboard/', follow_redirects=False)
        assert response.status_code in [302, 401]  # Redirect to login or unauthorized
    
    def test_dashboard_accessible_when_logged_in(self, client):
        """Test dashboard is accessible when logged in"""
        # Login first
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        response = client.get('/dashboard/')
        assert response.status_code == 200
        assert b'Dashboard' in response.data
    
    def test_profile_requires_login(self, client):
        """Test profile page requires authentication"""
        response = client.get('/auth/profile', follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_my_bikes_requires_login(self, client):
        """Test my bikes page requires authentication"""
        response = client.get('/dashboard/my_bikes', follow_redirects=False)
        assert response.status_code in [302, 401]


class TestPasswordReset:
    """Test password reset functionality"""
    
    def test_password_reset_request_page(self, client):
        """Test password reset request page loads"""
        response = client.get('/auth/reset_password_request')
        assert response.status_code == 200
        assert b'Reset Password' in response.data or b'Forgot Password' in response.data
    
    def test_password_reset_request_valid_email(self, client, app):
        """Test password reset request with valid email"""
        with app.mail.record_messages() as outbox:
            response = client.post('/auth/reset_password_request', data={
                'email': 'test@example.com'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            assert len(outbox) == 1  # Email sent
            assert 'reset' in outbox[0].subject.lower()
    
    def test_password_reset_request_invalid_email(self, client):
        """Test password reset request with non-existent email"""
        response = client.post('/auth/reset_password_request', data={
            'email': 'nonexistent@example.com'
        }, follow_redirects=True)
        
        # Should not reveal whether email exists
        assert response.status_code == 200


class TestUserSession:
    """Test user session management"""
    
    def test_session_persists_across_requests(self, client):
        """Test user session persists across multiple requests"""
        # Login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        
        # Make multiple requests
        response1 = client.get('/dashboard/')
        response2 = client.get('/bikes/')
        response3 = client.get('/dashboard/my_bikes')
        
        # All should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
    
    def test_session_expires(self, client, app):
        """Test session expiration"""
        # This would require manipulating session timeout
        # Simplified test
        with client.session_transaction() as sess:
            sess['_user_id'] = '999'  # Non-existent user
        
        response = client.get('/dashboard/', follow_redirects=True)
        # Should redirect to login
        assert b'Login' in response.data or response.status_code == 401


@pytest.fixture
def authenticated_client(client):
    """Fixture providing an authenticated test client"""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    return client
