import React, { useEffect, useState } from "react";
import { View, StyleSheet, Text, Dimensions, TouchableWithoutFeedback, Image } from "react-native";
import Bird from "./src/components/Bird";
import Obstacles from "./src/components/Obstacles";


export default function App() {
  const screenWidth = Dimensions.get("screen").width;
  const screenHeight = Dimensions.get("screen").height;
  const birdLeft = screenWidth / 2
  const [birdBottom, setBirdBottom] = useState(screenHeight / 2)
  const [obstaclesLeft, setObstaclesLeft] = useState(screenWidth)
  const [obstaclesLeftTwo, setObstaclesLeftTwo] = useState(screenWidth + screenWidth/2 + 30)
  const [obstaclesNegHeight, setObstaclesNegHeight] = useState(0)
  const [obstaclesNegHeightTwo, setObstaclesNegHeightTwo] = useState(0)
  const [score, setScore] = useState(0)
  const gravity = 3

  let obstacleWidth = 60
  let obstacleHeight = 300
  let gap = 200

  // Once a collision occurs, stopping the timers keeps this state unchanged.
  const isGameOver = birdBottom <= 0 ||
    ((birdBottom < (obstaclesNegHeight + obstacleHeight + 30) ||
      birdBottom > (obstaclesNegHeight + obstacleHeight + gap - 30)) &&
      (obstaclesLeft > birdLeft - 30 && obstaclesLeft < birdLeft + 30)) ||
    ((birdBottom < (obstaclesNegHeightTwo + obstacleHeight + 30) ||
      birdBottom > (obstaclesNegHeightTwo + obstacleHeight + gap - 30)) &&
      (obstaclesLeftTwo > birdLeft - 30 && obstaclesLeftTwo < birdLeft + 30))

  useEffect(() => {
    if(!isGameOver) {
      const gameTimerId = setInterval(() => {
        setBirdBottom(birdBottom => birdBottom - gravity)
      }, 30)

      return () => {
        clearInterval(gameTimerId)
      }
    }
  }, [isGameOver])

  // obstacle1
  useEffect(() => {
    if(isGameOver) return
    const obstaclesTimerId = setInterval(() => {
      if(obstaclesLeft > -obstacleWidth) {
        setObstaclesLeft(previousLeft => previousLeft - 5)
      } else {
        setScore(previousScore => previousScore + 1)
        setObstaclesLeft(screenWidth)
        setObstaclesNegHeight(-Math.random() * 100)
      }
      }, 30)

      return () => {
        clearInterval(obstaclesTimerId)
      }
  }, [obstaclesLeft, isGameOver, obstacleWidth, screenWidth])

  // obstacle 2
  useEffect(() => {
    if(isGameOver) return
    const obstaclesTimerIdTwo = setInterval(() => {
      if(obstaclesLeftTwo > -obstacleWidth) {
        setObstaclesLeftTwo(previousLeft => previousLeft - 5)
      } else {
        setScore(previousScore => previousScore + 1)
        setObstaclesLeftTwo(screenWidth)
        setObstaclesNegHeightTwo(-Math.random() * 100)
      }
      }, 30)

      return () => {
        clearInterval(obstaclesTimerIdTwo)
      }
  }, [obstaclesLeftTwo, isGameOver, obstacleWidth, screenWidth])

  // jump behaviour
  const jump = () => {
    if(!isGameOver && (birdBottom < screenHeight)) {
      setBirdBottom(birdBottom => birdBottom + 50)
      console.log('jumped')
    }
  }

  return(
    <TouchableWithoutFeedback onPress={jump}>
      <View style={styles.container}>
        <Image source={require('./assets/background.png')} style={styles.backgroundImage}></Image>
        <Text style={styles.score}>Score: {score}</Text>
        <Bird
          birdBottom={birdBottom}
          birdLeft={birdLeft}
        ></Bird>

        <Obstacles
          color={'green'}
          obstacleWidth={obstacleWidth}
          obstacleHeight={obstacleHeight}
          randomBottom={obstaclesNegHeight}
          gap={gap}
          obstaclesLeft={obstaclesLeft}
        ></Obstacles>

        <Obstacles
          color={'yellow'}
          obstacleWidth={obstacleWidth}
          obstacleHeight={obstacleHeight}
          randomBottom={obstaclesNegHeightTwo}
          gap={gap}
          obstaclesLeft={obstaclesLeftTwo}
        ></Obstacles>

      </View>
    </TouchableWithoutFeedback>
  )
}

const styles = StyleSheet.create({
  
  container: {
    flex: 1,
  },
  score: {
    fontSize: 32,
    top: 50,
    position: 'absolute',
    zIndex: 1,
    color: 'white'
  },
  backgroundImage: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    left: 0,
    right: 0
  }
})
