import { View, Text, TextInput, SafeAreaView, TouchableOpacity, Button } from "react-native";
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from "../types/navigation";
import React from "react";
import axios from 'axios';
import { BACKEND_URL } from "@env";
import Toast from 'react-native-toast-message';
import GoogleAuthButton from "../components/GoogleAuth";


type Props = NativeStackScreenProps<RootStackParamList, "Login">

interface UserInfo {

} 
export default function Login({ navigation }: Props) {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [userInfo, setUserInfo] = React.useState<UserInfo | null>(null);

    const submitHandler = async () => {
        if (email === '' || password === '') {
            Toast.show({
                type: 'error',
                text1: 'Empty Fields'
            })
            return;
        }
        const res = await axios.post(`${BACKEND_URL}`, {
            email, password
        })

        if (res.data.message === 'Login successful') {
            navigation.navigate('Home')
        } else {
            Toast.show({
                type: 'error',
                text1: 'Login failed'
            })
        }
    }
    
    console.log(userInfo)

    return (
        <SafeAreaView className="flex-1 bg-gray-100">
            <View className="flex-1 justify-center px-5">
                <View className="mb-8"  >
                    <Text className="text-gray-400 text-base mb-1">HELLO,</Text>
                    <Text className="text-gray-900 text-3xl font-bold">Welcome Back</Text>
                </View>
                <View className="bg-white rounded-3xl p-6">
                    <View className="mb-4">
                        <Text className="text-gray-400 text-xs mb-2">Email</Text>
                        <View className="bg-gray-50 rounded-2xl px-4 py-1 flex-row items-center gap-2">
                            <Text>✉️</Text>
                            <TextInput
                                placeholder="you@example.com"
                                placeholderTextColor="#9ca3af"
                                onChangeText={value => setEmail(value)}
                                className="flex-1 text-gray-800 text-sm focus:outline-none"
                            />
                        </View>
                    </View>
                    <View className="mb-4">
                        <Text className="text-gray-400 text-xs mb-2">Password</Text>
                        <View className="bg-gray-50 rounded-2xl px-4 py-1 flex-row items-center gap-2">
                            <Text>🔒</Text>
                            <TextInput
                                placeholder="••••••••"
                                placeholderTextColor="#9ca3af"
                                onChangeText={value => setPassword(value)}
                                className="flex-1 text-gray-800 text-sm focus:outline-none"
                            />
                        </View>
                    </View>
                    <TouchableOpacity
                        className="bg-[#AED49B] rounded-2xl py-4 items-center mb-4"
                        onPress={submitHandler}
                    >
                        <Text className="text-white font-semibold text-sm">Sign In</Text>
                    </TouchableOpacity>
                    <GoogleAuthButton setUserInfo={setUserInfo}/>
                    <View className="flex-row justify-center">
                        <Text className="text-gray-400 text-sm">Don't have an account? </Text>
                        <TouchableOpacity onPress={() => {
                            navigation.navigate('Signup');
                        }}>
                            <Text className="text-[#AED49B] text-sm font-medium">Sign up</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </SafeAreaView>

    )
}