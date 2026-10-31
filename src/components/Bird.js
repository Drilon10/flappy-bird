import { View, StyleSheet } from 'react-native';

export default function Bird({ birdLeft, birdBottom }) {
    const birdWidth = 50;
    const birdHeight = 50;

    return(
        <View
            style={styles.bird}
        ></View>
    )
}

const styles = StyleSheet.create({
  bird: {
    position: "absolute",
    width: birdWidth,
    height: birdHeight,
    backgroundColor: 'blue',
    left: birdLeft - birdWidth / 2,
    bottom: birdBottom - birdHeight / 2
  }
})
