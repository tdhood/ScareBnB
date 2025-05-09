import axios from "axios";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:5000";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class ScareBnBApi {
    
    static token = '';

    static async request(endpoint, data = {}, method = "get") {
        console.debug("API Call:", endpoint, data, method);
    
        const url = `${BASE_URL}/${endpoint}`;
        const headers = { AuthToken: `${ScareBnBApi.token}` };
        const params = (method === "get")
          ? data
          : {};
    
        try {
          return (await axios({ url, method, data, params, headers, withCredentials: true})).data;
        } catch (err) {
            console.log("unobstructed error message", err)
            console.error("API Error:", err.response);
            let message = err.response.data.error.message;
            throw Array.isArray(message) ? message : [message];
        }
    }

    // Individual API Routes
//#####################################################################
// LISTING ROUTES

    /** Get listings */
    static async getListingsForGuest() {
        console.debug("Token being sent:", ScareBnBApi.token);
        console.log("getListingsForGuest")
        let res = await this.request(`guest/listings`);
        return res.listings;
    }

    static async getListings(user_id) {
        let res = await this.request(`user/${user_id}/favorites`);
        return res.listings;
    }

    /** Get details for listing on a listing id */

    static async getListing(id) {
        let res = await this.request(`listing/${id}`);
        return res.listing;
    }

    /**Create new listing */

    static async createListing(data) {
        let res = await this.request(`listing`, data, "post");
        return res.listing;
    }


//#####################################################################
// USER ROUTES

    /** User signup */

    static async signup(data) {
        let res = await this.request(`signup`, data, "post");
        this.token = res.token
        return res;
    }

    /** User login */

    static async login(data) {
        let res = await this.request(`login`, data, "post");
        this.token = res.token
        return res;
    }

    /** User is Guest */
    static async is_guest() {
        console.log("is_guest")
        let res = await this.request(`guest`, {} ,"get");
        this.token = res.token
        console.log('token?????', this.token)
        return res;
    }


}

export default ScareBnBApi;