import React, { useState, useEffect, useContext } from "react";
import UserContext from "./UserContext";
import ScareBnBApi from "./api";
import ListingCard from "./ListingCard";

function Listing(id) {
    const {currUser, token} = useContext(UserContext);
    const [listing, setListing] = useState({
        data: null,
        isLoading: true,
    });


    useEffect(() => {
        async function loadListing() {
            if (token) {
                try {
                    let listing = await ScareBnBApi.getListing(id);
                    setListing({data: listing, isLoading: false});
                } catch (err) {
                    console.error(`Error loading Listing ${id}`, err)
                    setListing({data:null, isLoading:false});
                }
            } else {
                console.log("Listing page did not load, but no errors")
                setListing({data: null, isLoading: false});
            }
        }
        loadListing();
    }, [id])

    return (
        <div className="Listing">
            <div>
                <h2>Your New Listing!</h2>
            </div>
            <ListingCard key={listing.id} listing={listing} />
        </div>
    )

}

export default Listing;