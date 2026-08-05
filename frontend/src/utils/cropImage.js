export default function getCroppedImg(imageSrc, pixelCrop) {
    return new Promise((resolve, reject) => {

        const image = new Image();

        image.crossOrigin = "anonymous";

        image.src = imageSrc;

        image.onload = () => {

            const canvas = document.createElement("canvas");

            const ctx = canvas.getContext("2d");

            canvas.width = pixelCrop.width;
            canvas.height = pixelCrop.height;

            ctx.drawImage(
                image,
                pixelCrop.x,
                pixelCrop.y,
                pixelCrop.width,
                pixelCrop.height,
                0,
                0,
                pixelCrop.width,
                pixelCrop.height
            );

            canvas.toBlob((blob) => {

                if (!blob) {
                    reject(new Error("Canvas is empty"));
                    return;
                }

                // Convert Blob → File
                const file = new File(
                    [blob],
                    "profile.jpg",
                    {
                        type: "image/jpeg"
                    }
                );

                resolve(file);

            }, "image/jpeg", 0.95);

        };

        image.onerror = reject;

    });
}