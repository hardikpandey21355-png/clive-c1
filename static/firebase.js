// // Firebase CDN scripts
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// Your Firebase Config
const firebaseConfig = {
    apiKey: "AIzaSyAmInWJrr-Hb0xjOwwQ-dlDhyZq_M_ot5I",
    authDomain: "clive-v1.firebaseapp.com",
    projectId: "clive-v1",
     storageBucket: "clive-v1.appspot.com",
    messagingSenderId: "739607186994",
    appId: "1:739607186994:web:1defd843a3f0487481762b",
    measurementId: "G-SP3P65Z3P7"
  };

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);


console.log("🔥 firebase.js loaded");
