import React from 'react'
import { Layers, Upload, Download, Eye } from 'lucide-react'

export default function SSPManager() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">SSP Manager</h1>
          <p className="text-gray-600">Manage System Structure and Parameterization packages (SSP 2.0)</p>
        </div>
        <div className="flex space-x-3">
          <button className="btn-outline">
            <Download className="w-4 h-4 mr-2" />
            Export SSP
          </button>
          <button className="btn-primary">
            <Upload className="w-4 h-4 mr-2" />
            Import SSP
          </button>
        </div>
      </div>

      {/* SSP Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Layers className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="font-semibold">System Structure</h3>
            </div>
            <p className="text-sm text-gray-600">
              Define component hierarchies and system architectures with SSP 2.0
            </p>
          </div>
        </div>

        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <Eye className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="font-semibold">Parameterization</h3>
            </div>
            <p className="text-sm text-gray-600">
              Manage parameter sets and configurations across system components
            </p>
          </div>
        </div>

        <div className="card">
          <div className="card-content p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Upload className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="font-semibold">FMI 3.0 Integration</h3>
            </div>
            <p className="text-sm text-gray-600">
              Full compatibility with FMI 3.0 features including arrays and clocks
            </p>
          </div>
        </div>
      </div>

      {/* SSP Packages */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">SSP Packages</h3>
        </div>
        <div className="card-content">
          <div className="text-center py-12 text-gray-500">
            <Layers className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No SSP packages available</p>
            <p className="text-sm">Import or create your first SSP package</p>
          </div>
        </div>
      </div>
    </div>
  )
}