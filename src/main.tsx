import React from 'react'
import ReactDOM from 'react-dom/client'
import { Toaster } from 'react-hot-toast'
import App from './App.tsx'
import './index.css'
import './lib/i18n'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <App />
        <Toaster
            position="top-right"
            toastOptions={{
                style: {
                    background: '#0E243F',
                    color: '#fff',
                    border: '1px solid #00B8C4',
                },
            }}
        />
    </React.StrictMode>,
)