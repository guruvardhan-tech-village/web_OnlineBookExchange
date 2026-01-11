import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">BookExchange</h3>
            <p className="text-gray-300 text-sm">
              Connect with fellow book lovers and exchange your favorite reads.
              Discover new books and share the joy of reading.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="/books" className="text-gray-300 hover:text-white transition-colors">
                  Browse Books
                </a>
              </li>
              <li>
                <a href="/about" className="text-gray-300 hover:text-white transition-colors">
                  About Us
                </a>
              </li>
              <li>
                <a href="/contact" className="text-gray-300 hover:text-white transition-colors">
                  Contact
                </a>
              </li>
              <li>
                <a href="/help" className="text-gray-300 hover:text-white transition-colors">
                  Help
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact</h3>
            <div className="text-gray-300 text-sm space-y-2">
              <p>Email: support@bookexchange.com</p>
              <p>Phone: (555) 123-4567</p>
              <div className="flex space-x-4 mt-4">
                <button className="text-gray-300 hover:text-white transition-colors">
                  Facebook
                </button>
                <button className="text-gray-300 hover:text-white transition-colors">
                  Twitter
                </button>
                <button className="text-gray-300 hover:text-white transition-colors">
                  Instagram
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300 text-sm">
          <p>&copy; 2024 BookExchange. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;