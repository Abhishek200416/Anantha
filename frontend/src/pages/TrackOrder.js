import React, { useState } from 'react';
import { Search, Package, Truck, CheckCircle, Clock, MapPin, Mail, Phone, CreditCard, Calendar, User, XCircle } from 'lucide-react';
import axios from 'axios';
import { toast } from '../hooks/use-toast';
import CancelOrderModal from '../components/CancelOrderModal';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TrackOrder = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('online');
  const [paymentSubMethod, setPaymentSubMethod] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!searchTerm.trim()) {
      toast({ title: 'Error', description: 'Please enter Order ID, Tracking Code, Phone Number, or Email', variant: 'destructive' });
      return;
    }

    setLoading(true);
    setSearched(true);

    try {
      const response = await axios.get(`${API}/orders/track/${searchTerm.trim()}`);
      setOrder(response.data);
    } catch (error) {
      setOrder(null);
      if (error.response && error.response.status === 404) {
        toast({ 
          title: 'Order Not Found', 
          description: 'No order found with this information. Please check and try again, or contact support if you recently placed an order.', 
          variant: 'destructive' 
        });
      } else {
        toast({ 
          title: 'Error', 
          description: 'Failed to search for order. Please try again.', 
          variant: 'destructive' 
        });
      }
    }

    setLoading(false);
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'confirmed':
      case 'pending':
        return <Clock className="h-8 w-8 text-yellow-500" />;
      case 'processing':
        return <Package className="h-8 w-8 text-blue-500" />;
      case 'shipped':
      case 'out for delivery':
        return <Truck className="h-8 w-8 text-purple-500" />;
      case 'delivered':
        return <CheckCircle className="h-8 w-8 text-green-500" />;
      default:
        return <Package className="h-8 w-8 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'confirmed':
      case 'pending':
        return 'bg-yellow-100 text-yellow-700';
      case 'processing':
        return 'bg-blue-100 text-blue-700';
      case 'shipped':
      case 'out for delivery':
        return 'bg-purple-100 text-purple-700';
      case 'delivered':
        return 'bg-green-100 text-green-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const formatAddress = (order) => {
    if (order.doorNo || order.building) {
      // New format with separate fields
      return (
        <>
          <p>{order.doorNo}, {order.building}</p>
          <p>{order.street}</p>
          <p>{order.city}, {order.state} - {order.pincode}</p>
        </>
      );
    }
    // Old format with single address field
    return <p>{order.address}</p>;
  };

  const handleCancelOrder = async (cancelReason) => {
    try {
      // Use customer cancellation endpoint
      await axios.post(
        `${API}/orders/${order.order_id}/cancel-customer`,
        { cancel_reason: cancelReason }
      );

      toast({
        title: "Order Cancelled Successfully",
        description: "Your order has been cancelled. Cancellation fee of ₹20 will be deducted if payment was made. Refund will be processed within 2-3 business days.",
        duration: 8000
      });

      // Refresh order data
      const response = await axios.get(`${API}/orders/track/${searchTerm.trim()}`);
      setOrder(response.data);
    } catch (error) {
      console.error('Cancel order error:', error);
      toast({
        title: "Cancellation Failed",
        description: error.response?.data?.detail || "Failed to cancel order. Please try again or contact support.",
        variant: "destructive",
        duration: 6000
      });
    }
  };

  const canCancelOrder = (order) => {
    if (!order) return false;
    if (order.cancelled) return false;
    
    // Check if order is within 20-minute cancellation window
    const orderTime = new Date(order.created_at);
    const now = new Date();
    const minutesPassed = (now - orderTime) / (1000 * 60);
    
    const cancelableStatuses = ['confirmed', 'pending'];
    return minutesPassed <= 20 && cancelableStatuses.includes(order.order_status?.toLowerCase());
  };

  const getRemainingCancellationTime = (order) => {
    if (!order) return null;
    const orderTime = new Date(order.created_at);
    const now = new Date();
    const minutesPassed = (now - orderTime) / (1000 * 60);
    const minutesRemaining = Math.max(0, 20 - minutesPassed);
    return Math.ceil(minutesRemaining);
  };

  const canCompletePayment = (order) => {
    if (!order) return false;
    return order.payment_status === 'pending' && 
           order.order_status === 'confirmed' && 
           !order.cancelled;
  };

  const handleCompletePayment = async () => {
    try {
      // Show payment method selection (in a real app, this would open payment gateway)
      const paymentMethod = 'online';
      const paymentSubMethod = 'upi'; // Default to UPI
      
      const response = await axios.post(
        `${API}/orders/${order.order_id}/complete-payment`,
        { 
          payment_method: paymentMethod,
          payment_sub_method: paymentSubMethod
        }
      );

      toast({
        title: "Payment Completed",
        description: "Your payment has been recorded successfully! Your order is now confirmed.",
        duration: 6000
      });

      // Refresh order data
      const updatedOrder = await axios.get(`${API}/orders/track/${searchTerm.trim()}`);
      setOrder(updatedOrder.data);
    } catch (error) {
      console.error('Payment error:', error);
      toast({
        title: "Payment Failed",
        description: error.response?.data?.detail || "Failed to complete payment. Please try again.",
        variant: "destructive",
        duration: 6000
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-red-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-4">
              Track Your Order
            </h1>
            <p className="text-gray-600 text-lg">
              Enter your Order ID, Tracking Code (from email), Phone Number, or Email to track your order
            </p>
          </div>

          {/* Search Box */}
          <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
            <form onSubmit={handleSearch} className="flex space-x-3">
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Enter Order ID, Tracking Code, Phone Number, or Email"
                  className="w-full pl-12 pr-4 py-4 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-8 py-4 rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all disabled:opacity-50 flex items-center space-x-2"
              >
                {loading ? (
                  <span>Searching...</span>
                ) : (
                  <>
                    <Search className="h-5 w-5" />
                    <span>Track</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Order Details */}
          {order && (
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              {/* Order Header */}
              <div className="bg-gradient-to-r from-orange-500 to-red-500 p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">Order #{order.order_id}</h2>
                    <p className="text-orange-100">Tracking Code: {order.tracking_code}</p>
                  </div>
                  <div className="bg-white/20 backdrop-blur-sm rounded-xl p-4">
                    {getStatusIcon(order.order_status)}
                  </div>
                </div>
              </div>

              {/* Status Badge */}
              <div className="p-6 border-b">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="flex-1">
                    <p className="text-gray-600 text-sm mb-1">Current Status</p>
                    <span className={`inline-block px-4 py-2 rounded-full font-semibold text-lg ${getStatusColor(order.order_status)}`}>
                      {order.order_status?.toUpperCase()}
                      {order.cancelled && <span className="ml-2">(CANCELLED)</span>}
                    </span>
                  </div>
                  <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center w-full sm:w-auto">
                    <div className="text-left sm:text-right">
                      <p className="text-gray-600 text-sm mb-1">Order Date</p>
                      <p className="font-semibold">{new Date(order.created_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
                    </div>
                    {canCompletePayment(order) && (
                      <button
                        onClick={handleCompletePayment}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white rounded-lg transition-all font-medium shadow-md text-sm whitespace-nowrap"
                      >
                        <CreditCard className="h-4 w-4" />
                        Complete Payment
                      </button>
                    )}
                    {canCancelOrder(order) && (
                      <div className="flex flex-col gap-2">
                        <button
                          onClick={() => setShowCancelModal(true)}
                          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white rounded-lg transition-all font-medium shadow-md text-sm whitespace-nowrap"
                        >
                          <XCircle className="h-4 w-4" />
                          Cancel Order
                        </button>
                        <p className="text-xs text-orange-600 font-medium">
                          ⏱️ {getRemainingCancellationTime(order)} min left • ₹20 fee applies
                        </p>
                      </div>
                    )}
                  </div>
                </div>
                {order.cancelled && order.cancel_reason && (
                  <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 rounded-r-lg">
                    <p className="text-sm font-semibold text-red-900 mb-1">Cancellation Reason:</p>
                    <p className="text-sm text-red-700">{order.cancel_reason}</p>
                  </div>
                )}
              </div>

              {/* Customer & Delivery Info - Enhanced */}
              <div className="p-6 grid md:grid-cols-2 gap-6 border-b bg-gray-50">
                <div className="bg-white p-4 rounded-lg shadow-sm">
                  <h3 className="font-bold text-gray-800 mb-4 flex items-center space-x-2 text-lg border-b pb-2">
                    <User className="h-5 w-5 text-orange-600" />
                    <span>Customer Details</span>
                  </h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <p className="text-gray-500 text-xs uppercase mb-1">Full Name</p>
                      <p className="text-gray-800 font-semibold">{order.customer_name}</p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs uppercase mb-1">Phone Number</p>
                      <p className="text-gray-800 font-semibold flex items-center space-x-2">
                        <Phone className="h-4 w-4 text-orange-600" />
                        <span>{order.phone}</span>
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-500 text-xs uppercase mb-1">Email Address</p>
                      <p className="text-gray-800 font-semibold flex items-center space-x-2">
                        <Mail className="h-4 w-4 text-orange-600" />
                        <span>{order.email}</span>
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg shadow-sm">
                  <h3 className="font-bold text-gray-800 mb-4 flex items-center space-x-2 text-lg border-b pb-2">
                    <MapPin className="h-5 w-5 text-orange-600" />
                    <span>Delivery Address</span>
                  </h3>
                  <div className="text-sm text-gray-700 space-y-1">
                    {formatAddress(order)}
                    <p className="font-semibold text-orange-600 mt-3">
                      Location: {order.location}
                    </p>
                  </div>
                </div>
              </div>

              {/* Payment Information - New Section */}
              <div className="p-6 border-b bg-white">
                <h3 className="font-bold text-gray-800 mb-4 flex items-center space-x-2 text-lg">
                  <CreditCard className="h-5 w-5 text-orange-600" />
                  <span>Payment Information</span>
                </h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-500 text-xs uppercase mb-1">Payment Method</p>
                    <p className="text-gray-800 font-semibold capitalize">
                      {order.payment_method === 'online' ? 'Online Payment' : order.payment_method}
                    </p>
                    {order.payment_sub_method && (
                      <p className="text-sm text-gray-600 mt-1">{order.payment_sub_method}</p>
                    )}
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-500 text-xs uppercase mb-1">Payment Status</p>
                    <p className={`font-semibold capitalize ${
                      order.payment_status === 'completed' ? 'text-green-600' : 'text-yellow-600'
                    }`}>
                      {order.payment_status}
                    </p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-500 text-xs uppercase mb-1">Order Status</p>
                    <p className="font-semibold capitalize text-blue-600">
                      {order.order_status}
                    </p>
                  </div>
                </div>
                
                {/* Pending Payment Notice */}
                {order.payment_status === 'pending' && !order.cancelled && (
                  <div className="mt-4 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
                    <div className="flex items-start">
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-yellow-900 mb-2">⚠️ Payment Pending</p>
                        <p className="text-sm text-yellow-700 mb-3">
                          {order.custom_city_request 
                            ? "Your order is awaiting city approval. Once approved, you can complete payment using the 'Complete Payment' button above."
                            : "Please complete payment to confirm your order. Click the 'Complete Payment' button above to proceed."}
                        </p>
                        {order.custom_city_request && (
                          <p className="text-xs text-yellow-600 italic">
                            You'll receive an email notification once your city is approved for delivery.
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Order Items */}
              <div className="p-6 border-b">
                <h3 className="font-bold text-gray-800 mb-4 text-lg">Order Items</h3>
                <div className="space-y-3">
                  {order.items?.map((item, index) => (
                    <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <img src={item.image} alt={item.name} className="w-20 h-20 object-cover rounded-lg shadow-sm" />
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-800 text-lg">{item.name}</h4>
                        <p className="text-sm text-gray-600 mt-1">{item.weight} x {item.quantity}</p>
                        {item.description && (
                          <p className="text-xs text-gray-500 mt-1">{item.description}</p>
                        )}
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">Price</p>
                        <p className="font-bold text-orange-600 text-lg">₹{item.price * item.quantity}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Order Summary - Enhanced */}
              <div className="p-6 bg-gradient-to-br from-gray-50 to-orange-50">
                <h3 className="font-bold text-gray-800 mb-4 text-lg">Order Summary</h3>
                <div className="space-y-3">
                  <div className="flex justify-between text-gray-700">
                    <span className="font-medium">Subtotal:</span>
                    <span className="font-semibold">₹{order.subtotal}</span>
                  </div>
                  <div className="flex justify-between text-gray-700">
                    <span className="font-medium">Delivery Charge:</span>
                    <span className="font-semibold">₹{order.delivery_charge}</span>
                  </div>
                  <div className="flex justify-between items-center text-2xl font-bold border-t-2 border-orange-200 pt-3 mt-2">
                    <span>Total Amount:</span>
                    <span className="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                      ₹{order.total}
                    </span>
                  </div>
                </div>

                <div className="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg">
                  <div className="flex items-start space-x-3">
                    <Calendar className="h-5 w-5 text-yellow-600 mt-0.5" />
                    <div>
                      <p className="text-sm font-semibold text-yellow-800 mb-1">Important Note</p>
                      <p className="text-sm text-yellow-700">
                        You will receive a confirmation call from our team. For any queries, contact us at <strong className="text-yellow-900">9985116385</strong>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* No Results */}
          {searched && !order && !loading && (
            <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
              <Package className="h-24 w-24 text-gray-300 mx-auto mb-4" />
              <h3 className="text-2xl font-bold text-gray-800 mb-2">Order Not Found</h3>
              <p className="text-gray-600">
                We couldn't find an order with the provided information.
                <br />Please check your Order ID, Tracking Code, Phone Number, or Email and try again.
                <br />If you just placed an order, it may take a few moments to appear in our system.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Cancel Order Modal */}
      <CancelOrderModal
        isOpen={showCancelModal}
        onClose={() => setShowCancelModal(false)}
        onConfirm={handleCancelOrder}
        orderDetails={order}
      />
    </div>
  );
};

export default TrackOrder;
