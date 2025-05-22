import { NavLink } from "react-router-dom";
// import "./Navigation.css";
import {useContext} from "react";
import UserContext from "./UserContext";

/** navigation bar for the sharebnb app
 * renders on every page
 *
 * Navigation -> {homepage, Companies, Jobs}
 */
//FIXME: Logout function
function Navigation() {
  const { currUser } = useContext(UserContext);
  console.log('currUser', currUser)
  return (
    <nav className="Navigation navbar navbar-expand-md container-fluid ms-auto">
      <NavLink key="homepage" to="/">ScareBnB</NavLink>
      { currUser && currUser.username !== 'guest'
      ?
        (<div className="Navigation-links ms-auto">
          <NavLink key="listingForm" to="/createlisting">Create Listing</NavLink>
          <NavLink key="profile" to="/profile">Profile</NavLink>
          {/* <NavLink key="logout" onClick={logout} to="/">{`Log Out ${currUser.username}`}</NavLink> */}
        </div>)
        : (<div className="Navigation-links ms-auto">
          <NavLink key="login" to="/login">Login</NavLink>
          <NavLink key="signup" to="/signup">Sign Up</NavLink>
        </div>)
      }
    </nav>
  );
}

export default Navigation;