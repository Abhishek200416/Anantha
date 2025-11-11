import React, { useState, useEffect } from 'react';
import { Bell } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const NotificationBell = () => {
  const [notificationCount, setNotificationCount] = useState(0);
  const [isAdmin, setIsAdmin] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is admin - check both on mount and periodically
    const checkAdminStatus = () => {
      const token = localStorage.getItem('token');
      const user = localStorage.getItem('user');
      let isAdminUser = false;
      
      if (user) {
        try {
          const userData = JSON.parse(user);
          isAdminUser = userData.is_admin === true;
        } catch (e) {
          console.error('Error parsing user data:', e);
        }
      }
      
      setIsAdmin(isAdminUser && !!token);
      
      if (isAdminUser && token) {
        fetchNotificationCount();
      }
    };
    
    // Check immediately
    checkAdminStatus();
    
    // Check every 2 seconds for login status changes and refresh notifications
    const interval = setInterval(checkAdminStatus, 2000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchNotificationCount = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/admin/notifications/count`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        const total = (data.bug_reports || 0) + (data.city_suggestions || 0) + (data.new_orders || 0);
        setNotificationCount(total);
      }
    } catch (error) {
      console.error('Error fetching notification count:', error);
    }
  };

  const handleClick = () => {
    navigate('/admin');
  };

  // Don't render if not admin
  if (!isAdmin) {
    return null;
  }

  return (
    <button
      onClick={handleClick}
      className="relative p-2 text-gray-700 hover:text-orange-600 transition-colors"
      title="Admin Notifications"
    >
      <Bell className="h-6 w-6" />
      {notificationCount > 0 && (
        <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold animate-pulse">
          {notificationCount > 99 ? '99+' : notificationCount}
        </span>
      )}
    </button>
  );
};

export default NotificationBell;