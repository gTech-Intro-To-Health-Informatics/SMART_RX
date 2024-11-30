'use client'

import { useState, useEffect } from 'react';
import axios from 'axios';

export default function PatientChat() {
  const [conversationHistory, setConversationHistory] = useState([
    {
      role: 'Pharma Chatbot',
      content: 'Hello! How can I assist you today?',
    },
  ]);
  const [patientQuery, setPatientQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const [drugList, setDrugList] = useState(['Metformin', 'Adderall']);
  const [patientHistory, setPatientHistory] = useState(
    'Patient has a history of hypertension and ADHD'
  );
  const [rawConversationInput, setRawConversationInput] = useState(
    JSON.stringify(conversationHistory, null, 2)
  );
  const [jsonError, setJsonError] = useState(null);

  const [showSettings, setShowSettings] = useState(false);

  const handleSend = async () => {
    if (!patientQuery.trim()) return;

    const newMessage = {
      role: 'user',
      content: patientQuery,
    };

    const updatedConversation = [...conversationHistory, newMessage];

    setConversationHistory(updatedConversation);
    setPatientQuery('');
    setLoading(true);

    try {
      const response = await axios.post(
        'https://smartrx-production.up.railway.app/chat',
        {
          drug_list: drugList,
          patient_history: patientHistory,
          conversation_history: updatedConversation,
          patient_query: patientQuery,
        }
      );

      console.log('Response:', response, response.data.conversation_history);
      setConversationHistory(response.data.conversation_history);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyConversationHistory = () => {
    try {
      const parsed = JSON.parse(rawConversationInput);
      setConversationHistory(parsed);
      setJsonError(null);
    } catch (error: any) {
      setJsonError(error.message);
    }
  };

  useEffect(() => {
    setRawConversationInput(JSON.stringify(conversationHistory, null, 2));
  }, [conversationHistory]);

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6 text-center">Patient Chat</h1>

      <div className="space-y-6 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
        <div className="h-96 overflow-y-auto border border-gray-300 dark:border-gray-700 p-4 rounded-md">
          {conversationHistory.map((message, index) => (
            <div key={index} className="mb-4">
              <p
                className={`font-semibold ${
                  message.role === 'user'
                    ? 'text-blue-600'
                    : 'text-green-600'
                }`}
              >
                {message.role === 'user' ? 'You' : 'Pharma Chatbot'}:
              </p>
              <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
                {message.content}
              </p>
            </div>
          ))}
        </div>
        <div>
          <textarea
            className="w-full p-3 border border-gray-300 dark:border-gray-700 rounded-md bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            value={patientQuery}
            onChange={(e) => setPatientQuery(e.target.value)}
            placeholder="Type your message..."
          ></textarea>
          <button
            onClick={handleSend}
            disabled={loading}
            className="mt-2 w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 transition duration-200"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>

      <button
        onClick={() => setShowSettings(!showSettings)}
        className="mt-4 w-full bg-gray-600 text-white py-2 rounded-md font-semibold hover:bg-gray-700 transition duration-200"
      >
        {showSettings ? 'Hide Settings' : 'Show Settings'}
      </button>

      {showSettings && (
        <div className="settings-panel bg-gray-100 dark:bg-gray-900 p-4 rounded-md mt-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-200">
            Settings
          </h2>

          <div className="mb-4">
            <label className="block text-gray-800 dark:text-gray-200 font-semibold mb-2">
              Medications Taken (comma-separated):
            </label>
            <input
              type="text"
              className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              value={drugList.join(', ')}
              onChange={(e) =>
                setDrugList(
                  e.target.value.split(',').map((item) => item.trim())
                )
              }
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 dark:text-gray-200 font-semibold mb-2">
              Patient History:
            </label>
            <textarea
              className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              rows={3}
              value={patientHistory}
              onChange={(e) => setPatientHistory(e.target.value)}
            ></textarea>
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 dark:text-gray-200 font-semibold mb-2">
              Raw Conversation History (JSON):
            </label>
            <textarea
              className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              rows={5}
              value={rawConversationInput}
              onChange={(e) => setRawConversationInput(e.target.value)}
            ></textarea>
            {jsonError && (
              <p className="text-red-500 mt-2">Invalid JSON: {jsonError}</p>
            )}
            <button
              className="mt-2 bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
              onClick={applyConversationHistory}
            >
              Apply Conversation History
            </button>
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 dark:text-gray-200 font-semibold mb-2">
              Current Conversation History (Read-only):
            </label>
            <textarea
              className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              rows={5}
              value={JSON.stringify(conversationHistory, null, 2)}
              readOnly
            ></textarea>
          </div>
        </div>
      )}
    </div>
  );
}
