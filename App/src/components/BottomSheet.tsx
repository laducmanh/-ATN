import React from 'react'
import { StyleSheet, Text, View, Modal, Pressable, SafeAreaView, Dimensions } from 'react-native'
import {
    LineChart,
    BarChart,
    PieChart,
    ProgressChart,
    ContributionGraph,
    StackedBarChart
  } from "react-native-chart-kit";

import Icon from 'react-native-vector-icons/Feather';

const BottomSheet = ({ isOpen, setIsOpen, data }) => {

  return (
    <Modal
      animationType="fade"
      transparent={true}
      visible={isOpen}
      onRequestClose={() => setIsOpen(false)}
    >
        <View style={styles.container}>
            <Pressable onPress={() => setIsOpen(false)} style={styles.touchable} />
            <SafeAreaView style={styles.body}>
                <View style={styles.bottomHandle}>
                    <Icon name="minus" size={40} />
                </View>
                <View style={styles.header}>
                    <Text style={styles.title}>{'Biểu đồ nhiệt độ'}</Text>
                    <Pressable onPress={() => setIsOpen(false)}>
                    <Icon name="x" size={24} />
                    </Pressable>
                </View>
                <LineChart
                    data={{
                    labels: data.map(item => parseInt(item.time, 10)),
                    datasets: [
                        {
                        data: data.map(item => (item.temp).toFixed(2))
                        }
                    ]
                    }}
                    width={Dimensions.get("window").width} // from react-native
                    height={300}
                    // yAxisLabel="$"
                    yAxisSuffix="°C"
                    yAxisInterval={5} // optional, defaults to 1
                    chartConfig={{
                    backgroundColor: "#e26a00",
                    backgroundGradientFrom: "#0D47A1",
                    backgroundGradientTo: "#55C7F2",
                    decimalPlaces: 2, // optional, defaults to 2dp
                    color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
                    labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
                    style: {
                        borderRadius: 16
                    },
                    propsForDots: {
                        r: "4",
                        strokeWidth: "2",
                        stroke: "#ffa726"
                    }
                    }}
                    bezier
                    style={{
                    }}
                />
            </SafeAreaView>
        </View>
    </Modal>
  )
}

export default BottomSheet

const styles = StyleSheet.create({
    bottomHandle: {
        alignItems: 'center'
    },
    container: {
        flex: 1, 
        backgroundColor: "rgba(0, 0, 0, 0.15)",
    },
    touchable: {
        flex: 1
    },
    body: {
        backgroundColor: '#fff',
        borderTopRightRadius: 20,
        borderTopLeftRadius: 20,
    },
    header: {
        flexDirection: 'row',
        paddingLeft: 16,
        paddingRight: 16,
        marginBottom: 16,
        alignItems: 'center',
    },
    title: {
        flex: 1,
        fontWeight: 'bold',
        textAlign: 'center',
    },
})