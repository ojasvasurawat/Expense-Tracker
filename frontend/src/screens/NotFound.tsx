import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { TouchableOpacity, View } from "react-native";
import { RootStackParamList } from "../types/navigation";

type Props = NativeStackScreenProps<RootStackParamList, "NotFound">


export default function NotFound({navigation} : Props){
    return(
        <View className="flex-1 justify-center items-center">
            <TouchableOpacity onPress={() => {
                navigation.navigate('Home')
            }}>
                Go back to home screen
            </TouchableOpacity>
        </View>
    )
}