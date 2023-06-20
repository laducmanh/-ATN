import {initializeApp} from "firebase/app";
import {getDatabase} from "firebase/database";
import {getAnalytics} from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyD07F5mfZLRYWQ6fuwXB1xc1tdKE3LJn4U",
  authDomain: "raspberry-esp32.firebaseapp.com",
  databaseURL: "https://raspberry-esp32-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "raspberry-esp32",
  storageBucket: "raspberry-esp32.appspot.com",
  messagingSenderId: "449396500758",
  appId: "1:449396500758:web:3c88b0a71803ae8e4dc837",
  measurementId: "G-T1T0P5FY38"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

const db = getDatabase();
export { db }