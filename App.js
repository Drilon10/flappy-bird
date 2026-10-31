import React, { useEffect, useState } from "react";
import { View, StyleSheet, useWindowDimensions } from "react-native";
import Bird from "./src/components/Bird";
const GRAVITY = 3;
const FRAME_DELAY = 30;
const BIRD_HEIGHT = 60;
export default function App() {
  const { width, height } = useWindowDimensions();
  const birdLeft = width / 2;
  const [birdBottom, setBirdBottom] = useState(height / 2);
  useEffect(() => {
  setBirdBottom(height / 2);
  }, [height]);
  useEffect(() => {
    if (birdBottom <= BIRD_HEIGHT / 2) return;
    const timerId = setTimeout(() => {
    setBirdBottom((previousBottom) =>
    Math.max(BIRD_HEIGHT / 2, previousBottom - GRAVITY)
    );
    }, FRAME_DELAY);
    return () => clearTimeout(timerId);
  }, [birdBottom]);
  return (
    <View style={styles.container}>
      <Bird birdLeft={birdLeft} birdBottom={birdBottom} />
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
  flex: 1,
  backgroundColor: "#ffffff",
  },
});
