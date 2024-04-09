const scrapper = require("linkedin-catcher");

scrapper({
    url: "rishab-jain-k/", // e.g., Pragati Kumari/
}).then(res => console.warn(res));