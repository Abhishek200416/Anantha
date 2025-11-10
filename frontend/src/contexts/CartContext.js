import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  // Load cart from localStorage on mount
  useEffect(() => {
    const savedCart = localStorage.getItem('anantha-cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  }, []);

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('anantha-cart', JSON.stringify(cart));
  }, [cart]);

  const addToCart = (product, selectedPrice) => {
    const existingItem = cart.find(
      item => item.id === product.id && item.weight === selectedPrice.weight
    );

    if (existingItem) {
      setCart(cart.map(item =>
        item.id === product.id && item.weight === selectedPrice.weight
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, {
        id: product.id,
        name: product.name,
        image: product.image,
        weight: selectedPrice.weight,
        price: selectedPrice.price,
        quantity: 1
      }]);
    }
  };

  const removeFromCart = (productId, weight) => {
    setCart(cart.filter(item => !(item.id === productId && item.weight === weight)));
  };

  const updateQuantity = (productId, weight, quantity) => {
    if (quantity <= 0) {
      removeFromCart(productId, weight);
    } else {
      setCart(cart.map(item =>
        item.id === productId && item.weight === weight
          ? { ...item, quantity }
          : item
      ));
    }
  };

  const clearCart = () => {
    setCart([]);
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getCartCount = () => {
    return cart.reduce((count, item) => count + item.quantity, 0);
  };

  return (
    <CartContext.Provider value={{
      cart,
      isOpen,
      setIsOpen,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getCartTotal,
      getCartCount
    }}>
      {children}
    </CartContext.Provider>
  );
};