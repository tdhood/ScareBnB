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
  const { currUser } = useContext(UserContext);
  const [listings, setListings] = useState({
    data: null,
    isLoading: true,
  });

  useEffect(() => {
    async function loadGuestTokenListings() {
      try {
        let responseToken = await ScareBnBApi.is_guest();
        console.log('token?', responseToken.token)
        ScareBnBApi.token = responseToken.token;

        let responseListing = await ScareBnBApi.getListingsForGuest();
        setListings({ data: responseListing.listings, isLoading: false });
      } catch (err) {
        console.error("Error loading guest token or listings:", err);
      }
    }

    loadGuestTokenListings();
  }, []);

  if (listings.isLoading) return <p>Loading...</p>;

  return (
    <div className="Homepage">
      {listings.data.map(listing => (
        <ListingCard key={listing.id} listing={listing} />
      ))}
    </div>
  );
}

export default Homepage;
