import React from 'react'
import { FolderOpen, Plus, Search, Calendar } from 'lucide-react'

export default function Projects() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-600">Manage virtual prototype projects and configurations</p>
        </div>
        <button className="btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Project
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Search projects..."
          className="input pl-10"
        />
      </div>

      {/* Projects Grid */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold">Recent Projects</h3>
        </div>
        <div className="card-content">
          <div className="text-center py-12 text-gray-500">
            <FolderOpen className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No projects created yet</p>
            <p className="text-sm">Create your first virtual prototype project</p>
            <button className="btn-primary mt-4">
              <Plus className="w-4 h-4 mr-2" />
              Create Project
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}