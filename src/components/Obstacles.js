import { View, StyleSheet } from 'react-native';

const Obstacles = ({
    color,
    obstacleWidth,
    obstacleHeight,
    randomBottom,
    gap,
    obstaclesLeft
}) => {
    return(
        <View>
            <View style={styles.obstacle}></View>
            <View style={styles.obstacle2}></View>
        </View>
    )
}

const styles = StyleSheet.create({
  obstacle: {
    position: 'absolute',
    backgroundColor: color,
    width: obstacleWidth,
    height: 500,
    left: obstaclesLeft,
    bottom: randomBottom + obstacleHeight + gap
  },

  obstacle2: {
    position: 'absolute',
    backgroundColor: color,
    width: obstacleWidth,
    height: obstacleHeight,
    left: obstaclesLeft,
    bottom: randomBottom
  }
});

export default Obstacles;
