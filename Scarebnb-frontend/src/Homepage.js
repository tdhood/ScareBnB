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
    async function loadListings() {
      if (token) {
        
        setListings(prevListings => ({ ...prevListings, isLoading: true }));
        console.log("Homepage: Attempting to load listings with token");
        try {
          let listings = await ScareBnBApi.getAllListings();
          setListings({ data: listings, isLoading: false });
        } catch (err) {
          console.error("Error loading listings:", err);
          setListings({ data: null, isLoading: false });
        }
      } else {
        console.log("Homepage: No token available yet to fetch listings.");
        setListings({ data: null, isLoading: false });
      }
      
    }
    loadListings();
  }, [token]);

  console.log(listings.data)

    

  if (listings.isLoading) return <p>Loading...</p>;
  if (!listings.data || listings.data.length === 0) return <p>No listings available.</p>;

  // Determine if the current user is the specific guest user                                                             
  const isGuestUser = currUser && currUser.username === "guest";
  // Determine if the current user is a logged-in (non-guest) user                                                        
  const isLoggedInUser = currUser && currUser.username !== "guest";
  console.log("isGuest?=", isGuestUser)
  console.log("isUser?=", isLoggedInUser)
    return (
      <div className="Homepage">
        {isLoggedInUser && (
          <div>
            {/* Content for logged-in users */}
            <h2>Welcome back, {currUser.username}!</h2>
            <p>Explore all our haunted locations.</p>
            {/* Potentially display all listings or full features here */}
          </div>
        )}

        {isGuestUser && (
          <div>
            {/* Content for guests (limited homepage) */}
            <h2>Welcome, Guest!</h2>
            <p>You are viewing a limited selection. Log in or sign up for the full experience!</p>
            {/* Potentially display a limited set of listings or features here */}
          </div>
        )}

        {/* Fallback if currUser is not yet defined (e.g., initial load before guest user is set) */}
        {!currUser && !listings.isLoading && (
          <div>
            <h2>Welcome to ScareBnB!</h2>
          </div>
        )}

        {/* Common listings display logic */}
        {/* This part shows listings. If guests should see different listings,                                              
          this map function or the data source (listings.data) would also need to be conditional.                         
          For now, it shows all fetched listings to everyone who isn't seeing "Loading...". */}
        {(!listings.data || listings.data.length === 0)
          ? <p>No listings available at the moment.</p>
          : listings.data.map(listing => (
            <ListingCard key={listing.id} listing={listing} />
          ))
        }
      </div>    
    );                                                                                                            
  
  }

export default Homepage;
