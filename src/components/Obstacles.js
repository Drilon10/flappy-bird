import React from 'react';
import { Image } from 'react-native';

const Obstacles = ({
    color,
    obstacleWidth, 
    obstacleHeight, 
    randomBottom, 
    gap, 
    obstaclesLeft}) => {

    return (
        <>
            <Image style={{
                position: 'absolute',
                zIndex: 0,
                width: obstacleWidth,
                height: 500,
                left: obstaclesLeft,
                bottom: randomBottom + obstacleHeight + gap,

                }}
                source={require('../../assets/pipe.png')}
                resizeMode="cover"
            />
            <Image style={{
                position: 'absolute',
                zIndex: 0,
                backgroundColor: color,
                width: obstacleWidth,
                height: obstacleHeight,
                left: obstaclesLeft,
                bottom: randomBottom,

                }}
                source={require('../../assets/pipe.png')}
                resizeMode="cover"
            />
        </>
    )
}

export default Obstacles
