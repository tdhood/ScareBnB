import React, { useState, useContext } from "react";
import UserContext from "./UserContext";
import { useNavigate } from "react-router-dom";

const DEFAULT_DATA = {
  title: "",
  description: "",
  location: "",
  price: "",
};

function ListingForm({ create }) {
  const { currUser } = useContext(UserContext);
  const [formData, setFormData] = useState(DEFAULT_DATA);
  const [selectedFile, setSelectedFile] = useState(null); // State to hold the File object                                 
  const [errorMessages, setErrorMessages] = useState(null);
  const navigate = useNavigate();

  function handleChange(evt) {
    const { name, value, type, files } = evt.target;
    if (type === "file") {
      setSelectedFile(files[0]); // Store the File object from the input                                                   
    } else {
      setFormData(currentData => ({
        ...currentData,
        [name]: value
      }));
    }
  }

  async function handleSubmit(evt) {
    evt.preventDefault();

    const submissionData = new FormData(); // Create FormData                                                              

    // Append text fields                                                                                                  
    submissionData.append("title", formData.title);
    submissionData.append("description", formData.description);
    submissionData.append("location", formData.location);
    submissionData.append("price", formData.price);

    if (currUser && currUser.id) {
      submissionData.append("user_id", currUser.id);
    } else {
      console.error("User ID is not available.");
      setErrorMessages(["User information is missing."]);
      return;
    }

    // Append the file if selected                                                                                         
    if (selectedFile instanceof Blob) { // Check if selectedFile is a File/Blob                                            
      submissionData.append("files", selectedFile, formData.title); // 'files' is the key backend expects               
    } else if (selectedFile) {
      console.error("Attempted to append a non-File/Blob object:", selectedFile);
      setErrorMessages(["Invalid file selected."]);
      return;
    }
    // If file is mandatory, add a check: if (!selectedFile) { ... return; }                                               

    try {
      let response = await create(submissionData); // 'create' function sends this FormData                                
      if (response && response.id) {
        navigate(`/listing/${response.id}`);
      } else {
        navigate('/');
      }
    } catch (err) {
      setErrorMessages(err);
    }
  }

  return (
    <form className="SignUpForm col-md-6 offset-md-3 col-lg-4 offset-lg-4"
      onSubmit={handleSubmit}>
      {/* Text inputs for title, description, location, price */}
      <div className="mb-2 col-md-7">
        <input id="Title" name="title" className="form-control" placeholder="title" onChange={handleChange}
          value={formData.title} aria-label="Title" />
      </div>
      <div className="mb-2 col-md-7">
        <input id="Description" name="description" className="form-control" placeholder="description"
          onChange={handleChange} value={formData.description} aria-label="description" />
      </div>
      <div className="mb-2 col-md-7">
        <input id="Location" name="location" className="form-control" placeholder="location" onChange={handleChange}
          value={formData.location} aria-label="location" />
      </div>
      <div className="mb-2 col-md-7">
        <input id="price" name="price" className="form-control" placeholder="price" onChange={handleChange}
          value={formData.price} aria-label="price" type="number" />
      </div>
      {/* File input */}
      <div className="mb-2 col-md-7">
        <input
          id="Image File"
          name="files" // Name attribute for the input element                                                             
          className="form-control"
          onChange={handleChange} // Updates selectedFile state                                                            
          aria-label="Image file"
          type="file"
        />
      </div>
      {errorMessages && ( /* Simplified error display */
        <div className="alert alert-danger">
          {Array.isArray(errorMessages) ? errorMessages.map((e, i) => <p key={i}>{e}</p>) :
            <p>{errorMessages.toString()}</p>}
        </div>
      )}
      <button className="btn-primary btn btn-md LoginBtn">
        Create Listing!
      </button>
    </form>
  );
}

export default ListingForm;
