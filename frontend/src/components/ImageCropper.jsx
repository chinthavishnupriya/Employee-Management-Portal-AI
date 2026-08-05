import { useState, useCallback } from "react";
import Cropper from "react-easy-crop";
import getCroppedImg from "../utils/cropImage";

function ImageCropper({ image, onCancel, onCropComplete }) {

    const [crop, setCrop] = useState({ x: 0, y: 0 });

    const [zoom, setZoom] = useState(1);

    const [croppedAreaPixels, setCroppedAreaPixels] = useState(null);

    const onCropCompleteCallback = useCallback(
        (croppedArea, croppedAreaPixels) => {
            setCroppedAreaPixels(croppedAreaPixels);
        },
        []
    );

    async function handleCrop() {

    try {

        const croppedFile = await getCroppedImg(
            image,
            croppedAreaPixels
        );

        onCropComplete(croppedFile);

    }

    catch (error) {

        console.error(error);

        alert("Unable to crop image.");

    }

}

    return (

        <div
            className="position-fixed top-0 start-0 w-100 h-100"
            style={{
    background: "rgba(0,0,0,0.92)",
    zIndex: 9999,
    overflow: "auto"
}}
        >

            <div
                className="position-relative"
                style={{
                    width: "100%",
                    height: "65%"
                }}
            >

                <Cropper

                    image={image}

                    crop={crop}

                    zoom={zoom}

                    aspect={1}

                    cropShape="round"

                    showGrid={false}

                    onCropChange={setCrop}

                    onZoomChange={setZoom}

                    onCropComplete={onCropCompleteCallback}

                />

            </div>

            <div
    className="bg-white p-3 shadow-lg rounded-top"
    style={{
        height: "35vh",
        overflowY: "auto"
    }}
>

                <h4 className="text-center mb-4">

    Crop Your Profile Picture

</h4>

<p className="text-center text-muted">

    Drag the image and use the slider to position your face.

</p>

<label className="fw-bold">

    Zoom

</label>

<input

    type="range"

    min={1}

    max={5}

    step={0.1}

    value={zoom}

    onChange={(e) =>
        setZoom(Number(e.target.value))
    }

    className="form-range"

 />

<div className="d-flex justify-content-center gap-3 mt-4">

    <button
        className="btn btn-outline-secondary"
        onClick={onCancel}
    >
        Cancel
    </button>

    <button
        className="btn btn-success"
        onClick={handleCrop}
    >
        Save Photo
    </button>

</div>
                <button
                    className="btn btn-primary"
                    onClick={handleCrop}
                >
                    Crop Image
                </button>

            </div>

        </div>

    );

}

export default ImageCropper;