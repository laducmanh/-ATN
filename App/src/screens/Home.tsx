import React, { useState, useEffect } from 'react';
import {View, ScrollView, StyleSheet, SafeAreaView, Text, Modal, TouchableOpacity} from 'react-native';
import notifee, { AndroidStyle } from '@notifee/react-native';
import BackgroundService from 'react-native-background-actions';
import Icon from 'react-native-vector-icons/Ionicons';

import TempMainCard from '../components/TempMainCard';
import TempDayList from '../components/TempDayList';

import { db } from "../../firebase.config";
import { ref, onValue } from "firebase/database";

export default function Home() {
  const [modalVisible, setModalVisible] = useState(false);

  const onDisplayNotification = async ({title, body}) => {
    // Request permissions (required for iOS)
    await notifee.requestPermission()

    // Create a channel (required for Android)
    const channelId = await notifee.createChannel({
      id: 'default',
      name: 'Default Channel',
    });

    // Display a notification
    await notifee.displayNotification({
      title,
      body,
      android: {
        channelId,
        style: { type: AndroidStyle.BIGPICTURE, picture: require('../assets/img/mushroom.png') },
        //smallIcon: 'name-of-a-small-icon', // optional, defaults to 'ic_launcher'.
        // pressAction is needed if you want the notification to open the app when pressed
        pressAction: {
          id: 'default',
        },
      },
    });
  }

  const [future, setFuture] = useState(0);
  const [times, setTimes] = useState(0);
  useEffect (() => {
    startBackgroundService();
  }, []);

  const sleep = (time) => new Promise((resolve) => setTimeout(() => resolve(), time));

  const veryIntensiveTask = async (taskDataArguments) => {
    // Example of an infinite loop task
    const { delay } = taskDataArguments;
    await new Promise( async (resolve) => {
      const starCountRef = ref(db, 'Predict');
      onValue(starCountRef, (snapshot) => {
        const data = snapshot.val();

        // Lấy danh sách các key từ dữ liệu
        const keys = Object.keys(data);

        // Khởi tạo biến đếm và biến lưu trữ value lớn nhất
        let count = 0;
        let maxVal = null;

        // Lặp qua từng key trong danh sách keys
        for (let i = 0; i < keys.length; i++) {
          const key = keys[i];
          const value = data[key].toFixed();

          // Kiểm tra nếu value nằm ngoài khoảng 24 đến 32
          if (value < 24 || value > 32) {
            // Nếu đây là key đầu tiên hoặc value lớn hơn giá trị lớn nhất hiện tại, cập nhật giá trị lớn nhất
            if (i === 0 || value > maxVal) {
              maxVal = value;
            }
            count++;
          } else {
            // Nếu value nằm trong khoảng 24 đến 32, thoát khỏi vòng lặp
            break;
          }
        }

        if (count > 0) {
          setFuture(maxVal);
          setTimes(count);
          onDisplayNotification({title: "Cảnh báo nhiệt độ", body: `Trong khoảng ${count} giờ tới, nhiệt độ có thể đạt ${maxVal}°C`});
          setModalVisible(true);
        }

        // const firstKey = Object.keys(data)[0];
        // const firstValue = data[firstKey].toFixed();
        // if (firstValue < 24 || firstValue > 32) {
        //   setFuture(firstValue);
        //   onDisplayNotification({title: "Cảnh báo nhiệt độ", body: `Giờ tới nhiệt độ có thể đạt ${firstValue}`});
        //   setModalVisible(true);
        // }
      })
      await BackgroundService.updateNotification({taskDesc: 'Ứng dụng đang được chạy nền để dự báo nhiệt độ'});
      await sleep(delay);
    });
  };

  const options = {
    taskName: 'Cảnh báo',
    taskTitle: 'Cảnh báo nhiệt độ',
    taskDesc: 'Ứng dụng đang được chạy nền để dự báo nhiệt độ',
    taskIcon: {
        name: 'ic_launcher',
        type: 'mipmap',
    },
    color: '#ff00ff',
    linkingURI: 'yourSchemeHere://chat/jane', // See Deep Linking for more info
    parameters: {
        delay: 1000,
    },
  };

  const startBackgroundService = async () => {
    await BackgroundService.start(veryIntensiveTask, options);
    await BackgroundService.updateNotification({taskDesc: 'New ExampleTask description'});
  }

  const stopBackgroundService = async () => {
    await BackgroundService.stop();
  }

  const [isBackgroundService, setIsBackgroundService] = useState(true);

  return (
    <ScrollView style={styles.text}>
      <TempMainCard />
      <TempDayList />
      <View style={ styles.card }>
        <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
          <Text style={{ fontSize: 18, fontWeight: 600, }}>Cảnh báo:</Text>
          <View style={{ flexDirection: "row", alignItems: "center" }}>
            <TouchableOpacity
              style={{
                padding: 8,
                backgroundColor: isBackgroundService ? '#54B435' : '#B6D7AC',
                borderTopLeftRadius: 6,
                borderBottomLeftRadius: 6,
                justifyContent: 'center',
                alignItems: 'center',
                alignSelf: 'center',
              }}
              onPress={() => {startBackgroundService(); setIsBackgroundService(true) }}
            >
              <Text style={{ color: '#FFFFFF', fontWeight: 600, }}>Bật</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={{
                padding: 8,
                borderTopRightRadius: 6,
                borderBottomRightRadius: 6,
                backgroundColor: isBackgroundService ? '#F19999' : '#ED2B2A',
                justifyContent: 'center',
                alignItems: 'center',
                alignSelf: 'center',
              }}
              onPress={() => {stopBackgroundService(); setIsBackgroundService(false) }}
            >
              <Text style={{ color: '#FFFFFF', fontWeight: 600, }}>Tắt</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}>
        <View 
          style={{
            flex: 1, 
            backgroundColor: "rgba(0, 0, 0, 0.15)",
            justifyContent: "center",
            alignItems: "center",
          }}>
            <SafeAreaView style={{
              backgroundColor: "#FFFFFF",
              flexDirection: 'column',
              justifyContent: "center",
              marginLeft: 16,
              marginRight: 16,
              borderRadius: 15,
            }}>
              <View style={{
                alignItems: "center", 
                backgroundColor: "#FF5564", 
                padding: 16,
                borderTopLeftRadius: 15,
                borderTopRightRadius: 15,
              }}>
                <Icon name="warning-outline" size={64} style={{color: "#FFFFFF"}}/>
              </View>
              <View style={{alignItems: "center", padding: 28}}>
                <Text style={{ color: "#222222", fontSize: 28, fontWeight: "bold"}}>
                  Warning!
                </Text>
                <Text style={{ color: "#222222", fontSize: 18, marginTop: 16, textAlign: "center"}}>
                  {`Trong khoảng ${times} giờ tới, nhiệt độ có thể đạt ${future}°C, hãy cân nhắc để kịp thời điều chỉnh cho nấm có thể sinh trưởng tối ưu`}
                </Text>
                <TouchableOpacity
                  style={{ 
                    alignItems: "center", 
                    justifyContent: "center",
                    backgroundColor: "#FF5564",
                    paddingHorizontal: 30,
                    paddingVertical: 10,
                    marginTop: 30,
                    borderRadius: 50,
                  }}
                  onPress={() => setModalVisible(!modalVisible)}>
                  <Text style={{color: "#FFFFFF", fontWeight: "bold"}}>Close</Text>
                </TouchableOpacity>
              </View>
            </SafeAreaView>
        </View>
      </Modal>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  card: {
    margin: 16,
    marginTop: 0,
    padding: 24,
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
  },
});
