import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, ActivityIndicator, ImageBackground } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Lottie from 'lottie-react-native';
import Icon from 'react-native-vector-icons/Ionicons';

import { db } from "../../firebase.config";
import { ref, onValue } from "firebase/database";

import TempTimeList from './TempTimeList';

export default function TempMainCard() {
    const [tempReal, setTempReal] = useState();
    const [timeString, settimeString] = useState({});
  
    function formatDate (d) {
      const days = ['Chủ Nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
  
      const dateTime = {
        day: days[d.getDay()],
        date: d.getDate(),
        month: d.getMonth() + 1,
        year: d.getFullYear(),
        seconds: `0${d.getSeconds()}`.slice(-2),
        minutes: `0${d.getMinutes()}`.slice(-2),
        hours: `0${d.getHours()}`.slice(-2),
      }
  
      return dateTime
    }
  
    useEffect (() => {
      setInterval(() => {
        const now = new Date();
        const newTimeString = formatDate(now);
  
        settimeString(newTimeString);
  
      }, 1000)
      const starCountRef = ref(db, 'Actual/Temperature');
      onValue(starCountRef, (snapshot) => {
        const data = snapshot.val();
        setTempReal(data.toFixed());
      })
    }, []);
    return (
        <>
            <ImageBackground
                style={styles.img} 
                source={
                (timeString.hours < 18) && (timeString.hours > 0) ? require('../assets/img/day.jpg') : require('../assets/img/night.jpg')
                }
                PlaceholderContent={<ActivityIndicator />}
            >
                <View style={{ flex: 1, justifyContent: "flex-end"}}>
                <LinearGradient
                    // Background Linear Gradient
                    start={{x:0, y:0}}
                    end={{x:0, y:1}}
                    colors={['transparent', '#F4F4F4']}
                    style={{width: "100%", height:80, alignItems: "center", justifyContent: "flex-end" }}
                />
                </View>
            </ImageBackground>
            <View style={styles.cardMain}>
                <View>
                <View style={{ ...styles.row, marginBottom: 4 }}>
                    <Icon name="location" size={20} />
                    <Text style={styles.locationText}>Hồ Chí Minh</Text>
                </View>
                <Text style={styles.timeText}>{`${timeString.hours}:${timeString.minutes}:${timeString.seconds} ${timeString.day}, ${timeString.date} tháng ${timeString.month}`}</Text>
                </View>
                <View style={{ ...styles.row, justifyContent: "center" }}>
                <Lottie 
                    style={{ width: 160, height: 160 }} 
                    source={ (timeString.hours < 24) && (timeString.hours >= 18) ? require('../assets/img/night.json')
                    : (timeString.hours < 18) && (timeString.hours >= 12) ? require('../assets/img/sunclouds.json')
                    : (timeString.hours < 12) && (timeString.hours > 6) ? require('../assets/img/sunny.json')
                    : require('../assets/img/cloudynight.json')
                    } 
                    autoPlay 
                    loop 
                />
                <Text style={styles.tempText}>{tempReal}°C</Text>
                </View>
                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                    <TempTimeList />
                </ScrollView>
            </View>
        </>    
    )
}

const styles = StyleSheet.create({
  img: {
    height: 248,
    width: "100%",
  },
  cardMain: {
    margin: 16,
    padding: 24,
    paddingTop: 16, 
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
  },
  locationText: {
    marginLeft: 6,
    fontWeight: 500,
    fontSize: 20,
  },
  timeText: {
    color: "#969696",
    fontSize: 14,
  },
  tempText: {
    fontSize: 72,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
  },
})