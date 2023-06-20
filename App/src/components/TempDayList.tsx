import React, { useState, useEffect } from 'react';
import { Text, View, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

import { db } from "../../firebase.config";
import { ref, onValue } from "firebase/database";
import BottomSheet from './BottomSheet';

export default function TempDayList() {

  const [tempDay, setTempDay] = useState([]);
  
  function convertData(data) {
    const today = new Date();
    // lấy tất cả các ngày trong object
    const dates = Object.keys(data).map((date) => date.split(" ")[0]);
    // lấy các ngày duy nhất
    const uniqueDates = Array.from(new Set(dates));
  
    // tạo mảng kết quả
    const result = uniqueDates.map((date) => {
      // lọc ra tất cả các giờ của ngày hiện tại
      const filteredData = Object.keys(data)
        .filter((key) => key.includes(date))
        .map((key) => {
          return {
            time: key.split(" ")[1],
            temp: data[key],
          };
        });
  
      // tìm nhiệt độ cao nhất và thấp nhất trong ngày hiện tại
      const maxTemp = Math.max(...filteredData.map((item) => item.temp));
      const minTemp = Math.min(...filteredData.map((item) => item.temp));
  
      // tạo đối tượng ngày
      return {
        day: new Date(date).toLocaleDateString("vi-VN", { weekday: "long" }).split(",")[0],
        date: date,
        max: maxTemp.toFixed(),
        min: minTemp.toFixed(),
        temperatures: filteredData,
      };
    });
    return result.filter((item) => new Date(item.date) > today);
  };
  
  useEffect (() => {
    const starCountRef = ref(db, 'Predict');
    onValue(starCountRef, (snapshot) => {
      const data = snapshot.val();
      const newObj = convertData(data);
      setTempDay(newObj);
    })
  }, []);


  const [openBtnSheet, setOpenBtnSheet] = useState(false);
  const [dataTempDay, setDataTempDay] = useState([]);
  return (
    <View style={ styles.card }>
      {
        tempDay.slice(0,7).map((item, index) => {
          return (
            <>
              <TouchableOpacity
                key={index}
                style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}
                onPress={() => {
                  setOpenBtnSheet(true);
                  setDataTempDay(item.temperatures);
                }}
              >
                <Text style={{ fontSize: 18, fontWeight: 600, }}>{item.day}</Text>
                <View style={{ flexDirection: "row", alignItems: "center" }}>
                  <Text style={{ fontSize: 18, color: "#969696", }}>{item.min}°</Text>
                  <LinearGradient
                      // Background Linear Gradient
                      start={{x:0, y:0}}
                      end={{x:1, y:0}}
                      colors={['#62CDFF', '#C9F4AA', '#FCFFB2', '#FFD966', '#F45050']}
                      style={{width: 60, height: 6, borderRadius: 24, marginRight: 16, marginLeft: 16 }}
                  />
                  <Text style={{ fontSize: 18 }}>{item.max}°</Text>
                </View>
              </TouchableOpacity>
              <BottomSheet
                isOpen={openBtnSheet}
                setIsOpen={setOpenBtnSheet}
                data={dataTempDay}
              />
            </>
          )
        })
      }
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    margin: 16,
    marginTop: 0,
    padding: 24,
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    flexDirection: "column",
    gap: 16,
  },
});
