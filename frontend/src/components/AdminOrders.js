import React, { useState, useEffect, useMemo } from 'react';
import { 
  Search, ChevronDown, ChevronUp, Calendar, Filter, 
  TrendingUp, Package, XCircle, CheckCircle, Clock,
  MapPin, Phone, Mail, CreditCard, Edit2, Save, X
} from 'lucide-react';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

// Fixed admin location for distance calculation (example: Hyderabad, India)
const ADMIN_LOCATION = { lat: 17.385044, lon: 78.486671 };

const AdminOrders = () => {
  const [orders, setOrders] = useState([]);
  const [expandedOrder, setExpandedOrder] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState({ start: '', end: '' });
  const [cityFilter, setCityFilter] = useState('all');
  const [stateFilter, setStateFilter] = useState('all');
  const [analytics, setAnalytics] = useState(null);
  const [editingOrder, setEditingOrder] = useState(null);
  const [editData, setEditData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders();
    fetchAnalytics();
  }, []);

  const fetchOrders = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(response.data);
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch orders",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/orders/analytics/summary`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(response.data);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    }
  };

  const calculateDistance = (orderCity) => {
    // Simplified distance calculation - in production use proper geocoding API
    // For demo, return random distance based on city name hash
    const hash = orderCity.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return ((hash % 50) + 10).toFixed(1); // Distance between 10-60 km
  };

  const handleCancelOrder = async (orderId, reason) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `${API}/orders/${orderId}/cancel`,
        { cancel_reason: reason },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast({
        title: "Success",
        description: "Order cancelled successfully"
      });
      fetchOrders();
      fetchAnalytics();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to cancel order",
        variant: "destructive"
      });
    }
  };

  const handleUpdateOrder = async (orderId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `${API}/orders/${orderId}/admin-update`,
        editData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast({
        title: "Success",
        description: "Order updated successfully"
      });
      setEditingOrder(null);
      setEditData({});
      fetchOrders();
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update order",
        variant: "destructive"
      });
    }
  };

  const filteredOrders = useMemo(() => {
    return orders.filter(order => {
      // Search filter
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = 
        order.customer_name?.toLowerCase().includes(searchLower) ||
        order.phone?.includes(searchTerm) ||
        order.email?.toLowerCase().includes(searchLower) ||
        order.order_id?.toLowerCase().includes(searchLower);

      // Status filter
      const matchesStatus = statusFilter === 'all' || 
        (statusFilter === 'cancelled' && order.cancelled) ||
        (statusFilter === 'active' && !order.cancelled && order.order_status !== 'delivered') ||
        (statusFilter === 'delivered' && order.order_status === 'delivered');

      // Date filter
      let matchesDate = true;
      if (dateFilter.start || dateFilter.end) {
        const orderDate = new Date(order.created_at);
        if (dateFilter.start) {
          matchesDate = matchesDate && orderDate >= new Date(dateFilter.start);
        }
        if (dateFilter.end) {
          matchesDate = matchesDate && orderDate <= new Date(dateFilter.end + 'T23:59:59');
        }
      }

      // City filter
      const matchesCity = cityFilter === 'all' || order.city === cityFilter;

      // State filter
      const matchesState = stateFilter === 'all' || order.state === stateFilter;

      return matchesSearch && matchesStatus && matchesDate && matchesCity && matchesState;
    });
  }, [orders, searchTerm, statusFilter, dateFilter, cityFilter, stateFilter]);

  const sortedOrders = useMemo(() => {
    return [...filteredOrders].sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );
  }, [filteredOrders]);

  const formatAddress = (order) => {
    if (order.doorNo) {
      return `${order.doorNo}, ${order.building}, ${order.street}, ${order.city}, ${order.state} - ${order.pincode}`;
    }
    return order.address;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-600">Loading orders...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Analytics Dashboard */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <Package className="h-8 w-8 opacity-80" />
              <span className="text-3xl font-bold">{analytics.total_orders}</span>
            </div>
            <p className="text-blue-100">Total Orders</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="h-8 w-8 opacity-80" />
              <span className="text-3xl font-bold">₹{analytics.total_sales.toLocaleString()}</span>
            </div>
            <p className="text-green-100">Total Sales</p>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <Clock className="h-8 w-8 opacity-80" />
              <span className="text-3xl font-bold">{analytics.active_orders}</span>
            </div>
            <p className="text-orange-100">Active Orders</p>
          </div>

          <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between mb-2">
              <XCircle className="h-8 w-8 opacity-80" />
              <span className="text-3xl font-bold">{analytics.cancelled_orders}</span>
            </div>
            <p className="text-red-100">Cancelled</p>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {/* Search */}
          <div className="md:col-span-3 lg:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Orders
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by name, phone, email, or order ID"
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
              />
            </div>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          {/* State Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              State
            </label>
            <select
              value={stateFilter}
              onChange={(e) => setStateFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All States</option>
              {[...new Set(orders.map(o => o.state).filter(Boolean))].sort().map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>

          {/* City Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              City
            </label>
            <select
              value={cityFilter}
              onChange={(e) => setCityFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="all">All Cities</option>
              {[...new Set(orders.map(o => o.city).filter(Boolean))].sort().map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>

          {/* Date Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date Range
            </label>
            <div className="flex space-x-2">
              <input
                type="date"
                value={dateFilter.start}
                onChange={(e) => setDateFilter(prev => ({ ...prev, start: e.target.value }))}
                className="flex-1 px-2 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
              />
              <input
                type="date"
                value={dateFilter.end}
                onChange={(e) => setDateFilter(prev => ({ ...prev, end: e.target.value }))}
                className="flex-1 px-2 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 text-sm"
              />
            </div>
          </div>
        </div>

        {/* Filter Summary */}
        <div className="mt-4 flex items-center justify-between text-sm text-gray-600">
          <span>Showing {sortedOrders.length} of {orders.length} orders</span>
          {(searchTerm || statusFilter !== 'all' || dateFilter.start || dateFilter.end || cityFilter !== 'all' || stateFilter !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('all');
                setDateFilter({ start: '', end: '' });
                setCityFilter('all');
                setStateFilter('all');
              }}
              className="text-orange-600 hover:text-orange-700 font-medium"
            >
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Orders List */}
      <div className="space-y-4">
        {sortedOrders.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <Package className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No orders found</h3>
            <p className="text-gray-500">Try adjusting your filters</p>
          </div>
        ) : (
          sortedOrders.map(order => (
            <div key={order.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
              {/* Order Header - Clickable */}
              <div
                onClick={() => setExpandedOrder(expandedOrder === order.id ? null : order.id)}
                className="p-4 sm:p-6 cursor-pointer hover:bg-gray-50 transition-colors"
              >
                {/* Desktop Layout */}
                <div className="hidden sm:flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                      order.cancelled ? 'bg-red-100' :
                      order.order_status === 'delivered' ? 'bg-green-100' :
                      'bg-blue-100'
                    }`}>
                      {order.cancelled ? <XCircle className="h-6 w-6 text-red-600" /> :
                       order.order_status === 'delivered' ? <CheckCircle className="h-6 w-6 text-green-600" /> :
                       <Clock className="h-6 w-6 text-blue-600" />}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-gray-800">{order.customer_name}</h3>
                      <p className="text-sm text-gray-600">Order #{order.order_id}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-6">
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-800">₹{order.total}</p>
                      <p className="text-sm text-gray-600">
                        {new Date(order.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        order.cancelled ? 'bg-red-100 text-red-700' :
                        order.order_status === 'delivered' ? 'bg-green-100 text-green-700' :
                        'bg-blue-100 text-blue-700'
                      }`}>
                        {order.cancelled ? 'Cancelled' : order.order_status}
                      </span>
                      {expandedOrder === order.id ? 
                        <ChevronUp className="h-5 w-5 text-gray-400" /> : 
                        <ChevronDown className="h-5 w-5 text-gray-400" />
                      }
                    </div>
                  </div>
                </div>

                {/* Mobile Layout */}
                <div className="sm:hidden space-y-3">
                  {/* Top row: Icon and Name */}
                  <div className="flex items-start space-x-3">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                      order.cancelled ? 'bg-red-100' :
                      order.order_status === 'delivered' ? 'bg-green-100' :
                      'bg-blue-100'
                    }`}>
                      {order.cancelled ? <XCircle className="h-5 w-5 text-red-600" /> :
                       order.order_status === 'delivered' ? <CheckCircle className="h-5 w-5 text-green-600" /> :
                       <Clock className="h-5 w-5 text-blue-600" />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-base font-bold text-gray-800 truncate">{order.customer_name}</h3>
                      <p className="text-xs text-gray-600 truncate">Order #{order.order_id}</p>
                    </div>
                    {expandedOrder === order.id ? 
                      <ChevronUp className="h-5 w-5 text-gray-400 flex-shrink-0" /> : 
                      <ChevronDown className="h-5 w-5 text-gray-400 flex-shrink-0" />
                    }
                  </div>

                  {/* Middle row: Price and Date */}
                  <div className="flex items-center justify-between pl-13">
                    <div>
                      <p className="text-lg font-bold text-gray-800">₹{order.total}</p>
                      <p className="text-xs text-gray-600">
                        {new Date(order.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>

                  {/* Bottom row: Status Badge */}
                  <div className="pl-13">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                      order.cancelled ? 'bg-red-100 text-red-700' :
                      order.order_status === 'delivered' ? 'bg-green-100 text-green-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {order.cancelled ? 'Cancelled' : order.order_status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Expanded Order Details */}
              {expandedOrder === order.id && (
                <div className="border-t border-gray-200 p-6 bg-gray-50">
                  <div className="grid md:grid-cols-2 gap-6">
                    {/* Customer Details */}
                    <div className="space-y-4">
                      <h4 className="font-semibold text-gray-800 mb-3">Customer Details</h4>
                      <div className="flex items-start space-x-3">
                        <Phone className="h-5 w-5 text-gray-400 mt-0.5" />
                        <div>
                          <p className="text-sm text-gray-600">Phone</p>
                          <p className="font-medium">{order.phone}</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <Mail className="h-5 w-5 text-gray-400 mt-0.5" />
                        <div>
                          <p className="text-sm text-gray-600">Email</p>
                          <p className="font-medium">{order.email}</p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <MapPin className="h-5 w-5 text-gray-400 mt-0.5" />
                        <div>
                          <p className="text-sm text-gray-600">Delivery Address</p>
                          <p className="font-medium">{formatAddress(order)}</p>
                          <p className="text-sm text-gray-600 mt-1">{order.location}</p>
                          <p className="text-xs text-blue-600 mt-1">
                            📍 ~{calculateDistance(order.city || 'Unknown')} km from you
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-3">
                        <CreditCard className="h-5 w-5 text-gray-400 mt-0.5" />
                        <div>
                          <p className="text-sm text-gray-600">Payment</p>
                          <p className="font-medium capitalize">{order.payment_method}</p>
                          {order.payment_sub_method && (
                            <p className="text-sm text-gray-600">{order.payment_sub_method}</p>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Order Items */}
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-3">Order Items</h4>
                      <div className="space-y-3">
                        {order.items?.map((item, idx) => (
                          <div key={idx} className="flex items-center justify-between bg-white p-3 rounded-lg">
                            <div className="flex items-center space-x-3">
                              {item.image && (
                                <img 
                                  src={item.image} 
                                  alt={item.name} 
                                  className="w-12 h-12 object-cover rounded"
                                />
                              )}
                              <div>
                                <p className="font-medium text-gray-800">{item.name}</p>
                                <p className="text-sm text-gray-600">{item.weight}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <p className="font-medium">₹{item.price} × {item.quantity}</p>
                              <p className="text-sm text-gray-600">₹{item.price * item.quantity}</p>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* Order Summary */}
                      <div className="mt-4 pt-4 border-t border-gray-200 space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Subtotal</span>
                          <span className="font-medium">₹{order.subtotal}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Delivery Charge</span>
                          <span className="font-medium">₹{order.delivery_charge}</span>
                        </div>
                        <div className="flex justify-between text-lg font-bold pt-2 border-t">
                          <span>Total</span>
                          <span className="text-green-600">₹{order.total}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Admin Actions */}
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <h4 className="font-semibold text-gray-800 mb-3">Admin Actions</h4>
                    
                    {editingOrder === order.id ? (
                      <div className="space-y-4">
                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Order Status
                            </label>
                            <select
                              value={editData.order_status || order.order_status}
                              onChange={(e) => setEditData(prev => ({ ...prev, order_status: e.target.value }))}
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                            >
                              <option value="pending">Pending</option>
                              <option value="confirmed">Confirmed</option>
                              <option value="processing">Processing</option>
                              <option value="shipped">Shipped</option>
                              <option value="out for delivery">Out for Delivery</option>
                              <option value="delivered">Delivered</option>
                            </select>
                          </div>

                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Delivery Days
                            </label>
                            <input
                              type="number"
                              min="1"
                              value={editData.delivery_days || order.delivery_days || ''}
                              onChange={(e) => setEditData(prev => ({ ...prev, delivery_days: parseInt(e.target.value) }))}
                              placeholder="Enter delivery days"
                              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                            />
                          </div>
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Admin Notes
                          </label>
                          <textarea
                            value={editData.admin_notes || order.admin_notes || ''}
                            onChange={(e) => setEditData(prev => ({ ...prev, admin_notes: e.target.value }))}
                            placeholder="Add notes about this order..."
                            rows="3"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                        </div>

                        <div className="flex space-x-3">
                          <button
                            onClick={() => handleUpdateOrder(order.order_id)}
                            className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                          >
                            <Save className="h-4 w-4" />
                            <span>Save Changes</span>
                          </button>
                          <button
                            onClick={() => {
                              setEditingOrder(null);
                              setEditData({});
                            }}
                            className="flex items-center space-x-2 bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
                          >
                            <X className="h-4 w-4" />
                            <span>Cancel</span>
                          </button>
                        </div>
                      </div>
                    ) : (
                      <div className="flex flex-wrap gap-3">
                        <button
                          onClick={() => {
                            setEditingOrder(order.id);
                            setEditData({
                              order_status: order.order_status,
                              admin_notes: order.admin_notes || '',
                              delivery_days: order.delivery_days || ''
                            });
                          }}
                          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                        >
                          <Edit2 className="h-4 w-4" />
                          <span>Edit Order</span>
                        </button>

                        {!order.cancelled && (
                          <button
                            onClick={() => {
                              const reason = prompt('Enter cancellation reason:');
                              if (reason) handleCancelOrder(order.order_id, reason);
                            }}
                            className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
                          >
                            <XCircle className="h-4 w-4" />
                            <span>Cancel Order</span>
                          </button>
                        )}

                        {(order.admin_notes || order.delivery_days) && (
                          <div className="w-full mt-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                            {order.delivery_days && (
                              <p className="text-sm">
                                <span className="font-semibold">Delivery Time:</span> {order.delivery_days} days
                              </p>
                            )}
                            {order.admin_notes && (
                              <p className="text-sm mt-2">
                                <span className="font-semibold">Notes:</span> {order.admin_notes}
                              </p>
                            )}
                          </div>
                        )}

                        {order.cancelled && order.cancel_reason && (
                          <div className="w-full p-4 bg-red-50 border border-red-200 rounded-lg">
                            <p className="text-sm">
                              <span className="font-semibold text-red-700">Cancellation Reason:</span> {order.cancel_reason}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default AdminOrders;
