import React, { useState } from 'react'
import { View, Text, TextInput, TouchableOpacity, ScrollView, Alert } from 'react-native'
import axios from 'axios'

const API_BASE = 'https://globe-swift.org/api' // Change for dev

export default function App() {
  const [token, setToken] = useState(null)
  const [userId, setUserId] = useState('user-123')
  const [loanId, setLoanId] = useState('PL-001')
  const [amount, setAmount] = useState('300')

  const getToken = async () => {
    try {
      const res = await axios.post(`${API_BASE}/v1/auth/token`, { user_id: userId })
      setToken(res.data.access_token)
      Alert.alert('Success', 'Token obtained')
    } catch (err) {
      Alert.alert('Error', err.message)
    }
  }

  const createLoan = async () => {
    if (!token) return Alert.alert('Error', 'Get token first')
    try {
      const res = await axios.post(`${API_BASE}/v1/personal/loans`, {
        loan_id: loanId,
        lender_name: 'Lender',
        amount: 15000,
        monthly_payment: 300,
        interest_rate: 12.5,
        due_date: '12/27'
      }, { headers: { Authorization: `Bearer ${token}` } })
      Alert.alert('Success', 'Loan created')
    } catch (err) {
      Alert.alert('Error', err.message)
    }
  }

  const payLoan = async () => {
    if (!token) return Alert.alert('Error', 'Get token first')
    try {
      const res = await axios.post(`${API_BASE}/v1/personal/pay`, {
        loan_id: loanId,
        amount: parseFloat(amount)
      }, { headers: { Authorization: `Bearer ${token}` } })
      Alert.alert('Success', `Paid $${amount}`)
    } catch (err) {
      Alert.alert('Error', err.message)
    }
  }

  return (
    <ScrollView style={{ padding: 20, marginTop: 40 }}>
      <Text style={{ fontSize: 24, fontWeight: 'bold', marginBottom: 20 }}>Loan Manager</Text>
      
      <Text>User ID:</Text>
      <TextInput style={{ borderWidth: 1, padding: 10, marginBottom: 10 }} value={userId} onChangeText={setUserId} />
      <TouchableOpacity onPress={getToken} style={{ backgroundColor: '#007AFF', padding: 10, marginBottom: 20 }}>
        <Text style={{ color: 'white', textAlign: 'center' }}>Get Token</Text>
      </TouchableOpacity>

      <Text>Loan ID:</Text>
      <TextInput style={{ borderWidth: 1, padding: 10, marginBottom: 10 }} value={loanId} onChangeText={setLoanId} />
      <TouchableOpacity onPress={createLoan} style={{ backgroundColor: '#34C759', padding: 10, marginBottom: 20 }}>
        <Text style={{ color: 'white', textAlign: 'center' }}>Create Loan</Text>
      </TouchableOpacity>

      <Text>Payment Amount:</Text>
      <TextInput style={{ borderWidth: 1, padding: 10, marginBottom: 10 }} value={amount} onChangeText={setAmount} keyboardType="decimal-pad" />
      <TouchableOpacity onPress={payLoan} style={{ backgroundColor: '#FF9500', padding: 10 }}>
        <Text style={{ color: 'white', textAlign: 'center' }}>Make Payment</Text>
      </TouchableOpacity>
    </ScrollView>
  )
}
