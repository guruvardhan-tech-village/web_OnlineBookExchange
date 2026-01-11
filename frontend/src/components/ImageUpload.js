import React, { useState, useRef, useCallback } from 'react';

const ImageUpload = ({
  onImageSelect,
  onImageRemove,
  currentImage = null,
  maxSize = 5 * 1024 * 1024, // 5MB default
  acceptedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'],
  className = '',
  disabled = false
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState(currentImage);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const validateFile = (file) => {
    // Check file type
    if (!acceptedTypes.includes(file.type)) {
      return `Invalid file type. Please select: ${acceptedTypes.join(', ')}`;
    }

    // Check file size
    if (file.size > maxSize) {
      const maxSizeMB = (maxSize / (1024 * 1024)).toFixed(1);
      return `File size too large. Maximum size: ${maxSizeMB}MB`;
    }

    return null;
  };

  const processFile = useCallback((file) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError(null);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
    };
    reader.readAsDataURL(file);

    // Call parent callback
    if (onImageSelect) {
      onImageSelect(file);
    }
  }, [maxSize, acceptedTypes, onImageSelect]);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  }, [disabled, processFile]);

  const handleFileInput = (e) => {
    if (disabled) return;

    const files = e.target.files;
    if (files && files[0]) {
      processFile(files[0]);
    }
  };

  const handleClick = () => {
    if (disabled) return;
    fileInputRef.current?.click();
  };

  const handleRemove = () => {
    if (disabled) return;

    setPreview(null);
    setError(null);
    
    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }

    if (onImageRemove) {
      onImageRemove();
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-6 transition-colors ${
          dragActive
            ? 'border-blue-400 bg-blue-50'
            : preview
            ? 'border-green-300 bg-green-50'
            : error
            ? 'border-red-300 bg-red-50'
            : 'border-gray-300 bg-gray-50 hover:bg-gray-100'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={acceptedTypes.join(',')}
          onChange={handleFileInput}
          className="hidden"
          disabled={disabled}
        />

        {preview ? (
          /* Preview Mode */
          <div className="text-center">
            <div className="relative inline-block mb-4">
              <img
                src={preview}
                alt="Preview"
                className="max-w-full max-h-48 rounded-lg shadow-md"
              />
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemove();
                }}
                className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg hover:bg-red-600 transition-colors"
                disabled={disabled}
              >
                ×
              </button>
            </div>
            <p className="text-sm text-green-600 font-medium">
              Image uploaded successfully
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Click to change or drag a new image here
            </p>
          </div>
        ) : (
          /* Upload Mode */
          <div className="text-center">
            <div className="mx-auto w-16 h-16 mb-4">
              <svg
                className={`w-full h-full ${
                  error ? 'text-red-400' : dragActive ? 'text-blue-400' : 'text-gray-400'
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
            </div>
            
            <div className="space-y-2">
              <p className={`text-lg font-medium ${
                error ? 'text-red-600' : dragActive ? 'text-blue-600' : 'text-gray-700'
              }`}>
                {dragActive ? 'Drop image here' : 'Upload an image'}
              </p>
              
              <p className="text-sm text-gray-500">
                Drag and drop or click to browse
              </p>
              
              <p className="text-xs text-gray-400">
                Supported: {acceptedTypes.map(type => type.split('/')[1].toUpperCase()).join(', ')} 
                • Max size: {formatFileSize(maxSize)}
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-sm text-red-600">{error}</p>
          </div>
        </div>
      )}

      {/* Upload Progress (if needed in future) */}
      {/* This can be extended to show upload progress */}
    </div>
  );
};

export default ImageUpload;