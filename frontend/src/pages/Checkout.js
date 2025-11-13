import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../hooks/use-toast';
import { ShoppingBag, MapPin, Phone, Mail, CreditCard, Wallet, User, Home, Building, MapPinned, Navigation, Sparkles, Trash2, Edit, Check } from 'lucide-react';

const API = process.env.REACT_APP_BACKEND_URL;

function Checkout() {
  const navigate = useNavigate();
  const { cart, clearCart, updateCartItem, removeFromCart, cartTotal } = useCart();
  const { user } = useAuth();
  const { toast } = useToast();

  // Form state
  const [customerName, setCustomerName] = useState(user?.name || '');
  const [customerEmail, setCustomerEmail] = useState(user?.email || '');
  const [customerPhone, setCustomerPhone] = useState(user?.phone || '');
  
  // Structured address fields
  const [doorNo, setDoorNo] = useState('');
  const [building, setBuilding] = useState('');
  const [street, setStreet] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [pincode, setPincode] = useState('');
  
  const [paymentMethod, setPaymentMethod] = useState('razorpay');
  const [paymentSubMethod, setPaymentSubMethod] = useState('upi');
  const [loading, setLoading] = useState(false);
  const [deliveryCharge, setDeliveryCharge] = useState(0);
  const [deliveryLocations, setDeliveryLocations] = useState([]);
  const [detectingLocation, setDetectingLocation] = useState(false);
  const [previousSearchQuery, setPreviousSearchQuery] = useState('');
  const [previousSearchResults, setPreviousSearchResults] = useState([]);
  const [showPreviousResults, setShowPreviousResults] = useState(false);
  const [locationsByState, setLocationsByState] = useState({
    "Andhra Pradesh": [],
    "Telangana": []
  });
  const [editingItemIndex, setEditingItemIndex] = useState(null);
  const [selectedWeight, setSelectedWeight] = useState('');
  const [allProducts, setAllProducts] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [freeDeliverySettings, setFreeDeliverySettings] = useState({ enabled: true, threshold: 1000 });
  const [showCustomCityInput, setShowCustomCityInput] = useState(false);
  const [customCity, setCustomCity] = useState('');
  const [customCityState, setCustomCityState] = useState('');
  const [customCityDeliveryCharge, setCustomCityDeliveryCharge] = useState(199);

  // Enrich cart items with full product data
  const enrichedCart = React.useMemo(() => {
    return cart.map(item => {
      const product = allProducts.find(p => p.id === item.id);
      if (product) {
        return {
          ...item,
          prices: product.prices, // Add available price options from product
          description: product.description
        };
      }
      return item;
    });
  }, [cart, allProducts]);

  useEffect(() => {
    if (cart.length === 0) {
      navigate('/');
      return;
    }
    
    fetchAllProducts();
    fetchDeliveryLocations();
    fetchFreeDeliverySettings();
    loadPreviousOrderData();
  }, []);

  useEffect(() => {
    calculateDeliveryCharge();
  }, [city, deliveryLocations, freeDeliverySettings, cartTotal]);

  const fetchAllProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setAllProducts(response.data);
      
      // Get random recommendations (excluding items in cart)
      const cartProductIds = cart.map(item => item.id);
      const availableProducts = response.data.filter(p => !cartProductIds.includes(p.id));
      
      // Shuffle and get random 4 products
      const shuffled = [...availableProducts].sort(() => Math.random() - 0.5);
      const randomRecommendations = shuffled.slice(0, 4);
      
      setRecommendations(randomRecommendations);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    }
  };

  const fetchDeliveryLocations = async () => {
    try {
      const response = await axios.get(`${API}/locations`);
      const locations = response.data;
      console.log('📦 Fetched delivery locations:', locations.length);
      setDeliveryLocations(locations);

      // Group locations by state
      const groupedByState = {
        "Andhra Pradesh": [],
        "Telangana": []
      };

      locations.forEach(loc => {
        if (groupedByState[loc.state]) {
          groupedByState[loc.state].push(loc);
        }
      });

      // Sort each state's cities alphabetically
      groupedByState["Andhra Pradesh"].sort((a, b) => a.name.localeCompare(b.name));
      groupedByState["Telangana"].sort((a, b) => a.name.localeCompare(b.name));

      setLocationsByState(groupedByState);
    } catch (error) {
      console.error('Failed to fetch locations:', error);
    }
  };

  const fetchFreeDeliverySettings = async () => {
    try {
      const response = await axios.get(`${API}/settings/free-delivery`);
      setFreeDeliverySettings(response.data);
    } catch (error) {
      console.error('Failed to fetch free delivery settings:', error);
    }
  };

  const loadPreviousOrderData = () => {
    // Check if there's a phone number stored in localStorage from previous orders
    const storedPhone = localStorage.getItem('lastOrderPhone');
    if (storedPhone && !customerPhone) {
      setCustomerPhone(storedPhone);
    }
  };

  const handlePreviousOrderSearch = async () => {
    if (!previousSearchQuery.trim()) {
      toast({
        title: "Search Required",
        description: "Please enter phone number or email to search previous orders",
        variant: "destructive"
      });
      return;
    }

    try {
      const response = await axios.get(`${API}/orders/track/${previousSearchQuery.trim()}`);
      if (response.data.orders && response.data.orders.length > 0) {
        setPreviousSearchResults(response.data.orders);
        setShowPreviousResults(true);
        toast({
          title: "Orders Found",
          description: `Found ${response.data.total} order(s) for ${previousSearchQuery}`,
        });
      } else {
        toast({
          title: "No Orders Found",
          description: "No previous orders found with this phone or email",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch previous orders",
        variant: "destructive"
      });
    }
  };

  const fillFromPreviousOrder = (order) => {
    setCustomerName(order.customer_name || '');
    setCustomerEmail(order.email || '');
    setCustomerPhone(order.phone || '');
    
    // Handle both old and new address formats
    if (order.doorNo) {
      // New structured format
      setDoorNo(order.doorNo || '');
      setBuilding(order.building || '');
      setStreet(order.street || '');
      setCity(order.city || '');
      setState(order.state || '');
      setPincode(order.pincode || '');
    } else if (order.address) {
      // Old single address format - try to parse it
      setStreet(order.address);
      setCity(order.location || '');
    }
    
    setShowPreviousResults(false);
    toast({
      title: "Address Filled",
      description: "Previous order details have been filled in the form",
    });
  };

  const calculateDeliveryCharge = () => {
    if (!city) {
      setDeliveryCharge(0);
      return;
    }

    // Check if city exists in delivery locations
    const location = deliveryLocations.find(
      loc => loc.name.toLowerCase() === city.toLowerCase()
    );

    if (!location) {
      // City not found in delivery locations
      setDeliveryCharge(0);
      return;
    }

    // Check for free delivery
    if (freeDeliverySettings.enabled && cartTotal >= freeDeliverySettings.threshold) {
      setDeliveryCharge(0);
      return;
    }

    // Use the delivery charge from the location
    setDeliveryCharge(location.delivery_charge || 0);
  };

  const detectCurrentLocation = async () => {
    if (!navigator.geolocation) {
      toast({
        title: "Location Not Supported",
        description: "Your browser doesn't support geolocation",
        variant: "destructive"
      });
      return;
    }

    setDetectingLocation(true);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        
        try {
          // Use OpenStreetMap Nominatim API for reverse geocoding
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
          );
          const data = await response.json();
          
          if (data.address) {
            // Build a detailed street address from multiple components
            const streetParts = [];
            if (data.address.road) streetParts.push(data.address.road);
            if (data.address.neighbourhood) streetParts.push(data.address.neighbourhood);
            if (data.address.suburb) streetParts.push(data.address.suburb);
            if (data.address.hamlet) streetParts.push(data.address.hamlet);
            const detectedStreet = streetParts.join(', ');
            
            // Try to use neighbourhood or suburb for building
            const detectedBuilding = data.address.neighbourhood || data.address.suburb || '';
            
            const detectedPincode = data.address.postcode || '';
            const detectedState = data.address.state || '';
            
            // Smart city detection - try to match against known delivery cities
            let detectedCity = '';
            const apiCity = data.address.city || data.address.town || data.address.village || '';
            
            // First try exact match from delivery locations
            const exactMatch = deliveryLocations.find(
              loc => loc.name.toLowerCase() === apiCity.toLowerCase() && 
                     loc.state.toLowerCase() === detectedState.toLowerCase()
            );
            
            if (exactMatch) {
              detectedCity = exactMatch.name;
            } else {
              // Try partial match
              const partialMatch = deliveryLocations.find(
                loc => loc.name.toLowerCase().includes(apiCity.toLowerCase()) ||
                       apiCity.toLowerCase().includes(loc.name.toLowerCase())
              );
              
              if (partialMatch) {
                detectedCity = partialMatch.name;
              } else {
                // Use API city as fallback
                detectedCity = apiCity;
              }
            }
            
            console.log('🌍 Location detected:', {
              city: detectedCity,
              state: detectedState,
              pincode: detectedPincode,
              street: detectedStreet,
              building: detectedBuilding,
              raw: data.address
            });
            
            // Update form fields with detected values (ALWAYS overwrite)
            if (detectedStreet) setStreet(detectedStreet);
            if (detectedBuilding) setBuilding(detectedBuilding);
            if (detectedCity) setCity(detectedCity);
            if (detectedState) setState(detectedState);
            if (detectedPincode) setPincode(detectedPincode);
            
            // Show detailed notification
            toast({
              title: "📍 Location Detected",
              description: (
                <div className="space-y-1 text-sm">
                  {detectedStreet && <div>Street: {detectedStreet}</div>}
                  {detectedBuilding && <div>Building: {detectedBuilding}</div>}
                  {detectedCity && <div>City: {detectedCity}</div>}
                  {detectedState && <div>State: {detectedState}</div>}
                  {detectedPincode && <div>Pincode: {detectedPincode}</div>}
                  <div className="mt-2 text-amber-600">Please verify and adjust if needed</div>
                </div>
              ),
              duration: 8000,
            });
          }
        } catch (error) {
          console.error('Reverse geocoding error:', error);
          toast({
            title: "Location Error",
            description: "Failed to get address details",
            variant: "destructive"
          });
        } finally {
          setDetectingLocation(false);
        }
      },
      (error) => {
        setDetectingLocation(false);
        let errorMessage = "Failed to get location";
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = "Location permission denied. Please enable location access in your browser.";
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information unavailable";
            break;
          case error.TIMEOUT:
            errorMessage = "Location request timed out";
            break;
        }
        
        toast({
          title: "Location Error",
          description: errorMessage,
          variant: "destructive"
        });
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (cart.length === 0) {
      toast({
        title: "Cart is empty",
        description: "Please add items to cart before placing order",
        variant: "destructive"
      });
      return;
    }

    // Validate all required fields
    if (!customerName || !customerEmail || !customerPhone || !doorNo || !street || !city || !state || !pincode) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    // Validate city exists in delivery locations
    const cityExists = deliveryLocations.some(
      loc => loc.name.toLowerCase() === city.toLowerCase() && 
             loc.state.toLowerCase() === state.toLowerCase()
    );

    if (!cityExists) {
      toast({
        title: "City Not Available",
        description: `We don't currently deliver to ${city}. Please select a city from the dropdown list.`,
        variant: "destructive"
      });
      return;
    }

    setLoading(true);

    try {
      // Create order with pending payment status
      const orderData = {
        customer_name: customerName,
        email: customerEmail,
        phone: customerPhone,
        doorNo: doorNo,
        building: building,
        street: street,
        city: city,
        state: state,
        pincode: pincode,
        location: city,
        items: cart.map(item => ({
          product_id: item.id,
          name: item.name,
          weight: item.weight || 'N/A',
          price: item.price || 0,
          quantity: item.quantity,
          image: item.image
        })),
        subtotal: cartTotal || 0,
        delivery_charge: deliveryCharge || 0,
        total: (cartTotal || 0) + (deliveryCharge || 0),
        payment_method: paymentMethod,
        payment_sub_method: paymentSubMethod,
        payment_status: 'pending',
        order_status: 'pending'
      };

      console.log('📦 Creating order with data:', orderData);
      const orderResponse = await axios.post(`${API}/orders`, orderData);
      const { order_id, tracking_code } = orderResponse.data;

      console.log('✅ Order created:', order_id);

      // Store phone for next time
      localStorage.setItem('lastOrderPhone', customerPhone);

      // Create Razorpay order
      const razorpayOrderResponse = await axios.post(`${API}/payment/create-razorpay-order`, {
        amount: cartTotal + deliveryCharge,
        currency: 'INR',
        receipt: order_id
      });

      const { razorpay_order_id, key_id } = razorpayOrderResponse.data;

      // Initialize Razorpay
      const options = {
        key: key_id,
        amount: (cartTotal + deliveryCharge) * 100, // Amount in paise
        currency: 'INR',
        name: 'Anantha Lakshmi',
        description: 'Food Order Payment',
        order_id: razorpay_order_id,
        handler: async function (response) {
          try {
            // Verify payment
            await axios.post(`${API}/payment/verify-razorpay-payment`, {
              order_id: order_id,
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            // Clear cart and navigate to tracking
            clearCart();
            toast({
              title: "Order Placed Successfully! 🎉",
              description: `Your order has been confirmed. Tracking code: ${tracking_code}`,
            });
            navigate(`/track-order?code=${tracking_code}`);
          } catch (error) {
            console.error('Payment verification failed:', error);
            toast({
              title: "Payment Verification Failed",
              description: "Please contact support with your order ID: " + order_id,
              variant: "destructive"
            });
          }
        },
        modal: {
          ondismiss: async function() {
            // Cancel order if payment modal is dismissed
            try {
              await axios.post(`${API}/orders/${order_id}/payment-cancel`);
              toast({
                title: "Order Cancelled",
                description: "Payment was cancelled. Your order has been cancelled and will not be processed.",
                variant: "destructive"
              });
              setTimeout(() => {
                navigate('/');
              }, 2000);
            } catch (error) {
              console.error('Failed to cancel order:', error);
            }
          }
        },
        prefill: {
          name: customerName,
          email: customerEmail,
          contact: customerPhone
        },
        theme: {
          color: '#f97316' // Orange color matching app theme
        }
      };

      const rzp = new window.Razorpay(options);
      rzp.open();

    } catch (error) {
      console.error('❌ Order creation failed:', error);
      toast({
        title: "Order Failed",
        description: error.response?.data?.detail || "Failed to create order. Please try again.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEditWeight = (index) => {
    const item = cart[index];
    setEditingItemIndex(index);
    setSelectedWeight(item.weight);
  };

  const handleSaveWeight = (index) => {
    const item = cart[index];
    const newPrice = item.prices.find(p => p.weight === selectedWeight);
    if (newPrice) {
      updateCartItem(index, { selectedPrice: newPrice });
      toast({
        title: "Weight Updated",
        description: `Changed to ${newPrice.weight}`,
      });
    }
    setEditingItemIndex(null);
    setSelectedWeight('');
  };

  const handleCancelEdit = () => {
    setEditingItemIndex(null);
    setSelectedWeight('');
  };

  const handleQuantityChange = (index, newQuantity) => {
    if (newQuantity < 1) return;
    updateCartItem(index, { quantity: newQuantity });
  };

  const handleRemoveItem = (index) => {
    removeFromCart(index);
    toast({
      title: "Item Removed",
      description: "Item has been removed from cart",
    });
  };

  const handleAddRecommendation = (product) => {
    // Add the first price option by default
    if (product.prices && product.prices.length > 0) {
      const selectedPrice = product.prices[0];
      addToCart(product, selectedPrice);
      toast({
        title: "Added to Cart",
        description: `${product.name} (${selectedPrice.weight}) added to cart`,
      });
      
      // Refresh recommendations to exclude newly added item
      fetchAllProducts();
    }
  };

  const addToCart = (product, selectedPrice) => {
    const { addToCart: addToCartFn } = useCart();
    addToCartFn(product, selectedPrice);
  };

  const total = (cartTotal || 0) + (deliveryCharge || 0);

  return (
    <div className="min-w-screen bg-gradient-to-br from-orange-50 via-white to-red-50 py-4 sm:py-8 px-2 sm:px-4 overflow-x-hidden">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-4 sm:mb-8">
          <h1 className="text-2xl sm:text-4xl font-bold text-gray-800 mb-1 sm:mb-2">
            Checkout
          </h1>
          <p className="text-gray-600 text-xs sm:text-base">Complete your order</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-8">
          {/* Left Column - Form */}
          <div className="lg:col-span-2 space-y-4 sm:space-y-6">
            {/* Previous Order Search */}
            <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6">
              <h3 className="text-base sm:text-lg font-bold text-gray-800 mb-3 sm:mb-4">Quick Fill from Previous Order</h3>
              <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
                <input
                  type="text"
                  value={previousSearchQuery}
                  onChange={(e) => setPreviousSearchQuery(e.target.value)}
                  placeholder="Enter phone number or email"
                  className="flex-1 px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                />
                <button
                  type="button"
                  onClick={handlePreviousOrderSearch}
                  className="w-full sm:w-auto px-4 sm:px-6 py-2 sm:py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors font-medium text-sm sm:text-base whitespace-nowrap"
                >
                  Search
                </button>
              </div>

              {showPreviousResults && previousSearchResults.length > 0 && (
                <div className="mt-4 space-y-2">
                  <p className="text-xs sm:text-sm text-gray-600">Found {previousSearchResults.length} previous order(s). Click to use:</p>
                  {previousSearchResults.slice(0, 3).map((order) => (
                    <button
                      key={order.order_id}
                      type="button"
                      onClick={() => fillFromPreviousOrder(order)}
                      className="w-full text-left p-2 sm:p-3 border border-gray-200 rounded-lg hover:border-orange-400 hover:bg-orange-50 transition-all text-xs sm:text-sm"
                    >
                      <div className="font-medium text-gray-800">{order.customer_name}</div>
                      <div className="text-gray-600">
                        {order.doorNo && `${order.doorNo}, `}
                        {order.street && `${order.street}, `}
                        {order.city || order.location}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Customer Information */}
            <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6">
              <div className="flex items-center space-x-2 mb-3 sm:mb-4">
                <User className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
                <h3 className="text-base sm:text-lg font-bold text-gray-800">Customer Information</h3>
              </div>
              <div className="space-y-3 sm:space-y-4">
                <div>
                  <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    value={customerName}
                    onChange={(e) => setCustomerName(e.target.value)}
                    className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                    Email Address *
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-2 sm:left-3 top-2.5 sm:top-3 h-4 w-4 sm:h-5 sm:w-5 text-gray-400" />
                    <input
                      type="email"
                      value={customerEmail}
                      onChange={(e) => setCustomerEmail(e.target.value)}
                      className="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                    Phone Number *
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-2 sm:left-3 top-2.5 sm:top-3 h-4 w-4 sm:h-5 sm:w-5 text-gray-400" />
                    <input
                      type="tel"
                      value={customerPhone}
                      onChange={(e) => setCustomerPhone(e.target.value)}
                      className="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                      required
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Delivery Address */}
            <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6">
              <div className="flex items-center justify-between mb-3 sm:mb-4">
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
                  <h3 className="text-base sm:text-lg font-bold text-gray-800">Delivery Address</h3>
                </div>
                <button
                  type="button"
                  onClick={detectCurrentLocation}
                  disabled={detectingLocation}
                  className="flex items-center space-x-1 sm:space-x-2 px-2 sm:px-4 py-1.5 sm:py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-xs sm:text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Navigation className="h-3 w-3 sm:h-4 sm:w-4" />
                  <span>{detectingLocation ? 'Detecting...' : 'Detect Location'}</span>
                </button>
              </div>

              <div className="space-y-3 sm:space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                  <div>
                    <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                      Door No / Flat No *
                    </label>
                    <input
                      type="text"
                      value={doorNo}
                      onChange={(e) => setDoorNo(e.target.value)}
                      placeholder="e.g., 123, A-4"
                      className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                      Building / House Name
                    </label>
                    <input
                      type="text"
                      value={building}
                      onChange={(e) => setBuilding(e.target.value)}
                      placeholder="e.g., Sunshine Apartments"
                      className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                    Street / Area / Landmark *
                  </label>
                  <input
                    type="text"
                    value={street}
                    onChange={(e) => setStreet(e.target.value)}
                    placeholder="e.g., MG Road, Near City Mall"
                    className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                    required
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3">
                  <div>
                    <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                      State *
                    </label>
                    <select
                      value={state}
                      onChange={(e) => {
                        setState(e.target.value);
                        setCity(''); // Reset city when state changes
                      }}
                      className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                      required
                    >
                      <option value="">Select State</option>
                      <option value="Andhra Pradesh">Andhra Pradesh</option>
                      <option value="Telangana">Telangana</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                      City *
                    </label>
                    <select
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                      required
                      disabled={!state}
                    >
                      <option value="">Select City</option>
                      {state && locationsByState[state]?.map((location) => (
                        <option key={location.name} value={location.name}>
                          {location.name} (₹{location.delivery_charge})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs sm:text-sm font-medium text-gray-700 mb-1 sm:mb-2">
                    Pincode *
                  </label>
                  <input
                    type="text"
                    value={pincode}
                    onChange={(e) => {
                      const value = e.target.value.replace(/\D/g, '').slice(0, 6);
                      setPincode(value);
                    }}
                    placeholder="e.g., 500001"
                    className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm sm:text-base"
                    maxLength="6"
                    required
                  />
                </div>
              </div>

              {/* Info note */}
              <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                <p className="text-xs sm:text-sm text-amber-800">
                  <strong>Note:</strong> This checkout is only for ordering to existing delivery cities. If your city is not listed, please go to the homepage to request delivery in your area.
                </p>
              </div>
            </div>

          </div>

          {/* Right Column - Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6 sticky top-4">
              <div className="flex items-center space-x-2 mb-3 sm:mb-4">
                <ShoppingBag className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
                <h3 className="text-base sm:text-lg font-bold text-gray-800">Order Summary</h3>
              </div>

              {/* Cart Items */}
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {cart.map((item, index) => (
                  <div key={index} className="flex items-start gap-2 sm:gap-3 p-2 sm:p-3 border border-gray-200 rounded-lg">
                    <img 
                      src={item.image} 
                      alt={item.name}
                      className="w-12 h-12 sm:w-16 sm:h-16 object-cover rounded-lg flex-shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <h4 className="font-medium text-gray-800 text-xs sm:text-sm truncate">{item.name}</h4>
                      {editingItemIndex === index ? (
                        <div className="mt-1 sm:mt-2 flex items-center gap-1 sm:gap-2">
                          <select
                            value={selectedWeight}
                            onChange={(e) => setSelectedWeight(e.target.value)}
                            className="text-xs p-1 border border-gray-300 rounded"
                          >
                            {item.prices && Array.isArray(item.prices) && item.prices.map((price) => (
                              <option key={price.weight} value={price.weight}>
                                {price.weight} - ₹{price.price}
                              </option>
                            ))}
                          </select>
                          <button
                            onClick={() => handleSaveWeight(index)}
                            className="p-1 bg-green-500 text-white rounded hover:bg-green-600"
                          >
                            <Check className="h-3 w-3" />
                          </button>
                          <button
                            onClick={handleCancelEdit}
                            className="p-1 bg-gray-500 text-white rounded hover:bg-gray-600"
                          >
                            ×
                          </button>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2 mt-1">
                          <p className="text-xs sm:text-sm text-gray-600">
                            {item.weight || 'N/A'}
                          </p>
                          <button
                            onClick={() => handleEditWeight(index)}
                            className="p-1 text-blue-500 hover:text-blue-700"
                            title="Change weight"
                          >
                            <Edit className="h-3 w-3" />
                          </button>
                        </div>
                      )}
                      <div className="flex items-center gap-2 mt-1 sm:mt-2">
                        <div className="flex items-center border border-gray-300 rounded">
                          <button
                            onClick={() => handleQuantityChange(index, item.quantity - 1)}
                            className="px-1.5 sm:px-2 py-0.5 sm:py-1 text-gray-600 hover:bg-gray-100 text-xs sm:text-sm"
                          >
                            −
                          </button>
                          <span className="px-1.5 sm:px-3 py-0.5 sm:py-1 border-x border-gray-300 text-xs sm:text-sm">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => handleQuantityChange(index, item.quantity + 1)}
                            className="px-1.5 sm:px-2 py-0.5 sm:py-1 text-gray-600 hover:bg-gray-100 text-xs sm:text-sm"
                          >
                            +
                          </button>
                        </div>
                        <button
                          onClick={() => handleRemoveItem(index)}
                          className="p-1 text-red-500 hover:text-red-700"
                          title="Remove item"
                        >
                          <Trash2 className="h-3 w-3 sm:h-4 sm:w-4" />
                        </button>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <p className="font-semibold text-gray-800 text-xs sm:text-sm">
                        ₹{((item.price || 0) * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Price Breakdown */}
              <div className="mt-4 sm:mt-6 space-y-2 sm:space-y-3 pt-4 sm:pt-6 border-t border-gray-200">
                <div className="flex justify-between text-xs sm:text-sm">
                  <span className="text-gray-600">Subtotal</span>
                  <span className="font-medium text-gray-800">₹{(cartTotal || 0).toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-xs sm:text-sm">
                  <span className="text-gray-600">Delivery Charge</span>
                  <span className="font-medium text-gray-800">
                    {deliveryCharge === 0 && freeDeliverySettings.enabled && (cartTotal || 0) >= freeDeliverySettings.threshold ? (
                      <span className="text-green-600">FREE</span>
                    ) : (
                      `₹${(deliveryCharge || 0).toFixed(2)}`
                    )}
                  </span>
                </div>
                {freeDeliverySettings.enabled && (cartTotal || 0) < freeDeliverySettings.threshold && deliveryCharge > 0 && (
                  <div className="text-xs text-amber-600 bg-amber-50 p-2 rounded">
                    Add ₹{(freeDeliverySettings.threshold - (cartTotal || 0)).toFixed(2)} more for free delivery!
                  </div>
                )}
                <div className="flex justify-between text-sm sm:text-lg font-bold pt-2 sm:pt-3 border-t border-gray-200">
                  <span className="text-gray-800">Total</span>
                  <span className="text-orange-600">₹{(total || 0).toFixed(2)}</span>
                </div>
              </div>

              {/* Payment Method - Razorpay Info */}
              <div className="mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-gray-200">
                <div className="flex items-center space-x-2 mb-3">
                  <Wallet className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
                  <h4 className="text-sm sm:text-base font-bold text-gray-800">Payment Method</h4>
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-indigo-200 rounded-xl p-3 sm:p-4">
                  <div className="flex items-start space-x-2 sm:space-x-3">
                    <CreditCard className="h-5 w-5 sm:h-6 sm:w-6 text-indigo-600 flex-shrink-0 mt-1" />
                    <div>
                      <h5 className="font-semibold text-indigo-900 mb-1 sm:mb-2 text-xs sm:text-sm">Secure Payment via Razorpay</h5>
                      <p className="text-xs text-indigo-700 mb-2">
                        After placing your order, you'll be redirected to Razorpay's secure payment gateway:
                      </p>
                      <ul className="space-y-1 text-xs text-indigo-700">
                        <li className="flex items-center space-x-1">
                          <span className="text-indigo-500">•</span>
                          <span><strong>UPI:</strong> PhonePe, Google Pay, Paytm, BHIM</span>
                        </li>
                        <li className="flex items-center space-x-1">
                          <span className="text-indigo-500">•</span>
                          <span><strong>Cards:</strong> Credit & Debit Cards</span>
                        </li>
                        <li className="flex items-center space-x-1">
                          <span className="text-indigo-500">•</span>
                          <span><strong>Net Banking & Wallets</strong></span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Place Order Button */}
              <button
                onClick={handleSubmit}
                disabled={loading || cart.length === 0}
                className="w-full mt-4 sm:mt-6 py-2.5 sm:py-3 bg-gradient-to-r from-orange-500 to-red-600 text-white rounded-xl font-semibold hover:from-orange-600 hover:to-red-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed text-sm sm:text-base"
              >
                {loading ? 'Processing...' : 'Place Order & Pay'}
              </button>
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6 mt-4">
                <div className="flex items-center space-x-2 mb-3 sm:mb-4">
                  <Sparkles className="h-4 w-4 sm:h-5 sm:w-5 text-orange-500" />
                  <h3 className="text-base sm:text-lg font-bold text-gray-800">You May Also Like</h3>
                </div>
                <div className="space-y-3">
                  {recommendations.map((product) => (
                    <div 
                      key={product.id}
                      className="flex items-center gap-2 sm:gap-3 p-2 sm:p-3 border border-gray-200 rounded-lg hover:border-orange-400 transition-all group"
                    >
                      <img 
                        src={product.image} 
                        alt={product.name}
                        className="w-12 h-12 sm:w-16 sm:h-16 object-cover rounded-lg flex-shrink-0"
                      />
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium text-gray-800 text-xs sm:text-sm truncate">{product.name}</h4>
                        <p className="text-xs sm:text-sm text-orange-600 font-semibold">
                          ₹{product.prices[0]?.price}
                          <span className="text-gray-500 text-xs ml-1">
                            {product.prices[0]?.weight}
                          </span>
                        </p>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleAddRecommendation(product);
                        }}
                        className="px-2 sm:px-4 py-1.5 sm:py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors font-medium text-xs sm:text-sm whitespace-nowrap flex-shrink-0"
                      >
                        <span className="hidden sm:inline">Add to Cart</span>
                        <span className="sm:hidden">Add</span>
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Checkout;