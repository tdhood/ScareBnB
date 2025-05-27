import { Navigate, Route, Routes } from "react-router-dom";
import Homepage from "./Homepage";
import LoginForm from "./LoginForm";
import SignupForm from "./SignupForm";
import ListingForm from "./ListingForm";
import Listing from "./Listing";

/**Routes for browser
 *
 * props=functions to be called in parent: login, signup, logout
 * state=none
 *
 * App --> RouterList --> { Homepage, CompanyList, CompanyDetail, JobList, LoginForm,
 * SignupForm, ProfileForm, Logout}
 */
function RouteList({ login, signup, create, id }) {
  console.log("RouteList")
  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/login" element={<LoginForm login={login} />} />
      <Route path="/signup" element={<SignupForm signup={signup} />} />
      <Route path="/createlisting" element={<ListingForm create={create} />} />
      <Route path="/listing/<id:int>" element={<Listing listingID={id} />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default RouteList;



//<Route path="/profile" element={<ProfileForm />} />
//<Route path="/logout" element={<Logout logout={logout} />} />