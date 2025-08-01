import React, { useEffect, useCallback, useState } from 'react';
import { GoogleMap, useJsApiLoader, Marker } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '100%'
};

const defaultCenter = { lat: 20.5937, lng: 78.9629 };

const mapStyles = {
  dark: [
      { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
      { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
      { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
      { featureType: "administrative.locality", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
      { featureType: "poi", elementType: "labels.text.fill", stylers: [{ color: "#d59563" }] },
      { featureType: "poi.park", elementType: "geometry", stylers: [{ color: "#263c3f" }] },
      { featureType: "road", elementType: "geometry", stylers: [{ color: "#38414e" }] },
      { featureType: "road", elementType: "geometry.stroke", stylers: [{ color: "#212a37" }] },
      { featureType: "road.highway", elementType: "geometry", stylers: [{ color: "#746855" }] },
      { featureType: "transit", elementType: "geometry", stylers: [{ color: "#2f3948" }] },
      { featureType: "water", elementType: "geometry", stylers: [{ color: "#17263c" }] },
  ],
};

function MapComponent({ locations, isDarkMode, defaultZoom = 4 }) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.REACT_APP_Maps_API_KEY
  });

  // State to hold the map instance
  const [map, setMap] = useState(null);

  // Callback to set the map instance once it's loaded
  const onLoad = useCallback(function callback(map) {
    setMap(map);
  }, []);

  // Effect to adjust bounds when locations change
  useEffect(() => {
    if (map && locations && locations.length > 1) {
      const bounds = new window.google.maps.LatLngBounds();
      locations.forEach(loc => {
        bounds.extend(new window.google.maps.LatLng(loc.lat, loc.lon));
      });
      map.fitBounds(bounds);
    }
  }, [map, locations]);
  
  // Logic for single point zoom or default view
  const mapCenter = locations && locations.length > 0 ? { lat: locations[0].lat, lng: locations[0].lon } : defaultCenter;
  const zoomLevel = locations && locations.length === 1 ? 14 : defaultZoom; // Changed for single location zoom

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={mapCenter}
      zoom={zoomLevel}
      onLoad={onLoad} // Added onLoad callback
      options={{
        styles: isDarkMode ? mapStyles.dark : [],
        disableDefaultUI: true,
        zoomControl: true
      }}
    >
      {locations && locations.map(loc => (
        <Marker
          key={loc.id}
          position={{ lat: loc.lat, lng: loc.lon }}
          title={loc.name}
        />
      ))}
    </GoogleMap>
  ) : <p>Loading Map...</p>;
}

export default React.memo(MapComponent);