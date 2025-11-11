import React, { useState, useEffect, useRef } from 'react';
import { Bell, X, Bug, MapPin, ShoppingBag } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const NotificationBell = () => {
  const [notificationCount, setNotificationCount] = useState(0);
  const [notificationData, setNotificationData] = useState({ bug_reports: 0, city_suggestions: 0, new_orders: 0 });
  const [isAdmin, setIsAdmin] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [recentNotifications, setRecentNotifications] = useState([]);
  const [swipedNotification, setSwipedNotification] = useState(null);
  const [swipeOffset, setSwipeOffset] = useState({});
  const [touchStart, setTouchStart] = useState(null);
  const dropdownRef = useRef(null);
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
    
    // Check every 5 seconds for login status changes and refresh notifications
    const interval = setInterval(checkAdminStatus, 5000);
    
    return () => clearInterval(interval);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

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
        setNotificationData(data);
        const total = (data.bug_reports || 0) + (data.city_suggestions || 0) + (data.new_orders || 0);
        setNotificationCount(total);
        
        // Build recent notifications array
        const notifications = [];
        if (data.bug_reports > 0) {
          notifications.push({
            type: 'bug_reports',
            icon: Bug,
            color: 'text-red-600',
            bgColor: 'bg-red-50',
            title: 'New Bug Reports',
            count: data.bug_reports,
            message: `${data.bug_reports} new bug ${data.bug_reports === 1 ? 'report' : 'reports'} to review`,
            tab: 'reports'
          });
        }
        if (data.city_suggestions > 0) {
          notifications.push({
            type: 'city_suggestions',
            icon: MapPin,
            color: 'text-blue-600',
            bgColor: 'bg-blue-50',
            title: 'City Suggestions',
            count: data.city_suggestions,
            message: `${data.city_suggestions} new city ${data.city_suggestions === 1 ? 'suggestion' : 'suggestions'}`,
            tab: 'settings'
          });
        }
        if (data.new_orders > 0) {
          notifications.push({
            type: 'new_orders',
            icon: ShoppingBag,
            color: 'text-green-600',
            bgColor: 'bg-green-50',
            title: 'New Orders',
            count: data.new_orders,
            message: `${data.new_orders} new ${data.new_orders === 1 ? 'order' : 'orders'} to process`,
            tab: 'orders'
          });
        }
        setRecentNotifications(notifications);
      }
    } catch (error) {
      console.error('Error fetching notification count:', error);
    }
  };

  const handleBellClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleNotificationClick = (notification) => {
    setShowDropdown(false);
    // Navigate with section parameter for auto-scroll
    if (notification.type === 'city_suggestions') {
      navigate(`/admin?tab=delivery&section=city-suggestions`);
    } else if (notification.type === 'bug_reports') {
      navigate(`/admin?tab=reports`);
    } else if (notification.type === 'new_orders') {
      navigate(`/admin?tab=orders`);
    } else {
      navigate(`/admin?tab=${notification.tab}`);
    }
  };

  const handleViewAll = () => {
    setShowDropdown(false);
    navigate('/admin');
  };

  // Don't render if not admin
  if (!isAdmin) {
    return null;
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={handleBellClick}
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

      {/* Notification Dropdown */}
      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 md:w-96 bg-white rounded-lg shadow-2xl border border-gray-200 z-50 max-h-96 overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-orange-50 to-red-50">
            <h3 className="font-bold text-gray-800 text-lg">Notifications</h3>
            <button
              onClick={() => setShowDropdown(false)}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Notifications List */}
          <div className="divide-y divide-gray-100">
            {recentNotifications.length > 0 ? (
              <>
                {recentNotifications.map((notification, index) => {
                  const IconComponent = notification.icon;
                  return (
                    <button
                      key={index}
                      onClick={() => handleNotificationClick(notification.tab)}
                      className="w-full p-4 hover:bg-gray-50 transition-colors text-left"
                    >
                      <div className="flex items-start gap-3">
                        <div className={`flex-shrink-0 ${notification.bgColor} rounded-full p-2`}>
                          <IconComponent className={`h-5 w-5 ${notification.color}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center justify-between mb-1">
                            <p className="font-semibold text-gray-900 text-sm">
                              {notification.title}
                            </p>
                            <span className={`${notification.bgColor} ${notification.color} text-xs font-bold px-2 py-1 rounded-full`}>
                              {notification.count}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">
                            {notification.message}
                          </p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </>
            ) : (
              <div className="p-8 text-center">
                <Bell className="h-12 w-12 text-gray-300 mx-auto mb-2" />
                <p className="text-gray-500 text-sm">No new notifications</p>
              </div>
            )}
          </div>

          {/* Footer */}
          {recentNotifications.length > 0 && (
            <div className="p-3 bg-gray-50 border-t border-gray-200">
              <button
                onClick={handleViewAll}
                className="w-full text-center text-orange-600 hover:text-orange-700 font-semibold text-sm py-2 rounded-lg hover:bg-orange-50 transition-colors"
              >
                View All in Admin Panel
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationBell;