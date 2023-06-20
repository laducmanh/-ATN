import React, { useState, useEffect } from 'react';
import { Text, View, ScrollView, StyleSheet } from 'react-native';

import Ionicons from "react-native-vector-icons/Ionicons";
import MaterialIcons from "react-native-vector-icons/MaterialIcons";
import FontAwesome5 from "react-native-vector-icons/FontAwesome5";

import { db } from "../../firebase.config";
import { ref, onValue } from "firebase/database";

export default function TempTimeList() {
  var today = new Date();
  
  const [tempTime, setTempTime] = useState([]);
  useEffect (() => {
    const starCountRef = ref(db, 'Predict');
    onValue(starCountRef, (snapshot) => {
      const data = snapshot.val();
      const dataRealTime = Object.keys(snapshot.val()).filter((date) => {
        const someDate = new Date(date);
        return today <= someDate;
      });
      const newTemp = dataRealTime.map(key => ({
        temp: data[key].toFixed(),
        date: key.split(" ")[0],
        time: key.split(" ")[1],
        hours: (key.split(" ")[1]).split(":")[0],
      }));
      setTempTime(newTemp);
    })
    console.log(tempTime);
  }, []);

  return (
    <>
      {
        tempTime.slice(0,24).map((item, index) => {
          return (
            <View 
              key={index}
              style={ index == tempTime.slice(0,24).length - 1 ? { justifyContent: 'center', alignItems: 'center', } : { marginRight: 28, justifyContent: 'center', alignItems: 'center', }} 
            >
              <Text style={{ fontSize: 16, color: "#969696", }}>{item.time}</Text>
              { (item.hours < parseInt(24)) && (item.hours >= parseInt(18)) ? <Ionicons name="md-moon" size={32} color={"#FFD95A"} style={{ marginTop: 8, marginBottom: 8 }} />
              : (item.hours < parseInt(18)) && (item.hours >= parseInt(12)) ? <Ionicons name="partly-sunny" size={32} color={"#FFD95A"} style={{ marginTop: 8, marginBottom: 8 }} />
              : (item.hours < parseInt(12)) && (item.hours > parseInt(6)) ? <MaterialIcons name="wb-sunny" size={32} color={"#FFD95A"} style={{ marginTop: 8, marginBottom: 8 }}/>
              : <FontAwesome5 name="cloud-moon" size={32} color={"#FFD95A"} style={{ marginTop: 8, marginBottom: 8 }} />
              } 
              <Text style={{ fontSize: 16, fontWeight: 600 }}>{item.temp}°</Text>
            </View>
          )
        })
      }
    </>
  );
}

const styles = StyleSheet.create({
});
