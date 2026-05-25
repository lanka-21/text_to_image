import React from "react";

function ImageCard({ src }) {
  const fallbackSvg = `data:image/svg+xml;utf8,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="768" height="512">
      <rect width="100%" height="100%" fill="#1e3a8a"/>
      <text x="50%" y="48%" text-anchor="middle" fill="#e2e8f0" font-size="24" font-family="Arial">Image unavailable</text>
      <text x="50%" y="58%" text-anchor="middle" fill="#bfdbfe" font-size="16" font-family="Arial">Try generate again</text>
    </svg>`
  )}`;

  return (
    <div
      style={{
        borderRadius: "12px",
        overflow: "hidden",
        transition: "0.3s",
        cursor: "pointer"
      }}
      onMouseOver={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
      onMouseOut={(e) => (e.currentTarget.style.transform = "scale(1)")}
    >
      <img
        src={src}
        alt="generated"
        loading="lazy"
        onError={(e) => {
          if (e.currentTarget.src !== fallbackSvg) {
            e.currentTarget.src = fallbackSvg;
          }
        }}
        style={{
          width: "100%",
          height: "200px",
          objectFit: "cover"
        }}
      />
    </div>
  );
}

export default ImageCard;