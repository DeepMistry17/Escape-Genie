import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import MapComponent from './MapComponent';

const StarRating = ({ rating, setRating }) => {
    return (
        <div className="star-rating">
            {[...Array(5)].map((_, index) => {
                const starValue = index + 1;
                return (
                    <span
                        key={starValue}
                        className={starValue <= rating ? 'star-filled' : 'star-empty'}
                        onClick={() => setRating(starValue)}
                    >
                        ★
                    </span>
                );
            })}
        </div>
    );
};


const VenuesModal = ({ city, onClose, isDarkMode }) => {
    const [venues, setVenues] = useState({ attractions: [], restaurants: [] });
    const [reviews, setReviews] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedVenue, setSelectedVenue] = useState(null);

    // This state now controls the expansion to the 3-column layout
    const [isExpanded, setIsExpanded] = useState(false);

    // Review Form State
    const [userRating, setUserRating] = useState(0);
    const [userComment, setUserComment] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fetchVenuesAndReviews = useCallback(async () => {
        setIsLoading(true);
        try {
            // Fetch venues
            const venuesResponse = await fetch('http://127.0.0.1:5000/api/venues', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city: city }),
            });
            const venuesData = await venuesResponse.json();
            setVenues(venuesData || { attractions: [], restaurants: [] });

            // Fetch reviews
            const reviewsResponse = await fetch(`http://127.0.0.1:5000/api/reviews/${city.id}`);
            const reviewsData = await reviewsResponse.json();
            setReviews(reviewsData || []);

        } catch (error) {
            console.error("Failed to fetch data:", error);
        } finally {
            setIsLoading(false);
        }
    }, [city]);

    useEffect(() => {
        fetchVenuesAndReviews();
    }, [fetchVenuesAndReviews]);

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        if (userRating === 0) {
            alert("Please select a rating.");
            return;
        }
        setIsSubmitting(true);
        const token = localStorage.getItem('token');
        const username = localStorage.getItem('username');

        try {
            const response = await fetch('http://127.0.0.1:5000/api/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    destination_id: city.id,
                    rating: userRating,
                    comment: userComment,
                    username: username
                }),
            });

            if (response.ok) {
                setUserRating(0);
                setUserComment('');
                fetchVenuesAndReviews();
            } else {
                alert("Failed to submit review.");
            }
        } catch (error) {
            console.error("Error submitting review:", error);
            alert("An error occurred while submitting your review.");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleVenueClick = (venue) => {
        setSelectedVenue(venue);
        setIsExpanded(true); // Expand the modal on click
    };

    const renderVenueList = (venueList) => {
        return venueList.map(venue => (
            <div key={venue.id || venue.name} className="venue-item" onClick={() => handleVenueClick(venue)}>
                <div className="venue-details">
                    <span className="venue-name">{venue.name}</span>
                    <span className="venue-address">{venue.address}</span>
                </div>
                <a
                    href={venue.Maps_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="venue-gmaps-link"
                    onClick={(e) => e.stopPropagation()}
                >
                    Directions
                </a>
            </div>
        ));
    };

    const averageRating = reviews.length > 0
        ? (reviews.reduce((acc, review) => acc + review.rating, 0) / reviews.length).toFixed(1)
        : 'No ratings yet';

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className={`modal-content ${isExpanded ? 'expanded' : ''}`} onClick={e => e.stopPropagation()}>
                <button className="modal-close-button" onClick={onClose}>×</button>
                <h2>{city.name}</h2>
                <div className="modal-header-rating">
                    <span className="avg-rating-stars">{'★'.repeat(Math.round(averageRating))}{'☆'.repeat(5 - Math.round(averageRating))}</span>
                    <span className="avg-rating-text">{averageRating} ({reviews.length} reviews)</span>
                </div>

                <div className="modal-body-split">
                    {/* Panel 1: Venues List */}
                    <div className="venues-list-panel">
                        {isLoading ? <p>Loading...</p> : (
                          <>
                            {venues.attractions && venues.attractions.length > 0 && (
                                <div className="venue-category">
                                    <h3>Attractions & Landmarks</h3>
                                    {renderVenueList(venues.attractions)}
                                </div>
                            )}
                            {venues.restaurants && venues.restaurants.length > 0 && (
                                <div className="venue-category">
                                    <h3>Restaurants & Cafes</h3>
                                    {renderVenueList(venues.restaurants)}
                                </div>
                            )}
                          </>
                        )}
                    </div>

                    {/* Panel 2: Map (only shows in expanded view) */}
                    <div className={`venues-map-panel ${isExpanded ? 'visible' : ''}`}>
                        <MapComponent
                            locations={selectedVenue ? [selectedVenue] : []}
                            isDarkMode={isDarkMode}
                            defaultZoom={15}
                        />
                    </div>

                    {/* Panel 3: Reviews (only shows in expanded view) */}
                    <div className={`reviews-panel ${isExpanded ? 'visible' : ''}`}>
                         <div className="venue-category">
                            <h3>Reviews</h3>
                            <div className="reviews-list-container">
                              {reviews.length > 0 ? (
                                  reviews.map(review => (
                                      <div key={review.id} className="review-item">
                                          <div className="review-header">
                                              <strong>{review.username}</strong>
                                              <span className="review-stars">{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}</span>
                                          </div>
                                          <p>{review.comment}</p>
                                          <span className="review-timestamp">{new Date(review.timestamp).toLocaleDateString()}</span>
                                      </div>
                                  ))
                              ) : (
                                  <p>No reviews yet. Be the first!</p>
                              )}
                            </div>
                        </div>

                        <div className="venue-category review-form-container">
                            <h3>Leave a Review</h3>
                            <form onSubmit={handleReviewSubmit} className="review-form">
                                <StarRating rating={userRating} setRating={setUserRating} />
                                <textarea
                                    value={userComment}
                                    onChange={(e) => setUserComment(e.target.value)}
                                    placeholder="Share your experience..."
                                    rows="4"
                                />
                                <button type="submit" disabled={isSubmitting}>
                                    {isSubmitting ? 'Submitting...' : 'Submit Review'}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default VenuesModal;