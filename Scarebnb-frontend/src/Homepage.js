import React, { useState, useEffect, useContext } from "react";
import UserContext from "./UserContext";
import ScareBnBApi from "./api";
import ListingCard from "./ListingCard";

/**
 * Homepage component
 * 
 * Context: currUser (not currently used)
 * State:
 * - listings: { data: Array|null, isLoading: boolean }
 *
 * Displays listings for guest users
 */
function Homepage() {
  const { currUser, token } = useContext(UserContext);
  const [listings, setListings] = useState({
    data: null,
    isLoading: true,
  });

  useEffect(() => {
    async function loadGuestListings() {
      if (token) {
        // Check if token is available (either guest or logged-in user)
        console.log("Homepage: Attempting to load listings with token:", token); 
        try {
          // ScareBnBApi.getListingsForGuest() returns the listings array directly
          let fetchedListing = await ScareBnBApi.getListingsForGuest();
          console.log('did i fetch listings?', fetchedListing)
          setListings({ data: fetchedListing, isLoading: false });
          console.log('looking for listings', 'listings.data', listings.data, 'listings', listings)
        } catch (err) {
          console.error("Error loading listings:", err);
          setListings({ data: null, isLoading: false }); // Set isLoading to false on error 
        }
      } else {
        // No token available, perhaps App.js is still fetching it or failed.   
        console.log("Homepage: No token available yet to fetch listings.");     
        // You might want to keep isLoading true until a token is available or guest fetch fails in App.js                                                     
        // Or, if App.js signals completion of initial load, then set isLoading to false.                                                                       
        // For simplicity here, if no token, we'll consider it not loading listings. 
        setListings({ data: null, isLoading: false }); 
      }
    }
    loadGuestListings();
  }, [token]);

  if (listings.isLoading) return <p>Loading...</p>;
  if (!listings.data || listings.data.length === 0) return <p>No listings available.</p>;

  return (
    <div className="Homepage">
      {listings.data.map(listing => (
        <ListingCard key={listing.id} listing={listing} />
      ))}
    </div>
  );
}

export default Homepage;
