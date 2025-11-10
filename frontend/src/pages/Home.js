import React, { useState, useEffect } from 'react';
import CategoryFilter from '../components/CategoryFilter';
import ProductCard from '../components/ProductCard';
import ProductDetailModal from '../components/ProductDetailModal';
import { useAdmin } from '../contexts/AdminContext';
import { Sparkles, X, ArrowRight, MapPin } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedCity, setSelectedCity] = useState('');
  const [showFestivalPopup, setShowFestivalPopup] = useState(false);
  const [showBestSellerPopup, setShowBestSellerPopup] = useState(false);
  const [selectedPopupProduct, setSelectedPopupProduct] = useState(null);
  const [allProducts, setAllProducts] = useState([]);
  const { products: contextProducts, festivalProduct, deliveryLocations } = useAdmin();

  // Fetch products based on selected city
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const url = selectedCity 
          ? `${API}/products?city=${encodeURIComponent(selectedCity)}`
          : `${API}/products`;
        const response = await axios.get(url);
        setAllProducts(response.data || []);
      } catch (error) {
        console.error('Error fetching products:', error);
        setAllProducts(contextProducts);
      }
    };
    fetchProducts();
  }, [selectedCity, contextProducts]);

  // Use allProducts instead of contextProducts
  const products = allProducts.length > 0 ? allProducts : contextProducts;

  // Show festival popup on load if set
  useEffect(() => {
    if (festivalProduct && !sessionStorage.getItem('festivalPopupShown')) {
      // Add a small delay to ensure products are loaded
      setTimeout(() => {
        setShowFestivalPopup(true);
        sessionStorage.setItem('festivalPopupShown', 'true');
      }, 500);
    }
  }, [festivalProduct]);

  // Show best seller popup
  useEffect(() => {
    const timer = setTimeout(() => {
      if (!sessionStorage.getItem('bestSellerPopupShown')) {
        setShowBestSellerPopup(true);
        sessionStorage.setItem('bestSellerPopupShown', 'true');
      }
    }, 5000);
    return () => clearTimeout(timer);
  }, []);

  const filteredProducts = selectedCategory === 'all'
    ? products
    : products.filter(p => p.category === selectedCategory);

  const bestSellers = products.filter(p => p.isBestSeller).slice(0, 3);

  const handleViewProduct = (product) => {
    setShowFestivalPopup(false);
    setShowBestSellerPopup(false);
    // Open product detail modal instead of scrolling
    setSelectedPopupProduct(product);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-red-50">
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-6">
            Welcome to Anantha Lakshmi
          </h1>
          <p className="text-xl text-gray-600 mb-8">Discover premium quality products delivered to your doorstep</p>
        </div>
      </section>

      {/* Products Section */}
      <section id="products" className="container mx-auto px-4 pb-20 pt-8">
        <div className="mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-2">Our Products</h2>
          <p className="text-gray-600 text-sm md:text-base">Browse our delicious collection of traditional foods</p>
        </div>
        
        <CategoryFilter selectedCategory={selectedCategory} onSelectCategory={setSelectedCategory} />
        
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-6 mt-6 md:mt-8">
          {filteredProducts.map((product) => (
            <div key={product.id} id={`product-${product.id}`}>
              <ProductCard product={product} />
            </div>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-base md:text-lg">No products found in this category.</p>
          </div>
        )}
      </section>

      {/* Festival Product Popup */}
      {showFestivalPopup && festivalProduct && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in">
          <div className="bg-white rounded-2xl md:rounded-3xl max-w-md w-full p-4 md:p-6 shadow-2xl relative transform animate-in zoom-in max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowFestivalPopup(false)}
              className="absolute top-3 right-3 md:top-4 md:right-4 text-gray-500 hover:text-gray-700 z-10 bg-white rounded-full p-1"
            >
              <X className="h-5 w-5 md:h-6 md:w-6" />
            </button>
            
            <div className="text-center">
              <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1.5 md:px-4 md:py-2 rounded-full inline-flex items-center space-x-2 mb-3 md:mb-4 animate-bounce text-sm md:text-base">
                <Sparkles className="h-4 w-4 md:h-5 md:w-5" />
                <span className="font-bold">Festival Special!</span>
              </div>
              
              <img 
                src={festivalProduct.image} 
                alt={festivalProduct.name}
                className="w-full h-48 md:h-64 object-cover rounded-xl md:rounded-2xl mb-3 md:mb-4 shadow-lg"
              />
              
              <h2 className="text-xl md:text-2xl font-bold text-gray-800 mb-2">{festivalProduct.name}</h2>
              <p className="text-gray-600 mb-3 md:mb-4 text-sm md:text-base">{festivalProduct.description}</p>
              <p className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-4 md:mb-6">
                ₹{festivalProduct.prices[0]?.price}
              </p>
              
              <button
                onClick={() => handleViewProduct(festivalProduct)}
                className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-2.5 md:py-3 rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all flex items-center justify-center space-x-2 text-sm md:text-base"
              >
                <span>View Product</span>
                <ArrowRight className="h-4 w-4 md:h-5 md:w-5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Best Seller Popup */}
      {showBestSellerPopup && bestSellers.length > 0 && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in">
          <div className="bg-white rounded-2xl md:rounded-3xl max-w-2xl w-full p-4 md:p-6 shadow-2xl relative transform animate-in zoom-in max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowBestSellerPopup(false)}
              className="absolute top-3 right-3 md:top-4 md:right-4 text-gray-500 hover:text-gray-700 z-10 bg-white rounded-full p-1"
            >
              <X className="h-5 w-5 md:h-6 md:w-6" />
            </button>
            
            <div className="text-center mb-4 md:mb-6">
              <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-3 py-1.5 md:px-4 md:py-2 rounded-full inline-flex items-center space-x-2 mb-3 md:mb-4">
                <Sparkles className="h-4 w-4 md:h-5 md:w-5" />
                <span className="font-bold text-sm md:text-base">Our Best Sellers!</span>
              </div>
              <p className="text-gray-600 text-sm md:text-base">Check out our most popular products</p>
            </div>
            
            <div className="grid grid-cols-3 gap-2 md:gap-4 mb-4 md:mb-6">
              {bestSellers.map((product) => (
                <div key={product.id} className="text-center cursor-pointer hover:scale-105 transition-transform" onClick={() => handleViewProduct(product)}>
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="w-full h-20 md:h-32 object-cover rounded-lg mb-1 md:mb-2 shadow-md"
                  />
                  <h4 className="font-semibold text-xs md:text-sm text-gray-800 line-clamp-2">{product.name}</h4>
                  <p className="text-orange-600 font-bold text-xs md:text-base">₹{product.prices[0].price}</p>
                </div>
              ))}
            </div>
            
            <button
              onClick={() => setShowBestSellerPopup(false)}
              className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-2.5 md:py-3 rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all text-sm md:text-base"
            >
              Start Shopping
            </button>
          </div>
        </div>
      )}

      {/* Product Detail Modal from Popup */}
      {selectedPopupProduct && (
        <ProductDetailModal 
          product={selectedPopupProduct} 
          isOpen={true}
          onClose={() => setSelectedPopupProduct(null)}
        />
      )}
    </div>
  );
};

export default Home;
