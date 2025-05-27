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
  const [token, setToken] = useState(ScareBnBApi.token || null)

  // Effect to synchronize App's token state with ScareBnBApi.token             
  useEffect(() => {                                                             
    ScareBnBApi.token = token;                                                  
  }, [token]); 

  // Effect to load initial user from token or fetch guest token                
  useEffect(() => {                                                             
    async function loadInitialData() {                                          
      if (token) {                                                              
        // If there's a token (e.g., from previous session, login, signup)      
        // You might want to decode it and fetch user details                   
        // For example:                                                         
        // try {                                                                
        //   const { username } = decode(token);                                
        //   // Assuming you have an API endpoint like ScareBnBApi.getCurrentUser(username)                                            
        //   // const user = await ScareBnBApi.getCurrentUser(username);        
        //   // setCurrUser({ data: user, infoLoaded: true });                  
        //   // For now, we'll assume login/signup sets currUser directly.      
        // } catch (e) {                                                        
        //   console.error("App.js: Error processing token", e);                
        //   setCurrUser({ data: null, infoLoaded: true });                     
        //   setToken(null); // Clear invalid token                             
        // }                                                                    
      } else if (!currUser.data && currUser.infoLoaded === false) { 
        // Only fetch guest token if not logged in and not yet attempted                        
        console.log("App.js: No active user, attempting to get guest token.");  
        try {                                                                   
          const guestResponse = await ScareBnBApi.is_guest();                   
          if (guestResponse.token) {                                            
            setToken(guestResponse.token);                                      
            // Optionally, if is_guest returns user-like data for 'guest':      
            setCurrUser({ data: guestResponse.user, infoLoaded: true });     
            console.log("App.js: Guest token obtained and set.");               
          }                                                                     
        } catch (err) {                                                         
          console.error("App.js: Failed to get guest token", err);              
          // Ensure infoLoaded is true so we don't retry indefinitely           
          setCurrUser(prev => ({ ...prev, infoLoaded: true }));                 
        }                                                                       
      }                                                                         
    }                                                                           
                                                                                
    loadInitialData();                                                          
    // Add currUser.infoLoaded to dependencies if you want it to re-run when infoLoaded changes.                                                             
    // For guest token, typically run once if no token.                         
  }, [token, currUser.data]); // Re-run if token changes or user data is set/cleared 

  async function login(loginData) {
    let response = await ScareBnBApi.login(loginData)
    setToken(response.token)
    setCurrUser({data: response.user, infoLoaded: true});
    console.log('app.jy login', response.user)
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

  
  return (
    <div className="App">
    <UserContext.Provider value={{ currUser: currUser.data, token }}>
      <BrowserRouter>
      <Navigation />
      <RouteList login={login} signup={signup} create={create} />
      </BrowserRouter>
     </UserContext.Provider>
    </div>
  );
}

export default App;
