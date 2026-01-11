import { useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import recommendationService from '../services/recommendationService';

const useInteractionTracking = () => {
  const { user } = useAuth();

  const trackInteraction = useCallback(async (bookId, interactionType) => {
    // Only track interactions for authenticated users
    if (!user || !bookId) {
      return;
    }

    try {
      await recommendationService.recordInteraction(bookId, interactionType);
    } catch (error) {
      // Silently fail for interaction tracking to not disrupt user experience
      console.warn('Failed to track interaction:', error);
    }
  }, [user]);

  const trackView = useCallback((bookId) => {
    trackInteraction(bookId, 'view');
  }, [trackInteraction]);

  const trackLike = useCallback((bookId) => {
    trackInteraction(bookId, 'like');
  }, [trackInteraction]);

  const trackRequest = useCallback((bookId) => {
    trackInteraction(bookId, 'request');
  }, [trackInteraction]);

  const trackSearch = useCallback((searchTerm) => {
    // For search tracking, we'll track it as a general search interaction
    // In a real implementation, you might want to track specific search terms
    if (searchTerm && searchTerm.trim()) {
      // We can't track search without a specific book, so we'll skip this for now
      // or implement a different tracking mechanism for search terms
      console.log('Search tracked:', searchTerm);
    }
  }, []);

  return {
    trackView,
    trackLike,
    trackRequest,
    trackSearch,
    trackInteraction
  };
};

export default useInteractionTracking;