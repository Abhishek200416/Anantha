import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Truck, MapPin, CreditCard, Mail, Phone, Home, Building2, Navigation, Plus, Minus, Edit2, X, Sparkles, Trash2 } from 'lucide-react';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || '';
const API = `${BACKEND_URL}/api`;

const Checkout = () => {
  const { cart, getCartTotal, clearCart, updateQuantity, removeFromCart, addToCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchIdentifier, setSearchIdentifier] = useState('');
  const [searching, setSearching] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    doorNo: '',
    building: '',
    street: '',
    city: '',
    state: '',
    pincode: '',
    location: '',
    paymentMethod: 'online',
    paymentSubMethod: ''
  });
  const [errors, setErrors] = useState({});
  const [deliveryCharge, setDeliveryCharge] = useState(0);
  const [deliveryLocations, setDeliveryLocations] = useState([]);
  const [detectingLocation, setDetectingLocation] = useState(false);
  const [stateCities, setStateCities] = useState({
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
  const [customCityDistance, setCustomCityDistance] = useState(null);
  const [calculatingCustomCity, setCalculatingCustomCity] = useState(false);

  useEffect(() => {
    fetchDeliveryLocations();
    fetchAllProducts();
    fetchFreeDeliverySettings();
  }, []);

  const fetchFreeDeliverySettings = async () => {
    try {
      const response = await axios.get(`${API}/settings/free-delivery`);
      setFreeDeliverySettings(response.data);
    } catch (error) {
      console.error('Failed to fetch free delivery settings:', error);
    }
  };

  const fetchAllProducts = async () => {
    try {
      const response = await axios.get(`${API}/products`);
      setAllProducts(response.data);
      // Get best sellers for recommendations
      const bestSellers = response.data.filter(p => p.isBestSeller).slice(0, 4);
      setRecommendations(bestSellers);
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
      
      const apCities = [];
      const telCities = [];
      
      locations.forEach(loc => {
        const cityName = loc.name;
        const state = loc.state || "Andhra Pradesh";
        
        if (state === "Andhra Pradesh" && !apCities.includes(cityName)) {
          apCities.push(cityName);
        } else if (state === "Telangana" && !telCities.includes(cityName)) {
          telCities.push(cityName);
        }
      });
      
      setStateCities({
        "Andhra Pradesh": [...new Set(apCities)].sort(),
        "Telangana": [...new Set(telCities)].sort()
      });
    } catch (error) {
      console.error('Failed to fetch delivery locations:', error);
    }
  };

  const handleQuantityChange = (index, delta) => {
    const item = cart[index];
    const newQuantity = (item.quantity || 1) + delta;
    
    if (newQuantity < 1) {
      if (window.confirm(`Remove ${item.name} from cart?`)) {
        removeFromCart(item.id, item.weight || item.selectedWeight);
      }
      return;
    }
    
    updateQuantity(item.id, item.weight || item.selectedWeight, newQuantity);
  };

  const handleWeightEdit = (index) => {
    const item = cart[index];
    setEditingItemIndex(index);
    setSelectedWeight(item.weight || item.selectedWeight);
  };

  const handleWeightChange = (index) => {
    const item = cart[index];
    const weight = selectedWeight;
    
    // Find the new price for selected weight
    const product = allProducts.find(p => p.id === item.id);
    if (product) {
      const priceInfo = product.prices.find(p => p.weight === weight);
      if (priceInfo) {
        // Remove old item and add with new weight
        removeFromCart(item.id, item.weight || item.selectedWeight);
        
        // Update cart with new weight (this will be handled by CartContext)
        const updatedItem = {
          ...item,
          weight: weight,
          selectedWeight: weight,
          price: priceInfo.price,
          selectedPrice: priceInfo.price
        };
        
        // Add back with new weight
        toast({
          title: "Weight Updated",
          description: `Updated to ${weight} - ₹${priceInfo.price}`
        });
      }
    }
    
    setEditingItemIndex(null);
    setSelectedWeight('');
  };

  const calculateDeliveryCharge = () => {
    const subtotal = getCartTotal();
    
    // Get city-specific threshold with state match
    const selectedCity = deliveryLocations.find(loc => 
      loc.name.toLowerCase() === formData.city.toLowerCase() && 
      loc.state === formData.state
    );
    
    // Use city-specific threshold if available, otherwise fall back to global
    const threshold = selectedCity?.free_delivery_threshold || freeDeliverySettings.threshold;
    
    // Check if free delivery is enabled and threshold is met
    if (threshold && subtotal >= threshold) {
      console.log(`🎁 FREE DELIVERY: ${formData.city} - Subtotal ₹${subtotal} >= Threshold ₹${threshold}`);
      return 0;
    }
    
    console.log(`💰 DELIVERY CHARGE: ${formData.city} - ₹${deliveryCharge} (Threshold: ₹${threshold || 'Not set'})`);
    return deliveryCharge;
  };

  const isFreeDeliveryApplicable = () => {
    const subtotal = getCartTotal();
    
    // Get city-specific threshold with state match
    const selectedCity = deliveryLocations.find(loc => 
      loc.name.toLowerCase() === formData.city.toLowerCase() && 
      loc.state === formData.state
    );
    
    const threshold = selectedCity?.free_delivery_threshold || freeDeliverySettings.threshold;
    
    return threshold && subtotal >= threshold;
  };

  const getRemainingForFreeDelivery = () => {
    const subtotal = getCartTotal();
    
    // Get city-specific threshold with state match
    const selectedCity = deliveryLocations.find(loc => 
      loc.name.toLowerCase() === formData.city.toLowerCase() && 
      loc.state === formData.state
    );
    
    const threshold = selectedCity?.free_delivery_threshold || freeDeliverySettings.threshold;
    
    return threshold ? threshold - subtotal : 0;
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Enter valid email address';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    else if (!/^\d{10}$/.test(formData.phone)) newErrors.phone = 'Enter valid 10-digit phone number';
    
    if (!formData.doorNo.trim()) newErrors.doorNo = 'Door number is required';
    if (!formData.building.trim()) newErrors.building = 'Building/House name is required';
    if (!formData.street.trim()) newErrors.street = 'Street/Area is required';
    if (!formData.state.trim()) newErrors.state = 'State is required';
    if (!formData.city.trim()) newErrors.city = 'City is required';
    // If "Others" is selected, validate custom city
    if (formData.city === 'Others' && !customCity.trim()) newErrors.city = 'Please enter your city name';
    if (!formData.pincode.trim()) newErrors.pincode = 'Pincode is required';
    else if (!/^\d{6}$/.test(formData.pincode)) newErrors.pincode = 'Enter valid 6-digit pincode';
    
    if (!formData.paymentMethod) newErrors.paymentMethod = 'Please select payment method';
    if (formData.paymentMethod && !formData.paymentSubMethod) {
      newErrors.paymentSubMethod = 'Please select payment option';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSearchUserDetails = async () => {
    if (!searchIdentifier.trim()) {
      toast({
        title: "Error",
        description: "Please enter phone number or email",
        variant: "destructive"
      });
      return;
    }

    setSearching(true);
    try {
      const response = await axios.get(`${API}/user-details/${searchIdentifier.trim()}`);
      
      if (response.data) {
        const details = response.data;
        const cityValue = details.city || formData.city;
        setFormData(prev => ({
          ...prev,
          name: details.customer_name || prev.name,
          email: details.email || prev.email,
          phone: details.phone || prev.phone,
          doorNo: details.doorNo || prev.doorNo,
          building: details.building || prev.building,
          street: details.street || prev.street,
          city: cityValue,
          state: details.state || prev.state,
          pincode: details.pincode || prev.pincode,
          location: details.location || cityValue || prev.location
        }));
        
        if (cityValue) {
          const selectedLocation = deliveryLocations.find(loc => loc.name === cityValue);
          if (selectedLocation) {
            setDeliveryCharge(selectedLocation.charge);
          } else {
            setDeliveryCharge(99);
          }
        }
        
        toast({
          title: "Details Found!",
          description: "Your saved details have been filled. Please verify and update if needed."
        });
      }
    } catch (error) {
      toast({
        title: "No Details Found",
        description: "No saved details found for this phone/email. Please enter manually.",
        variant: "destructive"
      });
    } finally {
      setSearching(false);
    }
  };

  const detectCurrentLocation = () => {
    // Check if geolocation is available
    if (!navigator.geolocation) {
      toast({
        title: "Not Supported",
        description: "Geolocation is not supported by your browser. Please enter address manually.",
        variant: "destructive"
      });
      return;
    }

    setDetectingLocation(true);
    
    // Show initial notification
    toast({
      title: "Requesting Location",
      description: "Please allow location access in your browser to detect your address..."
    });

    // Geolocation options for better cross-browser compatibility
    const geoOptions = {
      enableHighAccuracy: true,
      timeout: 15000, // 15 seconds timeout
      maximumAge: 0 // Don't use cached position
    };

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        
        console.log('📍 Location acquired:', { latitude, longitude });
        
        try {
          // Add User-Agent to prevent being blocked
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`,
            {
              headers: {
                'Accept': 'application/json',
                'User-Agent': 'AnanthaLakshmiApp/1.0'
              }
            }
          );
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          const data = await response.json();
          
          console.log('🗺️ Location API Full Response:', JSON.stringify(data, null, 2));
          
          if (data && data.address) {
            const addr = data.address;
            console.log('📍 Address fields received:', JSON.stringify(addr, null, 2));
            console.log('🔍 Individual address components:');
            console.log('   - road:', addr.road);
            console.log('   - street:', addr.street);
            console.log('   - neighbourhood:', addr.neighbourhood);
            console.log('   - suburb:', addr.suburb);
            console.log('   - locality:', addr.locality);
            console.log('   - hamlet:', addr.hamlet);
            console.log('   - quarter:', addr.quarter);
            console.log('   - residential:', addr.residential);
            console.log('   - commercial:', addr.commercial);
            console.log('   - village:', addr.village);
            console.log('   - town:', addr.town);
            console.log('   - city:', addr.city);
            console.log('   - district:', addr.district);
            console.log('   - county:', addr.county);
            
            // Enhanced address extraction with comprehensive fallbacks
            const streetOptions = [
              addr.road,
              addr.street, 
              addr.pedestrian,
              addr.footway,
              addr.path,
              addr.cycleway,
              addr.neighbourhood,
              addr.suburb,
              addr.quarter,
              addr.locality,
              addr.residential,
              addr.commercial,
              addr.industrial,
              addr.place,
              addr.hamlet,
              addr.village
            ].filter(Boolean);
            
            console.log('🛣️ ALL street options found:', streetOptions);
            
            // Improved city detection - prioritize larger administrative divisions
            let detectedCity = '';
            
            // First try to find matching city from our delivery locations
            const possibleCities = [
              addr.city,
              addr.town,
              addr.municipality,
              addr.county,
              addr.district,
              addr.city_district,
              addr.village,
              addr.subdistrict
            ].filter(Boolean);
            
            console.log('🏙️ Possible cities from API:', possibleCities);
            console.log('📍 Our delivery cities:', deliveryLocations.map(l => l.name));
            
            // Try to match with our delivery locations database
            for (const possibleCity of possibleCities) {
              const matchedLocation = deliveryLocations.find(loc => 
                loc.name.toLowerCase() === possibleCity.toLowerCase() ||
                possibleCity.toLowerCase().includes(loc.name.toLowerCase()) ||
                loc.name.toLowerCase().includes(possibleCity.toLowerCase())
              );
              
              if (matchedLocation) {
                detectedCity = matchedLocation.name;
                console.log('✅ Matched city from database:', detectedCity);
                break;
              }
            }
            
            // If no match found, use the first major city option
            if (!detectedCity) {
              detectedCity = addr.city || addr.town || addr.municipality || addr.county || addr.district || '';
              console.log('⚠️ Using fallback city:', detectedCity);
            }
            
            const buildingOptions = [
              addr.building,
              addr.house,
              addr.apartment,
              addr.amenity,
              addr.shop,
              addr.office
            ].filter(Boolean);
            
            // DETAILED STREET ADDRESS - Use multiple components for complete address
            let detectedStreet = '';
            
            // Build detailed street address from available components
            const streetComponents = [];
            
            // Add road/street name if available
            if (addr.road || addr.street) {
              streetComponents.push(addr.road || addr.street);
            }
            
            // Add neighbourhood/suburb/locality for more detail
            if (addr.neighbourhood) {
              streetComponents.push(addr.neighbourhood);
            } else if (addr.suburb) {
              streetComponents.push(addr.suburb);
            } else if (addr.locality) {
              streetComponents.push(addr.locality);
            }
            
            // Add hamlet/village_quarter for very specific location
            if (addr.hamlet) {
              streetComponents.push(addr.hamlet);
            } else if (addr.quarter) {
              streetComponents.push(addr.quarter);
            }
            
            // Join all components with comma
            detectedStreet = streetComponents.join(', ');
            
            // Fallback if no street found - use any available location detail
            if (!detectedStreet) {
              detectedStreet = addr.residential || addr.commercial || addr.industrial || 
                             addr.pedestrian || addr.place || '';
            }
            
            console.log('🛣️ Detected street components:', streetComponents);
            console.log('📍 Final street address:', detectedStreet);
            
            const detectedAddress = {
              doorNo: addr.house_number || addr.housenumber || addr.building_number || addr.unit || '',
              building: buildingOptions[0] || '',
              street: detectedStreet,
              city: detectedCity,
              state: addr.state || addr.state_district || addr.region || addr.province || '',
              pincode: addr.postcode || addr.postal_code || addr.zip || ''
            };
            
            console.log('🔍 Extracted address:', detectedAddress);
            
            // Update form data - OVERWRITE with detected data (don't preserve old values)
            setFormData(prev => {
              const newData = {
                ...prev,
                // ALWAYS use detected data if available, otherwise keep previous
                doorNo: detectedAddress.doorNo ? detectedAddress.doorNo : prev.doorNo,
                building: detectedAddress.building ? detectedAddress.building : prev.building,
                street: detectedAddress.street ? detectedAddress.street : prev.street,
                city: detectedAddress.city ? detectedAddress.city : prev.city,
                state: detectedAddress.state ? detectedAddress.state : prev.state,
                pincode: detectedAddress.pincode ? detectedAddress.pincode : prev.pincode,
                location: detectedAddress.city ? detectedAddress.city : prev.location
              };
              
              console.log('📝 Updated form data:', newData);
              console.log('🆕 New street value:', newData.street);
              console.log('🆕 New building value:', newData.building);
              console.log('🆕 New door value:', newData.doorNo);
              return newData;
            });
            
            // Auto-select delivery location and update delivery charge
            if (detectedAddress.city && detectedAddress.state) {
              console.log('🔍 Looking for delivery location:', detectedAddress.city, detectedAddress.state);
              
              const selectedLocation = deliveryLocations.find(loc => 
                loc.name.toLowerCase() === detectedAddress.city.toLowerCase() && 
                loc.state === detectedAddress.state
              );
              
              if (selectedLocation) {
                console.log('✅ Found matching location:', selectedLocation);
                setDeliveryCharge(selectedLocation.charge);
                
                // Update form with matched city and state
                setFormData(prev => ({
                  ...prev,
                  city: selectedLocation.name,
                  state: selectedLocation.state,
                  location: selectedLocation.name
                }));
              } else {
                console.log('⚠️ No exact match found, searching for partial match...');
                // Try partial match
                const partialMatch = deliveryLocations.find(loc => 
                  loc.name.toLowerCase().includes(detectedAddress.city.toLowerCase()) ||
                  detectedAddress.city.toLowerCase().includes(loc.name.toLowerCase())
                );
                
                if (partialMatch) {
                  console.log('✅ Found partial match:', partialMatch);
                  setDeliveryCharge(partialMatch.charge);
                  setFormData(prev => ({
                    ...prev,
                    city: partialMatch.name,
                    state: partialMatch.state,
                    location: partialMatch.name
                  }));
                } else {
                  console.log('⚠️ No delivery location found for:', detectedAddress.city);
                }
              }
            }
            
            // Show which fields were detected
            const detectedFieldNames = [];
            if (detectedAddress.doorNo) detectedFieldNames.push('Door No');
            if (detectedAddress.building) detectedFieldNames.push('Building');
            if (detectedAddress.street) detectedFieldNames.push('Street/Area');
            if (detectedAddress.city) detectedFieldNames.push('City');
            if (detectedAddress.state) detectedFieldNames.push('State');
            if (detectedAddress.pincode) detectedFieldNames.push('Pincode');
            
            console.log('✅ Detected fields:', detectedFieldNames);
            
            const filledFields = detectedFieldNames.length;
            
            // Show detailed feedback about what was detected
            if (filledFields > 0) {
              // Build detailed description of what was filled
              let detailsList = '';
              if (detectedAddress.street) detailsList += `\n📍 Street: ${detectedAddress.street}`;
              if (detectedAddress.building) detailsList += `\n🏢 Building: ${detectedAddress.building}`;
              if (detectedAddress.doorNo) detailsList += `\n🚪 Door No: ${detectedAddress.doorNo}`;
              if (detectedAddress.city) detailsList += `\n🏙️ City: ${detectedAddress.city}`;
              if (detectedAddress.state) detailsList += `\n🗺️ State: ${detectedAddress.state}`;
              if (detectedAddress.pincode) detailsList += `\n📮 Pincode: ${detectedAddress.pincode}`;
              
              toast({
                title: "✅ Location Detected Successfully!",
                description: `${filledFields} field(s) auto-filled:${detailsList}\n\nPlease verify the details and complete any missing fields.`,
                variant: "default",
                duration: 8000
              });
            } else {
              // Show location name even if fields couldn't be extracted
              const locationName = data.display_name || 'Unknown location';
              toast({
                title: "Location Found",
                description: `📍 ${locationName}\n\nCouldn't auto-fill address fields. Please enter manually.`,
                variant: "destructive",
                duration: 5000
              });
            }
          } else {
            throw new Error('No address data in response');
          }
        } catch (error) {
          console.error('❌ Location API error:', error);
          console.error('Error details:', error.message);
          
          toast({
            title: "Address Lookup Failed",
            description: `📍 Coordinates: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}\n\nCouldn't fetch address details. Please enter manually.\n\nError: ${error.message || 'Unknown error'}`,
            variant: "destructive",
            duration: 7000
          });
        } finally {
          setDetectingLocation(false);
        }
      },
      (error) => {
        console.error('❌ Geolocation error:', error);
        setDetectingLocation(false);
        
        // Provide specific error messages based on error code
        let errorMessage = "Unable to detect location. ";
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage += "Location access was denied. Please allow location access in your browser settings and try again.";
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage += "Location information is unavailable. Please check your device settings and try again.";
            break;
          case error.TIMEOUT:
            errorMessage += "Location request timed out. Please try again or enter address manually.";
            break;
          default:
            errorMessage += "An unknown error occurred. Please enter address manually.";
        }
        
        toast({
          title: "Location Error",
          description: errorMessage,
          variant: "destructive"
        });
      },
      geoOptions
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast({
        title: "Error",
        description: "Please fill all required fields correctly.",
        variant: "destructive"
      });
      return;
    }

    if (!cart || cart.length === 0) {
      toast({
        title: "Error",
        description: "Your cart is empty.",
        variant: "destructive"
      });
      return;
    }

    // Check if all products are available for delivery to the selected city
    const unavailableProducts = [];
    for (const item of cart) {
      const available_cities = item.available_cities;
      if (available_cities && Array.isArray(available_cities) && available_cities.length > 0) {
        // If product has city restrictions, check if the selected city is in the list
        if (!available_cities.includes(formData.city)) {
          unavailableProducts.push(item.name);
        }
      }
    }

    if (unavailableProducts.length > 0) {
      toast({
        title: "Delivery Not Available",
        description: `The following products are not available for delivery to ${formData.city}: ${unavailableProducts.join(', ')}. Please remove them from cart or choose a different city.`,
        variant: "destructive"
      });
      return;
    }

    const fullAddress = `${formData.doorNo}, ${formData.building}, ${formData.street}, ${formData.city}, ${formData.state} - ${formData.pincode}`;
    const finalDeliveryCharge = calculateDeliveryCharge();

    const orderData = {
      user_id: user?.id || 'guest',
      customer_name: formData.name,
      email: formData.email,
      phone: formData.phone,
      address: fullAddress,
      doorNo: formData.doorNo,
      building: formData.building,
      street: formData.street,
      city: formData.city,
      state: formData.state,
      pincode: formData.pincode,
      location: formData.location || formData.city,
      items: cart.map(item => ({
        product_id: String(item.id || ''),
        name: item.name || '',
        image: item.image || '',
        weight: item.weight || item.selectedWeight || (item.prices && item.prices.length > 0 ? item.prices[0].weight : ''),
        price: parseFloat(item.price || item.selectedPrice || (item.prices && item.prices.length > 0 ? item.prices[0].price : 0)),
        quantity: parseInt(item.quantity) || 1,
        description: item.description || ''
      })),
      subtotal: getCartTotal(),
      delivery_charge: finalDeliveryCharge,
      total: getCartTotal() + finalDeliveryCharge,
      payment_method: formData.paymentMethod,
      payment_sub_method: formData.paymentSubMethod,
      is_custom_location: formData.city === 'Others',
      custom_city: formData.city === 'Others' ? customCity : null,
      custom_state: formData.city === 'Others' ? (customCityState || formData.state) : null,
      distance_from_guntur: formData.city === 'Others' ? customCityDistance : null
    };

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API}/orders`, orderData, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const result = response.data;
      clearCart();

      toast({
        title: "Order Placed Successfully!",
        description: `Order ID: ${result.order_id}. Check your email for tracking code.`,
      });

      navigate('/order-success', { state: { orderData: result } });
    } catch (error) {
      console.error('Order error:', error);
      const errorMsg = error.response?.data?.detail || 
                       (error.response?.data?.message) ||
                       "Failed to place order. Please try again.";
      toast({
        title: "Error",
        description: Array.isArray(errorMsg) ? errorMsg[0]?.msg || errorMsg[0] : errorMsg,
        variant: "destructive"
      });
    }
  };

  const calculateCustomCityDelivery = async (cityName, stateName) => {
    setCalculatingCustomCity(true);
    try {
      const response = await axios.post(`${API}/calculate-custom-city-delivery`, {
        city_name: cityName,
        state_name: stateName
      });
      
      setCustomCityDeliveryCharge(response.data.delivery_charge);
      setCustomCityDistance(response.data.distance_from_guntur_km);
      setDeliveryCharge(response.data.delivery_charge);
      
      toast({
        title: "Delivery Charge Calculated",
        description: response.data.distance_from_guntur_km 
          ? `₹${response.data.delivery_charge} for ${cityName} (${response.data.distance_from_guntur_km}km from Guntur)`
          : `₹${response.data.delivery_charge} for ${cityName}`
      });
    } catch (error) {
      console.error('Failed to calculate custom city delivery:', error);
      setCustomCityDeliveryCharge(199);
      setDeliveryCharge(199);
      toast({
        title: "Using Default Charge",
        description: `₹199 delivery charge for ${cityName}`,
        variant: "default"
      });
    } finally {
      setCalculatingCustomCity(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'state') {
      setFormData(prev => ({ ...prev, [name]: value, city: '' }));
      setDeliveryCharge(0);
      setShowCustomCityInput(false);
      setCustomCity('');
      if (errors.city) {
        setErrors(prev => ({ ...prev, city: '' }));
      }
    } else if (name === 'city') {
      // Check if "Others" is selected
      if (value === 'Others') {
        setShowCustomCityInput(true);
        setCustomCityState(formData.state);
        setFormData(prev => ({ ...prev, [name]: value, location: '' }));
        // Don't set delivery charge here - it will be calculated by admin
        setDeliveryCharge(0);
        setCustomCityDeliveryCharge(0);
        setCustomCityDistance(null);
      } else {
        setShowCustomCityInput(false);
        setCustomCity('');
        setFormData(prev => ({ ...prev, [name]: value, location: value }));
        
        // Find location with matching city name and state
        const currentState = formData.state;
        const selectedLocation = deliveryLocations.find(loc => 
          loc.name === value && loc.state === currentState
        );
        
        console.log('🏙️ City selected:', value, 'State:', currentState);
        console.log('📍 All locations:', deliveryLocations.length);
        console.log('📍 Found location:', selectedLocation);
        
        if (selectedLocation && selectedLocation.charge !== undefined) {
          const charge = Number(selectedLocation.charge);
          console.log('💰 Setting delivery charge:', charge);
          setDeliveryCharge(charge);
        } else {
          console.log('⚠️ Location not found or no charge, using default: 99');
          setDeliveryCharge(99);
        }
      }
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleCustomCitySubmit = () => {
    if (!customCity.trim()) {
      toast({
        title: "Error",
        description: "Please enter your city name",
        variant: "destructive"
      });
      return;
    }
    
    // Just set the location - no need to calculate delivery charge
    // Admin will approve and set delivery charge later
    setFormData(prev => ({ ...prev, location: customCity }));
    
    toast({
      title: "City Added",
      description: `${customCity} has been added. Delivery charges will be updated within 5-10 minutes.`,
    });
  };

  const scrollToProduct = (productId) => {
    navigate('/');
    setTimeout(() => {
      const element = document.getElementById(`product-${productId}`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.classList.add('ring-4', 'ring-orange-400', 'ring-offset-2');
        setTimeout(() => {
          element.classList.remove('ring-4', 'ring-orange-400', 'ring-offset-2');
        }, 2000);
      }
    }, 300);
  };

  const handleAddRecommendation = (product) => {
    // Add the first price option by default
    if (product.prices && product.prices.length > 0) {
      const selectedPrice = product.prices[0];
      addToCart(product, selectedPrice);
      toast({
        title: "Added to Cart!",
        description: `${product.name} (${selectedPrice.weight}) added to cart`
      });
    }
  };

  const finalDeliveryCharge = calculateDeliveryCharge();
  const totalAmount = getCartTotal() + finalDeliveryCharge;

  if (!cart || cart.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-red-50 flex items-center justify-center px-4">
        <div className="text-center">
          <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4">Your cart is empty</h2>
          <button
            onClick={() => navigate('/')}
            className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-lg hover:from-orange-600 hover:to-red-600 text-sm sm:text-base"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-red-50 py-4 sm:py-8 overflow-x-hidden">
      <div className="container mx-auto px-3 sm:px-4 max-w-7xl overflow-x-hidden">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-center mb-6 sm:mb-8 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
          Checkout
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-8">
          {/* Checkout Form - Keeping the same as before */}
          <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6">
            <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">Delivery Details</h2>
            
            {/* Previous Details Search */}
            <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Have you ordered before?</h3>
              <div className="flex flex-col sm:flex-row gap-2">
                <input
                  type="text"
                  value={searchIdentifier}
                  onChange={(e) => setSearchIdentifier(e.target.value)}
                  placeholder="Enter phone number or email"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={handleSearchUserDetails}
                  disabled={searching}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 w-full sm:w-auto"
                >
                  {searching ? 'Searching...' : 'Search'}
                </button>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Name */}
              <div>
                <label className="block text-gray-700 font-medium mb-2">Full Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                    errors.name ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="Enter your full name"
                />
                {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
              </div>

              {/* Email */}
              <div>
                <label className="block text-gray-700 font-medium mb-2 flex items-center space-x-2">
                  <Mail className="h-4 w-4" />
                  <span>Email Address *</span>
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                    errors.email ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="your.email@example.com"
                />
                {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
              </div>

              {/* Phone */}
              <div>
                <label className="block text-gray-700 font-medium mb-2 flex items-center space-x-2">
                  <Phone className="h-4 w-4" />
                  <span>Phone Number *</span>
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  maxLength="10"
                  className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                    errors.phone ? 'border-red-500' : 'border-gray-300'
                  }`}
                  placeholder="10-digit mobile number"
                />
                {errors.phone && <p className="text-red-500 text-sm mt-1">{errors.phone}</p>}
              </div>

              {/* Address Section */}
              <div className="pt-4 border-t">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                  <h3 className="text-lg font-bold text-gray-800 flex items-center space-x-2">
                    <Home className="h-5 w-5" />
                    <span>Delivery Address</span>
                  </h3>
                  <button
                    type="button"
                    onClick={detectCurrentLocation}
                    disabled={detectingLocation}
                    className="flex items-center justify-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all disabled:opacity-50 text-sm w-full sm:w-auto"
                  >
                    <Navigation className="h-4 w-4" />
                    <span>{detectingLocation ? 'Detecting...' : 'Detect Location'}</span>
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Door No */}
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">Door No *</label>
                    <input
                      type="text"
                      name="doorNo"
                      value={formData.doorNo}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                        errors.doorNo ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="12-34"
                    />
                    {errors.doorNo && <p className="text-red-500 text-sm mt-1">{errors.doorNo}</p>}
                  </div>

                  {/* Building */}
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">Building/House *</label>
                    <input
                      type="text"
                      name="building"
                      value={formData.building}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                        errors.building ? 'border-red-500' : 'border-gray-300'
                      }`}
                      placeholder="Apartment/House name"
                    />
                    {errors.building && <p className="text-red-500 text-sm mt-1">{errors.building}</p>}
                  </div>
                </div>

                {/* Street */}
                <div className="mt-4">
                  <label className="block text-gray-700 font-medium mb-2">Street/Area *</label>
                  <input
                    type="text"
                    name="street"
                    value={formData.street}
                    onChange={handleChange}
                    className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                      errors.street ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="Street name or area"
                  />
                  {errors.street && <p className="text-red-500 text-sm mt-1">{errors.street}</p>}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
                  {/* State */}
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">State *</label>
                    <select
                      name="state"
                      value={formData.state}
                      onChange={handleChange}
                      className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                        errors.state ? 'border-red-500' : 'border-gray-300'
                      }`}
                    >
                      <option value="">Select State</option>
                      <option value="Andhra Pradesh">Andhra Pradesh</option>
                      <option value="Telangana">Telangana</option>
                    </select>
                    {errors.state && <p className="text-red-500 text-sm mt-1">{errors.state}</p>}
                  </div>

                  {/* City */}
                  <div>
                    <label className="block text-gray-700 font-medium mb-2">City *</label>
                    <select
                      name="city"
                      value={formData.city}
                      onChange={handleChange}
                      disabled={!formData.state}
                      className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                        errors.city ? 'border-red-500' : 'border-gray-300'
                      } ${!formData.state ? 'bg-gray-100 cursor-not-allowed' : ''}`}
                    >
                      <option value="">
                        {formData.state ? 'Select City' : 'Select State First'}
                      </option>
                      {formData.state && stateCities[formData.state] && 
                        stateCities[formData.state].map((city, index) => {
                          const locationData = deliveryLocations.find(loc => loc.name === city && loc.state === formData.state);
                          const charge = locationData && locationData.charge !== undefined ? locationData.charge : 99;
                          return (
                            <option key={`${formData.state}-${city}-${index}`} value={city}>
                              {city} - ₹{charge}
                            </option>
                          );
                        })
                      }
                      {formData.state && (
                        <option value="Others" className="font-semibold text-orange-600">
                          Others (Enter Custom City)
                        </option>
                      )}
                    </select>
                    {errors.city && <p className="text-red-500 text-sm mt-1">{errors.city}</p>}
                    
                    {/* Custom City Input */}
                    {showCustomCityInput && (
                      <div className="mt-4 p-5 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-300 rounded-xl shadow-sm">
                        <div className="space-y-4">
                          <div>
                            <p className="text-base font-bold text-blue-900 mb-2 flex items-start gap-2">
                              <span className="text-xl">📍</span>
                              <span>Your City is Not in Our List</span>
                            </p>
                            <p className="text-sm text-gray-700 leading-relaxed">
                              Please enter your city name below. We will calculate the delivery charges for your location and update it within <span className="font-semibold text-blue-700">5-10 minutes</span>.
                            </p>
                          </div>
                          
                          <div className="bg-white p-4 rounded-lg border border-blue-200">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">
                              Enter Your City Name <span className="text-red-500">*</span>
                            </label>
                            <input
                              type="text"
                              value={customCity}
                              onChange={(e) => setCustomCity(e.target.value)}
                              placeholder="e.g., Nellore, Kurnool, Kadapa..."
                              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                            />
                          </div>

                          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg">
                            <p className="text-sm text-yellow-800 font-medium flex items-start gap-2">
                              <span>📧</span>
                              <span>
                                <span className="font-bold">Track Your Order:</span> Use your <span className="font-semibold underline">mobile number</span> or <span className="font-semibold underline">email ID</span> to check your order status and see the updated delivery charges.
                              </span>
                            </p>
                          </div>

                          <div className="flex items-center gap-2 text-sm text-gray-600 bg-white p-3 rounded-lg border border-gray-200">
                            <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                            <span>You can proceed with checkout. Delivery charges will be calculated and added to your order shortly.</span>
                          </div>
                        </div>
                      </div>
                    )}
                    {formData.city && formData.state && formData.city !== 'Others' && (
                      <div className="mt-2 space-y-1">
                        {(() => {
                          const loc = deliveryLocations.find(l => l.name === formData.city && l.state === formData.state);
                          const currentCharge = loc && loc.charge !== undefined ? loc.charge : deliveryCharge || 99;
                          const threshold = loc?.free_delivery_threshold;
                          const cartTotal = getCartTotal();
                          const qualifiesForFree = threshold && cartTotal >= threshold;
                          
                          return (
                            <>
                              <p className={`text-sm ${qualifiesForFree ? 'text-green-600 font-semibold' : 'text-green-600'}`}>
                                {qualifiesForFree ? (
                                  <>✓ Delivery Charge: <span className="line-through">₹{currentCharge}</span> <span className="font-bold">FREE! 🎉</span></>
                                ) : (
                                  <>✓ Delivery Charge: ₹{currentCharge}</>
                                )}
                              </p>
                              {threshold && (
                                <p className="text-sm text-blue-600">
                                  {qualifiesForFree ? (
                                    <>🎁 You qualify for FREE delivery in {formData.city}!</>
                                  ) : (
                                    <>🎁 Free delivery on orders above ₹{threshold} for {formData.city}</>
                                  )}
                                </p>
                              )}
                            </>
                          );
                        })()}
                      </div>
                    )}
                    {formData.city === 'Others' && customCity && (
                      <div className="mt-2">
                        <p className="text-sm text-blue-700 font-medium bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                          📍 Custom Location: <span className="font-semibold">{customCity}</span>
                          <br />
                          <span className="text-xs text-gray-600">💰 Delivery charges will be calculated and updated within 5-10 minutes</span>
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Pincode */}
                <div className="mt-4">
                  <label className="block text-gray-700 font-medium mb-2">Pincode *</label>
                  <input
                    type="text"
                    name="pincode"
                    value={formData.pincode}
                    onChange={handleChange}
                    maxLength="6"
                    className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 ${
                      errors.pincode ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder="6-digit pincode"
                  />
                  {errors.pincode && <p className="text-red-500 text-sm mt-1">{errors.pincode}</p>}
                </div>
              </div>

              {/* Payment Method */}
              <div className="pt-4 border-t">
                <h3 className="text-base sm:text-lg font-bold text-gray-800 mb-3 sm:mb-4">Payment Method</h3>
                
                {/* Online Payment */}
                <div className="mb-4">
                  <label className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="online"
                      checked={formData.paymentMethod === 'online'}
                      onChange={handleChange}
                      className="w-4 h-4 text-orange-600"
                    />
                    <div className="flex items-center space-x-2">
                      <CreditCard className="h-5 w-5 text-blue-600" />
                      <span className="font-semibold">Online Payment (UPI)</span>
                    </div>
                  </label>
                  {formData.paymentMethod === 'online' && (
                    <div className="mt-3 ml-0 sm:ml-8 p-4 bg-white border border-gray-200 rounded-lg">
                      <p className="text-sm text-gray-600 mb-3 font-medium">Select UPI Payment Option:</p>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {['Paytm', 'PhonePe', 'Google Pay', 'BHIM UPI'].map((app) => (
                          <label 
                            key={app}
                            className={`flex items-center space-x-2 p-3 border rounded-lg cursor-pointer transition-all ${
                              formData.paymentSubMethod === app 
                                ? 'border-orange-500 bg-orange-50' 
                                : 'border-gray-200 hover:border-orange-300'
                            }`}
                          >
                            <input
                              type="radio"
                              name="paymentSubMethod"
                              value={app}
                              checked={formData.paymentSubMethod === app}
                              onChange={handleChange}
                              className="w-4 h-4 text-orange-600"
                            />
                            <span className="text-sm font-medium">{app}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Card Payment */}
                <div>
                  <label className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="card"
                      checked={formData.paymentMethod === 'card'}
                      onChange={handleChange}
                      className="w-4 h-4 text-orange-600"
                    />
                    <div className="flex items-center space-x-2">
                      <CreditCard className="h-5 w-5 text-purple-600" />
                      <span className="font-semibold">Card Payment</span>
                    </div>
                  </label>
                  {formData.paymentMethod === 'card' && (
                    <div className="mt-3 ml-0 sm:ml-8 p-4 bg-white border border-gray-200 rounded-lg">
                      <p className="text-sm text-gray-600 mb-3 font-medium">Select Card Type:</p>
                      <div className="flex flex-col sm:flex-row gap-3 sm:space-x-4">
                        {['Debit Card', 'Credit Card'].map((cardType) => (
                          <label 
                            key={cardType}
                            className={`flex items-center space-x-2 p-3 border rounded-lg cursor-pointer transition-all ${
                              formData.paymentSubMethod === cardType 
                                ? 'border-orange-500 bg-orange-50' 
                                : 'border-gray-200 hover:border-orange-300'
                            }`}
                          >
                            <input
                              type="radio"
                              name="paymentSubMethod"
                              value={cardType}
                              checked={formData.paymentSubMethod === cardType}
                              onChange={handleChange}
                              className="w-4 h-4 text-orange-600"
                            />
                            <span className="text-sm font-medium">{cardType}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-3 sm:py-4 rounded-xl font-semibold hover:from-green-700 hover:to-green-800 transition-all transform hover:scale-105 shadow-lg flex items-center justify-center space-x-2 text-sm sm:text-base"
              >
                <Truck className="h-4 w-4 sm:h-5 sm:w-5" />
                <span>Place Order</span>
              </button>
            </form>
          </div>

          {/* Order Summary with Edit Features */}
          <div>
            <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6 mb-4 sm:mb-6">
              <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">Order Summary</h2>
              
              {/* Cart Items with Edit Options */}
              <div className="space-y-3 sm:space-y-4 mb-4 sm:mb-6">
                {cart.map((item, index) => (
                  <div key={index} className="border-b pb-3 sm:pb-4">
                    <div className="flex items-start gap-2 sm:gap-3">
                      <img src={item.image} alt={item.name} className="w-14 h-14 sm:w-16 sm:h-16 md:w-20 md:h-20 object-cover rounded-lg flex-shrink-0" />
                      <div className="flex-1 min-w-0 overflow-hidden">
                        <h3 className="font-semibold text-gray-800 text-xs sm:text-sm md:text-base truncate">{item.name}</h3>
                        <div className="flex items-center space-x-2 mt-1">
                          <p className="text-xs text-gray-600">{item.weight || item.selectedWeight}</p>
                          {allProducts.find(p => p.id === item.id)?.prices?.length > 1 && (
                            <button
                              onClick={() => handleWeightEdit(index)}
                              className="text-blue-600 hover:text-blue-700"
                              title="Change weight"
                            >
                              <Edit2 className="h-3 w-3" />
                            </button>
                          )}
                        </div>
                        
                        {/* Weight Edit Modal */}
                        {editingItemIndex === index && (
                          <div className="mt-2 p-3 bg-blue-50 rounded-lg border border-blue-200">
                            <p className="text-xs font-semibold text-gray-700 mb-2">Select Weight:</p>
                            <select
                              value={selectedWeight}
                              onChange={(e) => setSelectedWeight(e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
                            >
                              {allProducts.find(p => p.id === item.id)?.prices?.map((priceInfo, idx) => (
                                <option key={idx} value={priceInfo.weight}>
                                  {priceInfo.weight} - ₹{priceInfo.price}
                                </option>
                              ))}
                            </select>
                            <div className="flex space-x-2 mt-2">
                              <button
                                onClick={() => handleWeightChange(index)}
                                className="flex-1 px-3 py-1 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700"
                              >
                                Update
                              </button>
                              <button
                                onClick={() => setEditingItemIndex(null)}
                                className="flex-1 px-3 py-1 bg-gray-300 text-gray-700 rounded-lg text-sm hover:bg-gray-400"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        )}
                        
                        {/* Quantity Controls & Delete Button */}
                        <div className="flex items-center justify-between mt-2 gap-2">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleQuantityChange(index, -1)}
                              className="w-6 h-6 sm:w-7 sm:h-7 flex items-center justify-center bg-gray-200 rounded-full hover:bg-gray-300 transition-colors flex-shrink-0"
                            >
                              <Minus className="h-3 w-3" />
                            </button>
                            <span className="font-semibold text-gray-700 text-sm min-w-[20px] text-center">{item.quantity}</span>
                            <button
                              onClick={() => handleQuantityChange(index, 1)}
                              className="w-6 h-6 sm:w-7 sm:h-7 flex items-center justify-center bg-orange-500 text-white rounded-full hover:bg-orange-600 transition-colors flex-shrink-0"
                            >
                              <Plus className="h-3 w-3" />
                            </button>
                          </div>
                          <button
                            onClick={() => {
                              if (window.confirm(`Remove ${item.name} from cart?`)) {
                                removeFromCart(item.id, item.weight || item.selectedWeight);
                                toast({
                                  title: "Item Removed",
                                  description: `${item.name} removed from cart`
                                });
                              }
                            }}
                            className="flex items-center space-x-1 px-2 py-1 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors text-xs flex-shrink-0"
                            title="Remove item"
                          >
                            <Trash2 className="h-3 w-3" />
                            <span className="hidden sm:inline">Delete</span>
                          </button>
                        </div>
                      </div>
                      <p className="font-bold text-orange-600 text-xs sm:text-sm flex-shrink-0 whitespace-nowrap">₹{(item.price || item.selectedPrice || 0) * (item.quantity || 1)}</p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Free Delivery Progress or Success */}
              {formData.city && (() => {
                const selectedCity = deliveryLocations.find(loc => 
                  loc.name.toLowerCase() === formData.city.toLowerCase() && 
                  loc.state === formData.state
                );
                const threshold = selectedCity?.free_delivery_threshold;
                
                if (!threshold) return null;
                
                if (isFreeDeliveryApplicable()) {
                  return (
                    <div className="mb-6 p-4 bg-gradient-to-r from-green-100 to-emerald-100 rounded-lg border-2 border-green-400">
                      <div className="flex items-center space-x-2">
                        <Truck className="h-6 w-6 text-green-700" />
                        <div>
                          <p className="text-base font-bold text-green-800">
                            🎉 Congratulations! You qualify for FREE delivery!
                          </p>
                          <p className="text-sm text-green-700 mt-1">
                            Your order of ₹{getCartTotal()} exceeds the ₹{threshold} threshold for {formData.city}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                }
                
                const remaining = getRemainingForFreeDelivery();
                if (remaining > 0) {
                  return (
                    <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
                      <div className="flex items-center space-x-2 mb-2">
                        <Truck className="h-5 w-5 text-green-600" />
                        <p className="text-sm font-semibold text-green-800">
                          Add ₹{remaining.toFixed(2)} more for FREE delivery in {formData.city}!
                        </p>
                      </div>
                      <div className="w-full bg-green-200 rounded-full h-2.5">
                        <div 
                          className="bg-green-600 h-2.5 rounded-full transition-all duration-300 ease-in-out"
                          style={{ width: `${Math.min((getCartTotal() / threshold) * 100, 100)}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-600 mt-2">
                        ₹{getCartTotal()} / ₹{threshold}
                      </p>
                    </div>
                  );
                }
                
                return null;
              })()}

              {/* Price Breakdown */}
              <div className="space-y-3 border-t pt-4">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal:</span>
                  <span className="font-semibold">₹{getCartTotal()}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Delivery Charge:</span>
                  <span className={`font-semibold ${isFreeDeliveryApplicable() ? 'text-green-600' : ''}`}>
                    {isFreeDeliveryApplicable() ? (
                      <span className="flex items-center space-x-1">
                        <span className="line-through text-gray-400">₹{deliveryCharge}</span>
                        <span className="text-green-600 font-bold">FREE</span>
                      </span>
                    ) : (
                      `₹${finalDeliveryCharge}`
                    )}
                  </span>
                </div>
                <div className="flex justify-between text-xl font-bold text-gray-800 border-t pt-3">
                  <span>Total:</span>
                  <span className="text-orange-600">₹{totalAmount}</span>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="bg-white rounded-2xl shadow-lg p-4 sm:p-6">
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
                        className="w-12 h-12 sm:w-16 sm:h-16 object-cover rounded-lg cursor-pointer flex-shrink-0" 
                        onClick={() => scrollToProduct(product.id)}
                      />
                      <div className="flex-1 min-w-0 overflow-hidden">
                        <h4 
                          className="font-semibold text-gray-800 text-xs sm:text-sm group-hover:text-orange-600 cursor-pointer truncate"
                          onClick={() => scrollToProduct(product.id)}
                        >
                          {product.name}
                        </h4>
                        <p className="text-xs text-gray-600 truncate">{product.category}</p>
                        <p className="text-xs sm:text-sm font-bold text-orange-600 mt-1">
                          From ₹{product.prices[0]?.price}
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
};

export default Checkout;
