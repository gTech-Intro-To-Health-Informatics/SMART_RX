'use client'
import { useState } from 'react';
import axios from 'axios';

export default function NewChat() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    drugs: '',
    patient_history: '',
    conversation_history: '',
  });

  const [showConversationHistory, setShowConversationHistory] = useState(false);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const toggleConversationHistory = () => {
    setShowConversationHistory(!showConversationHistory);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    try {
      await axios.put('/set_new_chat', formData);
      alert('New chat created!');
      setFormData({
        name: '',
        email: '',
        phone: '',
        drugs: '',
        patient_history: '',
        conversation_history: '',
      });
      setShowConversationHistory(false);
    } catch (error) {
      console.error('Error creating new chat:', error);
      alert('Failed to create new chat.');
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">Create a New Chat</h1>
      <form onSubmit={handleSubmit} className="space-y-6 max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md">
        <div>
          <label className="block text-gray-700 font-semibold">Patient Name:</label>
          <input
            className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter patient's name"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 font-semibold">Patient Email:</label>
          <input
            className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter patient's email"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 font-semibold">Phone Number:</label>
          <input
            className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            placeholder="Enter phone number"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 font-semibold">Drugs Prescribed:</label>
          <input
            className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            name="drugs"
            value={formData.drugs}
            onChange={handleChange}
            placeholder="Enter drugs prescribed"
          />
        </div>
        <div>
          <label className="block text-gray-700 font-semibold">Patient History:</label>
          <textarea
            className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            name="patient_history"
            value={formData.patient_history}
            onChange={handleChange}
            placeholder="Enter patient history"
            rows={5}
          ></textarea>
        </div>
        <div>
          <button
            type="button"
            onClick={toggleConversationHistory}
            className="mt-4 text-blue-600 hover:underline"
          >
            {showConversationHistory ? 'Hide Conversation History' : 'Add Conversation History'}
          </button>
        </div>
        {showConversationHistory && (
          <div>
            <label className="block text-gray-700 font-semibold">Conversation History:</label>
            <textarea
              className="mt-2 w-full p-3 border border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              name="conversation_history"
              value={formData.conversation_history}
              onChange={handleChange}
              placeholder="Enter conversation history"
              rows={5}
            ></textarea>
          </div>
        )}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 transition duration-200"
        >
          Create Chat
        </button>
      </form>
    </div>
  );
}
