import React from 'react'
import { Play, Pause, Square, Settings, BarChart3 } from 'lucide-react'

export default function Simulation() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Simulation</h1>
          <p className="text-gray-600">Execute and monitor co-simulation scenarios</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn-outline">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </button>
          <button className="btn-primary">
            <Play className="w-4 h-4 mr-2" />
            Start Simulation
          </button>
        </div>
      </div>

      {/* Simulation Controls */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Simulation Controls</h3>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="label">Start Time</label>
              <input type="number" className="input" defaultValue="0.0" />
            </div>
            <div>
              <label className="label">Stop Time</label>
              <input type="number" className="input" defaultValue="10.0" />
            </div>
            <div>
              <label className="label">Step Size</label>
              <input type="number" className="input" defaultValue="0.01" />
            </div>
          </div>
          
          <div className="flex items-center space-x-4 mt-6">
            <button className="btn-primary">
              <Play className="w-4 h-4 mr-2" />
              Start
            </button>
            <button className="btn-outline">
              <Pause className="w-4 h-4 mr-2" />
              Pause
            </button>
            <button className="btn-outline">
              <Square className="w-4 h-4 mr-2" />
              Stop
            </button>
          </div>
        </div>
      </div>

      {/* Simulation Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Status</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Simulation State</span>
                <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm">Stopped</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Current Time</span>
                <span className="font-mono">0.000 s</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Progress</span>
                <span>0%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-primary-600 h-2 rounded-full" style={{ width: '0%' }}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Performance</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Real-time Factor</span>
                <span className="font-mono">--</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Step Time</span>
                <span className="font-mono">-- ms</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Memory Usage</span>
                <span className="font-mono">-- MB</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Results Visualization */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Results</h3>
        </div>
        <div className="card-content">
          <div className="text-center py-12 text-gray-500">
            <BarChart3 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No simulation results available</p>
            <p className="text-sm">Run a simulation to see results and plots</p>
          </div>
        </div>
      </div>
    </div>
  )
}