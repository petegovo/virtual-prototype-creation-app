import React from 'react'
import { Workflow, Plus, Save, Play } from 'lucide-react'

export default function SystemDesigner() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Designer</h1>
          <p className="text-gray-600">Visual system composition and virtual prototype design</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn-outline">
            <Save className="w-4 h-4 mr-2" />
            Save Design
          </button>
          <button className="btn-primary">
            <Play className="w-4 h-4 mr-2" />
            Simulate
          </button>
        </div>
      </div>

      {/* Design Canvas */}
      <div className="grid grid-cols-4 gap-6 h-[600px]">
        {/* Component Library */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold">Components</h3>
          </div>
          <div className="card-content">
            <div className="space-y-3">
              <div className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-blue-500 rounded"></div>
                  <span className="text-sm font-medium">SystemC Models</span>
                </div>
              </div>
              <div className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded"></div>
                  <span className="text-sm font-medium">Simulink Models</span>
                </div>
              </div>
              <div className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-purple-500 rounded"></div>
                  <span className="text-sm font-medium">Modelica Models</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Design Canvas */}
        <div className="col-span-3 card">
          <div className="card-content p-0 h-full">
            <div className="h-full bg-gray-50 rounded-lg flex items-center justify-center">
              <div className="text-center text-gray-500">
                <Workflow className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <h3 className="text-lg font-semibold mb-2">Design Canvas</h3>
                <p className="text-sm">Drag components here to build your virtual prototype</p>
                <button className="btn-primary mt-4">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Component
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Properties Panel */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Properties</h3>
        </div>
        <div className="card-content">
          <div className="text-center py-8 text-gray-500">
            <p>Select a component to view its properties</p>
          </div>
        </div>
      </div>
    </div>
  )
}