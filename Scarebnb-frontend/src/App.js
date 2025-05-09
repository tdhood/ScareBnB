// import logo from './logo.svg';
import './App.css';
import UserContext from "./UserContext";
import decode from "jwt-decode";
import ScareBnBApi from './api';
import { useEffect, useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import Navigation from './Navigation';
import RouteList from './RouteList';
import Homepage from './Homepage';

/** App - wrapper
 * 
 * Props:
 * -None
 * 
 * State:
 * -Current User
 * 
 * App -> { Navigation, RouteList }
 */
function App() {
  const [currUser, setCurrUser] = useState({
    data: null,
    infoLoaded: false
  });
  const [token, setToken] = useState(ScareBnBApi.token)

  async function login(loginData) {
    let response = await ScareBnBApi.login(loginData)
    setToken(response.token)
    setCurrUser({data: response.user, infoLoaded: true});
  }

  async function signup(signupData) {
    let response = await ScareBnBApi.signup(signupData)
    setToken(response.token)
    setCurrUser({data: response.user, infoLoaded: true})
  }

  async function create(listingData) {
    let response = await ScareBnBApi.createListing(listingData)
    return response.listings
  }

  //  function getGuestToken() {
  //   const response = await ScareBnBApi.is_guest();
  //   setToken(response.token)
  //   ScareBnBApi.token = response.token;
  //   setCurrUser({data: response.user, infoLoaded: true})
  // }
  
  return (
    <div className="App">
    <UserContext.Provider value={{ currUser, token }}>
      <BrowserRouter>
      <Navigation />
      <Homepage />
      <RouteList login={login} signup={signup} create={create}/>
      </BrowserRouter>
     </UserContext.Provider>
    </div>
  );
}

export default App;
