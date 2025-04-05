import React, { useEffect, useRef, useState } from "react";

const GetYourPhotos = () => {
    const faceImg = useRef(null);
    const api = "http://localhost:8000";
    const [selectedImage, setSelectedImage] = useState(null);
    const [eventId, setEventId] = useState("E0001");
    const [matchedImages, setMatchedImages] = useState([]);
    const [formMessage, setFormMessage] = useState("");

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
        formData.append("file", selectedImage);
        formData.append("event_id", eventId);

        if (selectedImage) {
            setFormMessage("Please Wait...");
            setMatchedImages([]);
            fetch(`${api}/gyp/upload/`, {
                method: "POST",
                body: formData,
                headers: {
                    Accept: "application/json", // Ensure JSON response
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "success") {
                        setMatchedImages(data["matched_files"]);
                    } else {
                        setMatchedImages([]);
                        setFormMessage(data["message"]);
                    }
                })
                .finally(() => {
                    setFormMessage("");
                });
        }
    }, [selectedImage]);

    return (
        <div className="flex flex-col w-full h-svh p-6 items-center">
            <span className="text-3xl font-bold">GetYourPhotos</span>
            <div className="flex flex-col w-96 p-4 border rounded-lg border-teal-700 bg-teal-700 items-center justify-center mt-4 shadow-xl">
                <input name="file" type="file" ref={faceImg} className="hidden" onChange={handleChange} accept="image/jpeg" />
                <label className="pt-2 pb-6 text-center items-center text-black font-bold">Upload your selfie to find your photos captured during the event</label>
                <button className="border bg-blue-800/40 border-blue-800/40 font-bold rounded-2xl px-2 py-1 hover:bg-blue-500/40 cursor-pointer" onClick={handleUpload}>
                    Upload
                </button>
                {formMessage && <p className="font-bold text-amber-950 mt-2">{formMessage}</p>}
            </div>

            {matchedImages.length > 0 && (
                <div className="grid grid-cols-3 items-center justify-center bg-teal-700 border-teal-700  border rounded-2xl shadow-2xl w-full h-fit mt-4 gap-2 p-6``">
                    {matchedImages.map((image, index) => (
                        <img key={index} src={`${api}${image}`} className="w-96 border-2 rounded-2xl" />
                    ))}
                </div>
            )}
        </div>
    );
};

export default GetYourPhotos;
