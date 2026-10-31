import { Image } from 'react-native';

export default function Bird({ birdLeft, birdBottom }) {
    const birdWidth = 40;
    const birdHeight = 40;

    return(
       <Image
        style={{
          position: 'absolute',
          left: birdLeft - (birdWidth/2),
          bottom: birdBottom - (birdHeight/2),
          width: birdWidth,
          height: birdHeight
        }}
        source={require('../../assets/bird1.png')}
        resizeMode='stretch'
       ></Image>
    )
}

