import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import FMUManager from './pages/FMUManager'
import SSPManager from './pages/SSPManager'
import SystemDesigner from './pages/SystemDesigner'
import Simulation from './pages/Simulation'
import Projects from './pages/Projects'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/fmu" element={<FMUManager />} />
          <Route path="/ssp" element={<SSPManager />} />
          <Route path="/designer" element={<SystemDesigner />} />
          <Route path="/simulation" element={<Simulation />} />
          <Route path="/projects" element={<Projects />} />
        </Routes>
      </Layout>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
    </div>
  )
}

export default App