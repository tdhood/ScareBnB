import React from "react";
import { Link } from "react-router-dom";

/** Shows a card for a listing
 *
 * props: listing {}
 *
 * states: none
 *
 * Homepage -> ListingCard
 */

function ListingCard({ listing }){
  return (
    <div className="ListingCard">
      <Link className="ListingCard-Link" to={`/listing/${listing.id}`}>
        <div className="ListingCard-img">
          <img src={listing.image_url} alt={listing.title}></img>
        </div>
        <div className="ListingCard-details">
        <h3>{listing.title}</h3>
        <p>{listing.description}</p>
        <ul>
          <li>Location: {listing.location}</li>
          <li>Price: {listing.price}</li>
          <li>Rating: {listing.rating}/5</li>
        </ul>
        </div>
      </Link>
    </div>
  )
}

export default ListingCard


//TODO: add info about host