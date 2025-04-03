import React, { useEffect, useRef, useState } from "react";

const GetYourPhotos = () => {
  const faceImg = useRef(null);
  const api = "http://localhost:8000/upload";
  const [selectedImage, setSelectedImage] = useState(null);
  const [eventId, setEventId] = useState("E0001");

  const handleUpload = (e) => {
    faceImg.current.click();
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      faceImg.current.value = null; // Reset the input value
    }
  };

  useEffect(() => {
    const formData = new FormData();
    formData.append("image", selectedImage);
    formData.append("eventId", eventId);

    if (selectedImage) {
      fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json", // Ensure JSON response
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Image upload failed");
        });
    }
  }, [selectedImage]);

  return (
    <div className="flex flex-col w-full h-svh p-2  items-center">
      <span className="text-3xl font-bold">GetYourPhotos</span>
      <div className="flex flex-col w-96 p-4 border rounded-lg border-teal-700 bg-teal-700 items-center justify-center mt-4 shadow-xl">
        <input
          type="file"
          ref={faceImg}
          className="hidden"
          onChange={handleChange}
          accept="image/jpeg"
        />
        <label className="pt-2 pb-6 text-center items-center text-black font-bold">
          Upload your selfie to find your photos captured during the event
        </label>
        <button
          className="border bg-blue-800/40 border-blue-800/40 font-bold rounded-2xl px-2 py-1 hover:bg-blue-500/40 cursor-pointer"
          onClick={handleUpload}
        >
          Upload
        </button>
      </div>
    </div>
  );
};

export default GetYourPhotos;
