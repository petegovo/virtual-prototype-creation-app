import React from 'react'
import { Upload, Package, Search, Filter } from 'lucide-react'

export default function FMUManager() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">FMU Manager</h1>
          <p className="text-gray-600">Import and manage FMI 3.0 models from SystemC, Simulink, and Modelica</p>
        </div>
        <button className="btn-primary">
          <Upload className="w-4 h-4 mr-2" />
          Upload FMU
        </button>
      </div>

      {/* Upload Area */}
      <div className="card">
        <div className="card-content p-8">
          <div className="dropzone">
            <Package className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Drop FMU files here or click to browse
            </h3>
            <p className="text-gray-600 mb-4">
              Supports FMI 1.0, 2.0, and 3.0 formats
            </p>
            <button className="btn-outline">
              Choose Files
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="flex items-center space-x-4">
        <div className="flex-1 relative">
          <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search FMUs..."
            className="input pl-10"
          />
        </div>
        <button className="btn-outline">
          <Filter className="w-4 h-4 mr-2" />
          Filter
        </button>
      </div>

      {/* FMU List */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Uploaded FMUs</h3>
        </div>
        <div className="card-content">
          <div className="text-center py-12 text-gray-500">
            <Package className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No FMUs uploaded yet</p>
            <p className="text-sm">Upload your first FMU to get started</p>
          </div>
        </div>
      </div>
    </div>
  )
}