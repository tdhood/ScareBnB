import React, { useState, useContext } from "react";
import UserContext from "./UserContext";



const DEFAULT_DATA = {
  title: "",
  description: "",
  location: "",
  price: "",
  image_url: "",
  rating: "",
};

/** Form for create listing
 * takes to logged in homepage if successful
 *  Displays error message if creation fails
 *
 *  Props:
 *  - create is a function from App
 *
 *  State:
 *  - formData
 *  - errorMessage
 *
 *  Navigation -> ListingForm
 *
 */


function ListingForm({ create }) {
  const { currUser } = useContext(UserContext)
  const [formData, setFormData] = useState(DEFAULT_DATA);
  const [errorMessages, setErrorMessages] = useState(null);

  /** Update form input. */
  function handleChange(evt) {
    const input = evt.target;
    setFormData(formData => ({
      ...formData,
      [input.name]: input.value
    }));

  }

  /** Call App signup function or
   * updateErrorMessage state */
  async function handleSubmit(evt) {
    evt.preventDefault();
    try {
      await create({...formData, user_id: currUser.id});
    } catch (err) {
      setErrorMessages(err);
    }
  }

  return (
    <form className="SignUpForm col-md-6 offset-md-3 col-lg-4 offset-lg-4"
      onSubmit={handleSubmit}>
      <div className="mb-2 col-md-7">
        <input
          id="Title"
          name="title"
          className="form-control"
          placeholder="title"
          onChange={handleChange}
          value={formData.title}
          aria-label="Title"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Description"
          name="description"
          className="form-control"
          placeholder="description"
          onChange={handleChange}
          value={formData.description}
          aria-label="description"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Location"
          name="location"
          className="form-control"
          placeholder="location"
          onChange={handleChange}
          value={formData.location}
          aria-label="location"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="price"
          name="price"
          className="form-control"
          placeholder="price"
          onChange={handleChange}
          value={formData.price}
          aria-label="price"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Image File"
          name="files"
          className="form-control"
          placeholder="Image File"
          onChange={handleChange}
          value={formData.files}
          aria-label="Image file"
          type="file"
        />
      </div>
      <div className="mb-2 col-md-7">
        <input
          id="Rating"
          name="rating"
          className="form-control"
          placeholder="rating"
          onChange={handleChange}
          value={formData.rating}
          aria-label="Rating"
        />
      </div>
      {errorMessages !== null &&
        <div className="alert"><p>{errorMessages}</p></div>}
      <button className="btn-primary btn btn-md LoginBtn">
        Create Listing!
      </button>
    </form>
  );
}

export default ListingForm;