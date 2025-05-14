import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
// import "./SignUpForm.css";


const DEFAULT_DATA = {
  username: "",
  password: "",
  first_name: "",
  last_name: "",
  email: "",
  bio: "",
};

/** Form for sign-up
 * takes to logged in homepage if successful
 *  Displays error message if sign-up fails
 *
 *  Props:
 *  - signup is a function from ShareBnBApp
 *
 *  State:
 *  - formData
 *  - errorMessage
 *
 *   Navigation -> SignUpForm
 *
 */


function SignUpForm({ signup }) {
  const [formData, setFormData] = useState(DEFAULT_DATA);
  const [errorMessages, setErrorMessages] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate                                                               


  /** Update form input. */
  function handleChange(evt) {
    const input = evt.target;
    setFormData(formData => ({
      ...formData,
      [input.name]: input.value
    }));

  }

  /** Call ShareBnBApp signup function or
   * updateErrorMessage state */
  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await signup(formData);
      navigate("/");
    } catch (err) {
      setErrorMessages(err);
    }
  }

  return (
    <form className="SignUpForm col-md-6 offset-md-3 col-lg-4 offset-lg-4"
      onSubmit={handleSubmit}>
      <div className="mb-2 col-md-7">
        <input
          id="Username"
          name="username"
          className="form-control"
          placeholder="Username"
          onChange={handleChange}
          value={formData.username}
          aria-label="Username"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Password"
          name="password"
          className="form-control"
          placeholder="Password"
          onChange={handleChange}
          value={formData.password}
          aria-label="Password"
          type="password"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Firstname"
          name="first_name"
          className="form-control"
          placeholder="Firstname"
          onChange={handleChange}
          value={formData.first_name}
          aria-label="Firstname"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Lastname"
          name="last_name"
          className="form-control"
          placeholder="Lastname"
          onChange={handleChange}
          value={formData.last_name}
          aria-label="Lastname"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Email"
          name="email"
          className="form-control"
          placeholder="Email"
          onChange={handleChange}
          value={formData.email}
          aria-label="Email"
        />
      </div>
      <div className="mb-2 col-md-7">
        <textarea
          id="bio"
          name="bio"
          className="form-control"
          placeholder="Bio"
          onChange={handleChange}
          value={formData.bio}
          aria-label="Bio"
        />
      </div>
      {errorMessages !== null &&
        <div className="alert"><p>{errorMessages}</p></div>}
      <button className="btn-primary btn btn-md LoginBtn">
        Sign Up!
      </button>
    </form>
  );
}

export default SignUpForm;